#!/usr/bin/env python3
"""
test_look_write.py - tests for look_write.py.

created: 2026-11 (DataWizard)
edit_log:
  - Seed 1.15.0 2026-11-18 - first Seed release; fixture names made generic

Standard library unittest only. Fixtures are made OUTSIDE the vault, under
$LOOK_WRITE_FIXTURES (default ~/look_write_fixtures/), one fresh folder per
test, removed after the test. Run:

    cd /tmp && python3 -B "<scripts folder>/test_look_write.py" -v
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import look_write as lw  # noqa: E402

BASE = os.environ.get("LOOK_WRITE_FIXTURES") or os.path.expanduser("~/look_write_fixtures")

MAP_TEXT = (
    "---\ntype: infrastructure\n---\n\n# Vault Config\n\n## Paths\n\n"
    "| Key | Value |\n|---|---|\n"
    "| board_dir | `_Coordination/` (board) |\n"
    "| holon_lens_map | `_Alpha/=AL; _Beta/=BE; _Gamma/=GA; _Delta/=DE` "
    "(vault-relative folder prefix = project abbreviation) |\n")

HEADER = "| " + " | ".join(lw.COLS) + " |"
SEP = lw.render_sep(12)


def note_text(abbr="AL", year=2026, rows=(), eol="\n", frozen=False, extra_after="",
              flag=True, final_eol=True):
    t = ["---", "title: 'x'", "type: project-doc", "created: 2026-11-18", "updated: 2026-11-18",
         "operator: Operator One"]
    if flag:
        t.append("look_ledger: " + abbr)
    t += ["edit_log:", "  - 'ABC-S12 2026-11-18 - created'", "---", "",
          "*Part of the [[Research Tracking Index]]*"]
    if frozen:
        t.append("*Frozen 2026-11-18 (D183): old rows kept as history; do not edit. "
                 "New looks: [[x]].*")
    t += ["", "## Looks %d" % year, "", HEADER, SEP]
    t += list(rows)
    s = eol.join(t)
    if final_eol:
        s += eol
    return s + extra_after


def row(subject="SampleTool", kind="tool", key="url:github.com/sampletool/sampletool", date="2026-11-18",
        depth="light", rel="medium", for_="", outcome="watch", trigger="", finding="ok",
        view="", by="ABC-S12"):
    return lw.render_row([subject, kind, key, date, depth, rel, for_, outcome, trigger, finding,
                          view, by])


class Base(unittest.TestCase):
    def setUp(self):
        os.makedirs(BASE, exist_ok=True)
        self.d = tempfile.mkdtemp(prefix="lw_", dir=BASE)
        self.map = os.path.join(self.d, "Vault Config.md")
        with open(self.map, "w") as fh:
            fh.write(MAP_TEXT)
        self.ledger = os.path.join(self.d, "4.0 Looks 2026 - AL Research Tracking Index.md")

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def write(self, path, text, binary=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(text if binary else text.encode("utf-8"))

    def read(self, path):
        with open(path, "rb") as fh:
            return fh.read()

    def run_lw(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = lw.main(list(argv))
            except SystemExit as e:
                code = e.code
        return code, out.getvalue(), err.getvalue()

    def add(self, *extra, **kw):
        args = {"--subject": "SampleTool", "--kind": "tool", "--date": "2026-11-18",
                "--depth": "light", "--relevance": "medium", "--outcome": "watch",
                "--session": "ABC-S12", "--finding": "ok"}
        keys = kw.pop("keys", ["url:https://github.com/sampletool/sampletool"])
        ledger = kw.pop("ledger", self.ledger)
        for k, v in kw.items():
            args["--" + k.rstrip("_").replace("_", "-")] = v
        argv = ["add", "--ledger", ledger, "--map", self.map, "--today", "2026-11-18"]
        for k, v in args.items():
            if v is not None:
                argv += [k, v]
        for k in keys:
            argv += ["--key", k]
        argv += list(extra)
        return self.run_lw(*argv)

    def assertRefused(self, res, text=None, path=None, before=None):
        code, out, err = res
        self.assertEqual(code, 1, "expected refusal; out=%r err=%r" % (out, err))
        self.assertIn("REFUSED", err)
        if text:
            self.assertIn(text, err)
        if path is not None:
            self.assertEqual(self.read(path), before, "file changed on a refusal")


class TestRefusals(Base):
    """One test per refusal in the ADD REFUSES list plus the grammar ones."""

    def setUp(self):
        Base.setUp(self)
        self.write(self.ledger, note_text())
        self.before = self.read(self.ledger)

    def refused(self, res, text=None):
        self.assertRefused(res, text, self.ledger, self.before)

    def test_word_outside_lists(self):
        for opt, bad in (("kind", "repo"), ("depth", "Deep"), ("depth", "sweep"),
                         ("relevance", "Very High"), ("outcome", "try")):
            with self.subTest(opt=opt, bad=bad):
                self.refused(self.add(**{opt: bad}), "is not one of")

    def test_key_no_scheme(self):
        self.refused(self.add(keys=["github.com/x/y"]), "no scheme")

    def test_key_unknown_scheme(self):
        self.refused(self.add(keys=["slug:sampletool"]), "unknown scheme")

    def test_key_value_with_semicolon_space(self):
        self.refused(self.add(keys=["name:a; b"]), "%3B")

    def test_key_value_with_raw(self):
        self.refused(self.add(keys=["name:a raw:b"]), "raw:")

    def test_date_not_iso(self):
        for bad in ("18.11.2026", "2026-11-1", "2026-02-30"):
            with self.subTest(bad=bad):
                self.refused(self.add(date=bad), "ISO")

    def test_for_lower_case(self):
        code, out, err = self.add(for_="al")
        self.refused((code, out, err), "upper case")
        self.assertNotIn("=al", err)

    def test_for_not_in_map(self):
        self.refused(self.add(for_="ZZ"), "not in holon_lens_map")

    def test_flag_not_in_map(self):
        self.write(self.ledger, note_text(abbr="QQ"))
        self.before = self.read(self.ledger)
        self.refused(self.add(), "not in holon_lens_map")

    def test_note_without_flag(self):
        self.write(self.ledger, note_text(flag=False))
        self.before = self.read(self.ledger)
        self.refused(self.add(), "no look_ledger")

    def test_row_without_twelve_cells(self):
        self.write(self.ledger, note_text(rows=["| a | b | c |"]))
        self.before = self.read(self.ledger)
        self.refused(self.add(), "not 12")

    def test_duplicate_id_in_note(self):
        self.assertEqual(self.add()[0], 0)
        self.before = self.read(self.ledger)
        self.refused(self.add(), "already in")

    def test_newline_in_cell(self):
        self.refused(self.add(finding="line one\nline two"), "line break")

    def test_tab_in_cell(self):
        self.refused(self.add(subject="a\tb"), "line break, tab")

    def test_lone_trailing_backslash(self):
        self.refused(self.add(finding="ends in \\"), "lone backslash")

    def test_pre_escaped_pipe_input(self):
        self.refused(self.add(finding="a \\| b"), "plain pipe")

    def test_changed_on_disk(self):
        real = lw.backup_once

        def sneaky(path, data, today, always):
            r = real(path, data, today, always)
            with open(path, "ab") as fh:
                fh.write(b"other writer\n")
            return r
        with mock.patch.object(lw, "backup_once", sneaky):
            res = self.add()
        code, out, err = res
        self.assertEqual(code, 1)
        self.assertIn("changed on disk", err)
        self.assertEqual(self.read(self.ledger), self.before + b"other writer\n")

    def test_add_only_appends_and_verify_failed(self):
        # an append never changes an old byte
        self.assertEqual(self.add()[0], 0)
        after = self.read(self.ledger)
        self.assertTrue(after.startswith(self.before))
        self.assertEqual(after.count(b"\n") - self.before.count(b"\n"), 1)
        # a read-back that differs is VERIFY FAILED, exit 3
        real = lw.read_bytes
        calls = {"n": 0}

        def bad_read(path):
            data = real(path)
            if path != self.ledger:
                return data
            calls["n"] += 1
            return data + b"x" if calls["n"] >= 4 else data   # 4th read = read-back
        with mock.patch.object(lw, "read_bytes", bad_read):
            code, out, err = self.add(subject="Other")
        self.assertEqual(code, 3)
        self.assertIn("VERIFY FAILED", err)
        self.assertIn("backup:", err)

    def test_frozen_note(self):
        self.write(self.ledger, note_text(frozen=True))
        self.before = self.read(self.ledger)
        self.refused(self.add(), "frozen")

    def test_map_without_row(self):
        with open(self.map, "w") as fh:
            fh.write("| Key | Value |\n|---|---|\n| board_dir | `x` |\n")
        self.refused(self.add(), "<folder>/=<ABBR>")

    # grammar refusals (G)
    def test_for_own_abbreviation(self):
        self.refused(self.add(for_="AL"), "leave For empty")

    def test_queued_without_trigger(self):
        self.refused(self.add(outcome="queued"), "Trigger is required")

    def test_trigger_without_queued(self):
        self.refused(self.add(trigger="when x"), "Trigger must be empty")

    def test_date_in_other_year(self):
        self.refused(self.add(date="2025-12-31"), "not in the note's year")

    def test_view_note_not_one_wikilink(self):
        for bad in ("Note", "[[A]]; [[B]]", "[[A]] [[B]]"):
            with self.subTest(bad=bad):
                self.refused(self.add(view_note=bad), "one wikilink")

    def test_bad_session(self):
        for bad in ("ABC S12", "ABC-S12;x", "Operator One", "abc-s12", "S12", "ABC-S", "Unlogged",
                    "DE_2026-01-15_OP_1", "DE_2026-1-15_OP_01", "DE_2026-01-15_op_01"):
            with self.subTest(bad=bad):
                self.refused(self.add(session=bad, subject="S " + bad), "session id")
        for good in ("ABC-S12", "GA_2026-11-04_OP_04", "unlogged", "AL-S120"):
            with self.subTest(good=good):
                self.assertEqual(self.add(session=good, subject="G " + good)[0], 0)

    def test_bad_from(self):
        for bad in ("folder/file#3", "file.md#3", "file#0", "research_items#x"):
            with self.subTest(bad=bad):
                self.refused(self.add("--from", bad), "from pointer")

    def test_same_key_twice(self):
        self.refused(self.add(keys=["url:https://www.github.com/a/b/",
                                    "url:http://github.com/a/b"]), "twice")

    def test_space_in_url(self):
        self.refused(self.add(keys=["url:https://x.com/a b"]), "%20")

    def test_url_without_scheme(self):
        self.refused(self.add(keys=["url:x.com/a"]), "http://")

    def test_empty_name_slug(self):
        self.refused(self.add(keys=["name:(only brackets)"]), "empty after")

    def test_bad_repo_and_core(self):
        self.refused(self.add(keys=["repo:sampletool/sampletool"]), "github-repo~")
        self.refused(self.add(keys=["core:Has Space"]), "core_id")

    def test_text_after_table(self):
        self.write(self.ledger, note_text(extra_after="\nA note after.\n"))
        self.before = self.read(self.ledger)
        self.refused(self.add(), "after the table")

    def test_two_tables(self):
        self.write(self.ledger, note_text() + "\n" + HEADER + "\n" + SEP + "\n")
        self.before = self.read(self.ledger)
        self.refused(self.add(), "exactly one table")

    def test_from_pointer_checked_with_vault(self):
        vault = os.path.join(self.d, "vault")
        led = os.path.join(vault, "_Alpha", "S", "4.0 Looks 2026 - AL Research Tracking Index.md")
        self.write(led, note_text())
        self.write(os.path.join(vault, "_Alpha", "S", "1.0 Evaluated.md"), "x\n")
        before = self.read(led)
        res = self.add("--from", "Missing File#3", "--vault", vault, ledger=led)
        self.assertRefused(res, "not found", led, before)
        code, out, err = self.add("--from", "1.0 Evaluated#3", "--vault", vault, ledger=led)
        self.assertEqual(code, 0, err)
        code, out, err = self.add("--from", "Missing File#4", ledger=led, subject="B")
        self.assertEqual(code, 0, err)
        self.assertIn("WARNING", err)


class TestMore(Base):
    """Cases added from a review update."""

    def setUp(self):
        Base.setUp(self)
        self.write(self.ledger, note_text())

    def test_backslash_before_pipe_anywhere_in_check(self):
        bad = lw.render_row(["A", "tool", "name:a", "2026-11-18", "light", "low", "", "pass", "",
                             "x", "", "ABC-S12"]).replace("| x |", "| a \\\\| b |")
        self.write(self.ledger, note_text(rows=[bad]))
        code, out, err = self.run_lw("check", "--ledger", self.ledger)
        self.assertEqual(code, 1)
        self.assertIn("backslash right before a pipe", out)
        self.assertRefused(self.add(model="a\\|b"), "backslash right before a pipe")

    def test_table_not_under_heading(self):
        text = note_text().replace("## Looks 2026\n\n" + HEADER + "\n" + SEP + "\n",
                                   HEADER + "\n" + SEP + "\n\n## Looks 2026\n")
        text = text.rstrip("\n").rsplit("\n", 1)[0] + "\n" + HEADER + "\n" + SEP + "\n"
        # two tables now: one above the heading, one below
        self.write(self.ledger, text)
        code, out, err = self.run_lw("check", "--ledger", self.ledger)
        self.assertEqual(code, 1)
        lone = note_text().replace("## Looks 2026\n\n", "") + "\n## Looks 2026\n"
        self.write(self.ledger, lone)
        before = self.read(self.ledger)
        self.assertRefused(self.add(), None, self.ledger, before)
        code, out, err = self.run_lw("check", "--ledger", self.ledger)
        self.assertEqual(code, 1)

    def test_blank_line_after_last_row(self):
        self.write(self.ledger, note_text(rows=[row(subject="Old")]) + "\n")
        before = self.read(self.ledger)
        self.assertRefused(self.add(), "after the table", self.ledger, before)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 1)

    def test_from_file_name_shared_by_two_files(self):
        vault = os.path.join(self.d, "vault")
        led = os.path.join(vault, "_Alpha", "S", "4.0 Looks 2026 - AL Research Tracking Index.md")
        self.write(led, note_text())
        self.write(os.path.join(vault, "_Alpha", "S", "Research Tracking Index.md"), "x\n")
        self.write(os.path.join(vault, "_Alpha", "W", "Research Tracking Index.md"), "y\n")
        before = self.read(led)
        self.assertRefused(self.add("--from", "Research Tracking Index#2", "--vault", vault,
                                    ledger=led), "ambiguous", led, before)

    def test_find_turns_space_into_pct20(self):
        self.assertEqual(self.add(keys=["url:https://x.com/a%20b"])[0], 0)
        code, out, err = self.run_lw("find", "--vault", self.d, "--url", "https://x.com/a b",
                                     "--json")
        self.assertEqual(len(json.loads(out)["lines"]), 1)

    def test_skipped_folder_warning(self):
        led = os.path.join(self.d, "_Archive - Alpha", "4.0 Looks 2026 - AL Research Tracking Index.md")
        self.write(led, note_text())
        code, out, err = self.add(ledger=led)
        self.assertEqual(code, 0, err)
        self.assertIn("skipped folder", err)
        self.assertTrue(lw.skipped_path(led))
        self.assertFalse(lw.skipped_path(self.ledger))
        for name, want in (("xArchive - Gamma", True), ("_to_delete", True),
                           ("Archive", True), ("Rendered", True), (".obsidian", True),
                           ("Archives of X", False), ("Research", False)):
            self.assertEqual(lw.skip_dir(name), want, name)

    def test_dry_run_still_checks_changed_on_disk(self):
        real = lw.read_bytes
        calls = {"n": 0}

        def moving(path):
            calls["n"] += 1
            d = real(path)
            return d + b"z" if (calls["n"] >= 2 and path == self.ledger) else d
        with mock.patch.object(lw, "read_bytes", moving):
            res = self.add("--dry-run")
        self.assertEqual(res[0], 1)
        self.assertIn("changed on disk", res[2])


class TestSize(Base):
    def make(self, size):
        base = note_text()
        pad = size - len(base.encode("utf-8"))
        rows = []
        i = 0
        while pad > 0:
            r = row(subject="pad%d" % i, finding="x")
            if len(r) + 1 > pad:
                break
            rows.append(r)
            pad -= len(r) + 1
            i += 1
        text = note_text(rows=rows)
        # fill the rest into the last row's Finding
        short = size - len(text.encode("utf-8"))
        rows[-1] = row(subject="pad%d" % (i - 1), finding="x" + "y" * short)
        text = note_text(rows=rows)
        self.assertEqual(len(text.encode("utf-8")), size)
        self.write(self.ledger, text)

    def test_40959_accepted(self):
        self.make(40959)
        code, out, err = self.add()
        self.assertEqual(code, 0, err)

    def test_40960_refused(self):
        self.make(40960)
        before = self.read(self.ledger)
        code, out, err = self.add()
        self.assertEqual(code, 4, err)
        self.assertIn("40,960", err)
        self.assertEqual(self.read(self.ledger), before)


class TestWrites(Base):
    def setUp(self):
        Base.setUp(self)
        self.write(self.ledger, note_text())

    def test_pipes_and_alias_round_trip(self):
        code, out, err = self.add(subject="A|B tool", finding="x | y",
                                  view_note="[[SampleTool - Review Note|eval]]",
                                  keys=["url:https://example.com/a|b"])
        self.assertEqual(code, 0, err)
        data = self.read(self.ledger).decode("utf-8")
        self.assertIn("| A\\|B tool |", data)
        self.assertIn("[[SampleTool - Review Note\\|eval]]", data)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger, "--map", self.map)[0], 0)
        code, out, err = self.run_lw("find", "--vault", self.d, "--all", "--json")
        rec = json.loads(out)["lines"][0]
        self.assertEqual(rec["subject"], "A|B tool")
        self.assertEqual(rec["view_note"], "[[SampleTool - Review Note|eval]]")
        self.assertEqual(rec["keys"][0]["value"], "example.com/a|b")

    def test_two_adds_keep_order(self):
        self.assertEqual(self.add(subject="First")[0], 0)
        self.assertEqual(self.add(subject="Second")[0], 0)
        lines = self.read(self.ledger).decode("utf-8").split("\n")
        self.assertTrue(lines[-3].startswith("| First "))
        self.assertTrue(lines[-2].startswith("| Second "))
        self.assertEqual(lines[-1], "")

    def test_output_form(self):
        self.assertEqual(self.add()[0], 0)
        last = self.read(self.ledger).decode("utf-8").split("\n")[-2]
        self.assertEqual(last, "| SampleTool | tool | url:github.com/sampletool/sampletool | 2026-11-18 "
                               "| light | medium || watch || ok || ABC-S12 |")

    def test_crlf_file(self):
        self.write(self.ledger, note_text(eol="\r\n"))
        before = self.read(self.ledger)
        self.assertEqual(self.add()[0], 0)
        after = self.read(self.ledger)
        self.assertTrue(after.startswith(before))
        new = after[len(before):]
        self.assertTrue(new.endswith(b"\r\n"))
        self.assertEqual(new.count(b"\n"), 1)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 0)

    def test_missing_trailing_newline_dry_run_wording(self):
        self.write(self.ledger, note_text(rows=[row(subject="Old")], final_eol=False))
        before = self.read(self.ledger)
        code, out, err = self.add("--dry-run")
        self.assertEqual(code, 0, err)
        self.assertIn("would be added", out)
        self.assertNotIn("was added", out)
        self.assertEqual(self.read(self.ledger), before)

    def test_missing_trailing_newline(self):
        self.write(self.ledger, note_text(rows=[row(subject="Old")], final_eol=False))
        before = self.read(self.ledger)
        code, out, err = self.add()
        self.assertEqual(code, 0, err)
        self.assertIn("no final line ending", out)
        after = self.read(self.ledger)
        self.assertEqual(after[:len(before)], before)
        self.assertEqual(after[len(before):len(before) + 1], b"\n")
        self.assertTrue(after.endswith(b"|\n"))

    def test_non_ascii_subject(self):
        code, out, err = self.add(subject="\u00d6kosystem caf\u00e9 \u2013 \u65e5\u672c",
                                  keys=["name:\u00d6kosystem caf\u00e9"])
        self.assertEqual(code, 0, err)
        data = self.read(self.ledger)
        self.assertIn("\u00d6kosystem caf\u00e9 \u2013 \u65e5\u672c".encode("utf-8"), data)
        self.assertIn(b"name:okosystem-cafe", data)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 0)

    def test_id_survives_repadding(self):
        v = ["A", "tool", "name:a", "2026-11-18", "light", "low", "", "pass", "", "x \\| y", "",
             "ABC-S12"]
        tight = "|" + "|".join(v) + "|"
        loose = "|  " + "   |  ".join(v) + "  |"
        a = lw.line_id(lw.cell_values(lw.split_cells(tight)))
        b = lw.line_id(lw.cell_values(lw.split_cells(loose)))
        self.assertEqual(a, b)
        self.assertRegex(a, r"^[0-9a-f]{10}$")
        # a hand re-padded copy in the note still blocks the same line
        w = ["SampleTool", "tool", "url:github.com/sampletool/sampletool", "2026-11-18", "light", "low",
             "", "pass", "", "ok", "", "ABC-S12"]
        self.write(self.ledger, note_text(rows=["|  " + "   |  ".join(w) + "  |"]))
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 0)
        before = self.read(self.ledger)
        self.assertRefused(self.add(relevance="low", outcome="pass"), "already in",
                           self.ledger, before)

    def test_key_order_and_raw_rule(self):
        code, out, err = self.add(keys=["name:Sample Tool", "url:https://WWW.GitHub.com/SampleTool/x/",
                                        "url:https://sampletool.app", "core:sampletool",
                                        "repo:GitHub-Repo~SampleTool/X.git", "host:www.SampleTool.app:443"])
        self.assertEqual(code, 0, err)
        last = self.read(self.ledger).decode("utf-8").split("\n")[-2]
        self.assertIn("| core:sampletool; repo:github-repo~sampletool/x; "
                      "url:github.com/SampleTool/x raw:https://WWW.GitHub.com/SampleTool/x/; "
                      "url:sampletool.app; host:sampletool.app; name:sample-tool |", last)

    def test_trailing_slash_kept_with_query_or_fragment(self):
        cases = (("https://a.com/?q=1/", "a.com/?q=1/"), ("https://a.com/p/#x/", "a.com/p/#x/"),
                 ("https://www.a.com/p/?", "a.com/p/?"), ("https://a.com/p//", "a.com/p"),
                 ("https://A.com/", "a.com"))
        for raw, want in cases:
            with self.subTest(raw=raw):
                self.assertEqual(lw.build_key("url:" + raw)[1], want)
        self.assertEqual(self.add(keys=["url:https://a.com/?q=1/"])[0], 0)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 0)
        code, out, err = self.run_lw("find", "--vault", self.d, "--url", "a.com/?q=1/", "--json")
        self.assertEqual(len(json.loads(out)["lines"]), 1)
        code, out, err = self.run_lw("find", "--vault", self.d, "--url", "a.com/?q=1", "--json")
        self.assertEqual(len(json.loads(out)["lines"]), 0)

    def test_multi_operator_session_and_by_order(self):
        code, out, err = self.add("--from", "research_items#12", "--from", "1.0 Evaluated#3",
                                  "--model", "opus", session="DE_2026-01-15_OP_01")
        self.assertEqual(code, 0, err)
        last = self.read(self.ledger).decode("utf-8").split("\n")[-2]
        self.assertIn("| DE_2026-01-15_OP_01; model=opus; from=1.0 Evaluated#3; "
                      "from=research_items#12 |", last)
        self.assertEqual(self.run_lw("check", "--ledger", self.ledger)[0], 0)

    def test_unlogged_and_queued(self):
        code, out, err = self.add(session="unlogged", outcome="queued", trigger="when v2 ships")
        self.assertEqual(code, 0, err)

    def test_dry_run_writes_nothing(self):
        before = self.read(self.ledger)
        code, out, err = self.add("--dry-run")
        self.assertEqual(code, 0, err)
        self.assertIn("DRY RUN", out)
        self.assertEqual(self.read(self.ledger), before)
        self.assertEqual(os.listdir(self.d).count(os.path.basename(self.ledger) +
                                                  ".pre-look-20261118.bak"), 0)

    def test_backup_once_per_day(self):
        before = self.read(self.ledger)
        self.assertEqual(self.add(subject="One")[0], 0)
        bak = self.ledger + ".pre-look-20261118.bak"
        self.assertEqual(self.read(bak), before)
        self.assertEqual(self.add(subject="Two")[0], 0)
        self.assertEqual(self.read(bak), before)


class TestCheck(Base):
    def test_wide_table_with_ten_escaped_pipes(self):
        rows = []
        for i in range(10):
            rows.append("| Tool %d | tool | url:github.com/o/t%d | 2026-11-%02d | moderate | high || adopt "
                        "|| Learn-only. See [[T%d - Review Note\\|eval %d]] |"
                        " [[T%d - Review Note\\|T%d]] | AL-S1%02d; from=1.0 Evaluated - AL Research "
                        "Tracking Index#%d |" % (i, i, i + 1, i, i, i, i, i, i + 1))
        self.write(self.ledger, note_text(rows=rows))
        code, out, err = self.run_lw("check", "--ledger", self.ledger, "--map", self.map)
        self.assertEqual(code, 0, out + err)
        self.assertEqual(out.count("\trow "), 10)
        self.assertEqual(sum(r.count("\\|") for r in rows), 20)

    def test_check_reports_bad_rows_and_changes_nothing(self):
        rows = [row(depth="Deep"), row(subject="B", key="url:https://github.com/x"),
                "| a | b |", row(subject="C", key="name:c; core:c")]
        self.write(self.ledger, note_text(rows=rows))
        before = self.read(self.ledger)
        code, out, err = self.run_lw("check", "--ledger", self.ledger)
        self.assertEqual(code, 1)
        self.assertIn("Depth 'Deep'", out)
        self.assertIn("not in normal form", out)
        self.assertIn("cells, not 12", out)
        self.assertIn("out of order", out)
        self.assertEqual(self.read(self.ledger), before)

    def test_check_json(self):
        self.write(self.ledger, note_text(rows=[row()]))
        code, out, err = self.run_lw("check", "--ledger", self.ledger, "--json")
        self.assertEqual(code, 0)
        j = json.loads(out)
        self.assertEqual(j["project"], "AL")
        self.assertEqual(len(j["lines"]), 1)


class TestFind(Base):
    def setUp(self):
        Base.setUp(self)
        self.vault = os.path.join(self.d, "vault")
        a = os.path.join(self.vault, "_Alpha", "Sec", "4.0 Looks 2026 - AL Research Tracking Index.md")
        b = os.path.join(self.vault, "_Beta", "1.0 Looks 2026 - BE Research Tracking Index.md")
        arch = os.path.join(self.vault, "_Alpha", "_Archive - Alpha", "old.md")
        xarch = os.path.join(self.vault, "xArchive - Gamma", "old.md")
        self.write(a, note_text(rows=[
            row(subject="SampleTool", key="url:github.com/sampletool/sampletool"),
            row(subject="Piped", key="url:example.com/a|b raw:http://www.Example.com/a|b/"),
            row(subject="Other", key="name:other-thing")]))
        self.write(b, note_text(abbr="BE", rows=[
            row(subject="Sample Tool", key="url:github.com/sampletool/sampletool; name:sample-tool",
                for_="AL")]))
        self.write(arch, note_text(rows=[row(subject="Archived", key="url:github.com/sampletool/sampletool")]))
        self.write(xarch, note_text(rows=[row(subject="X", key="url:github.com/sampletool/sampletool")]))
        self.write(a + ".pre-look-20261118.bak", note_text(rows=[row(subject="Bak")]))
        self.write(os.path.join(self.vault, "_Alpha", "Notes.bak review.md"),
                   note_text(rows=[row(subject="BakInName", key="name:bak-in-name")]))
        self.write(os.path.join(self.vault, "plain.md"),
                   "no flag\n\n" + HEADER + "\n" + SEP + "\n" + row() + "\n")

    def snapshot(self):
        snap = {}
        for r, ds, fs in os.walk(self.vault):
            for f in fs:
                p = os.path.join(r, f)
                snap[p] = self.read(p)
        return snap

    def test_url_matches_across_forms_and_writes_nothing(self):
        before = self.snapshot()
        for q in ("https://www.github.com/sampletool/sampletool/", "http://GITHUB.com/sampletool/sampletool",
                  "github.com/sampletool/sampletool"):
            with self.subTest(q=q):
                code, out, err = self.run_lw("find", "--vault", self.vault, "--url", q, "--json")
                self.assertEqual(code, 0, err)
                got = sorted((o["project"], o["subject"]) for o in json.loads(out)["lines"])
                self.assertEqual(got, [("AL", "SampleTool"), ("BE", "Sample Tool")])
        code, out, err = self.run_lw("find", "--vault", self.vault, "--url",
                                     "https://www.example.com/a\\|b/", "--json")
        self.assertEqual([o["subject"] for o in json.loads(out)["lines"]], ["Piped"])
        self.assertEqual(self.snapshot(), before)

    def test_archive_skipped(self):
        code, out, err = self.run_lw("find", "--vault", self.vault, "--all", "--json")
        subjects = [o["subject"] for o in json.loads(out)["lines"]]
        self.assertNotIn("Archived", subjects)
        self.assertNotIn("X", subjects)
        self.assertNotIn("Bak", subjects)
        self.assertIn("BakInName", subjects)   # ".bak" inside a name is not a backup
        self.assertEqual(len(subjects), 5)

    def test_name_match(self):
        code, out, err = self.run_lw("find", "--vault", self.vault, "--name", "The Sample Tool")
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().split("\n")), 1)
        self.assertIn("Sample Tool", out)
        code, out, err = self.run_lw("find", "--vault", self.vault, "--name", "OTHER thing", "--json")
        self.assertEqual([o["subject"] for o in json.loads(out)["lines"]], ["Other"])

    def test_all_json_same_lines_as_url_form(self):
        before = self.snapshot()
        code, out, err = self.run_lw("find", "--vault", self.vault, "--all", "--json")
        top = json.loads(out)
        self.assertEqual(top["version"], lw.VERSION)
        allj = top["lines"]
        code, out, err = self.run_lw("find", "--vault", self.vault, "--url",
                                     "github.com/sampletool/sampletool", "--json")
        urlj = json.loads(out)["lines"]
        sub = [o for o in allj if any(k["value"] == "github.com/sampletool/sampletool" for k in o["keys"])]
        self.assertEqual(sub, urlj)
        for o in allj:
            self.assertEqual(o["id"], lw.line_id([o[f] for f in lw.FIELDS]))
            for f in ("id", "project", "ledger", "row", "line", "keys") + tuple(lw.FIELDS):
                self.assertIn(f, o)
        self.assertEqual(self.snapshot(), before)


class TestConfirm(Base):
    def setUp(self):
        Base.setUp(self)
        self.write(self.ledger, note_text(rows=[
            row(subject="One", key="url:github.com/a/b"),
            row(subject="Two", key="url:github.com/c/d; name:two")]))
        n = lw.parse_note(self.read(self.ledger).decode("utf-8"))
        self.ids = [lw.line_id(lw.cell_values(r["cells"])) for r in n["tables"][0]["rows"]]
        self.note = os.path.join(self.d, "Look Confirmations 2026 - Alpha.md")

    def confirm(self, *extra):
        return self.run_lw("confirm", "--note", self.note, "--by", "Operator One", "--today",
                           "2026-11-18", "--session", "ABC-S12", *extra)

    def test_create_and_append_never_edit(self):
        code, out, err = self.confirm("--line", self.ids[0], "--what", "key", "--ledger",
                                      self.ledger, "--core", "ab-core", "--create")
        self.assertEqual(code, 0, err)
        first = self.read(self.note)
        self.assertIn(("| %s | key | url:github.com/a/b | ab-core | 2026-11-18 | Operator One |"
                       % self.ids[0]).encode(), first)
        code, out, err = self.confirm("--line", self.ids[1], "--what", "outcome")
        self.assertEqual(code, 0, err)
        second = self.read(self.note)
        self.assertTrue(second.startswith(first))
        self.assertEqual(second[len(first):].count(b"\n"), 1)
        self.assertIn(b"never MCP", second.replace(b"Never edit by MCP", b"never MCP"))

    def test_missing_note_needs_create(self):
        self.assertRefused(self.confirm("--line", self.ids[0], "--what", "depth"), "--create")
        self.assertFalse(os.path.exists(self.note))

    def test_unknown_id_refused(self):
        self.confirm("--line", self.ids[0], "--what", "depth", "--create")
        before = self.read(self.note)
        self.assertRefused(self.confirm("--line", "0123456789", "--what", "depth", "--ledger",
                                        self.ledger), "not in", self.note, before)
        self.assertRefused(self.confirm("--line", "XYZ", "--what", "depth"), "line id",
                           self.note, before)

    def test_key_required_for_two_keys(self):
        self.confirm("--line", self.ids[0], "--what", "depth", "--create")
        before = self.read(self.note)
        self.assertRefused(self.confirm("--line", self.ids[1], "--what", "key", "--ledger",
                                        self.ledger), "--key", self.note, before)
        self.assertRefused(self.confirm("--line", self.ids[1], "--what", "key", "--ledger",
                                        self.ledger, "--key", "name:three"), "not a key",
                           self.note, before)
        self.assertRefused(self.confirm("--line", self.ids[1], "--what", "key"), "--key",
                           self.note, before)
        self.assertRefused(self.confirm("--line", self.ids[1], "--what", "depth", "--key",
                                        "name:two"), "only with --what key", self.note, before)
        code, out, err = self.confirm("--line", self.ids[1], "--what", "key", "--ledger",
                                      self.ledger, "--key", "name:Two")
        self.assertEqual(code, 0, err)

    def test_dry_run(self):
        code, out, err = self.confirm("--line", self.ids[0], "--what", "depth", "--create",
                                      "--dry-run")
        self.assertEqual(code, 0)
        self.assertFalse(os.path.exists(self.note))


class TestInit(Base):
    def setUp(self):
        Base.setUp(self)
        self.sec = os.path.join(self.d, "_Sections", "Research Tracking Index - Alpha")
        os.makedirs(self.sec)
        for f in ("1.0 Evaluated - AL Research Tracking Index.md",
                  "3.0 Queued for Review - AL Research Tracking Index.md"):
            self.write(os.path.join(self.sec, f), "---\ntype: project-doc\n---\n\nold\n")
        self.shell = os.path.join(self.d, "_Alpha", "! Research Tracking Index.md")
        self.write(self.shell, "---\ntitle: RTI\n---\n\n# RTI\n\n"
                   "<!-- grow: group=1 target=\"1.0 Evaluated - AL Research Tracking Index\" "
                   "insert=after soft=30 -->\n![[1.0 Evaluated - AL Research Tracking Index]]\n\n"
                   "![[3.0 Queued for Review - AL Research Tracking Index]]\n")

    def init(self, *extra, **kw):
        return self.run_lw("init", "--sections", self.sec, "--shell", kw.get("shell", self.shell),
                           "--abbr", "AL", "--year", kw.get("year", "2026"), "--map", self.map,
                           "--session", "ABC-S12", "--operator", "Operator One", "--today", "2026-11-18",
                           *extra)

    def test_first_part_then_refused_then_part_two(self):
        shell0 = self.read(self.shell)
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        p = os.path.join(self.sec, "4.0 Looks 2026 - AL Research Tracking Index.md")
        self.assertIn(p, out)
        text = self.read(p).decode("utf-8")
        for s in ("look_ledger: AL", "section: '4.0'", "## Looks 2026", HEADER, SEP,
                  "*Part of the [[! Research Tracking Index]]*", "created: 2026-11-18"):
            self.assertIn(s, text)
        shell1 = self.read(self.shell)
        self.assertEqual(shell1, shell0 + b"\n<!-- grow: group=4 target=\"4.0 Looks 2026 - AL Research "
                         b"Tracking Index\" insert=after soft=40 -->\n![[4.0 Looks 2026 - AL Research "
                         b"Tracking Index]]\n")
        # check on the new empty note passes; add works
        self.assertEqual(self.run_lw("check", "--ledger", p, "--map", self.map)[0], 0)
        self.assertEqual(self.add(ledger=p)[0], 0)
        # init again while the newest part is under 40 KB: refused, nothing written
        self.assertRefused(self.init(), "under 40 KB", self.shell, self.read(self.shell))
        # grow the part to 40 KB and start part 2
        with open(p, "ab") as fh:
            while os.path.getsize(p) < lw.SIZE_LIMIT:
                fh.write(b"| pad | tool | name:pad || light | low || pass |||| ABC-S12 |\n")
        shell2 = self.read(self.shell)
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        p2 = os.path.join(self.sec, "4.1 Looks 2026 - Part 2 - AL Research Tracking Index.md")
        t2 = self.read(p2).decode("utf-8")
        self.assertIn("*Continuation of [[4.0 Looks 2026 - AL Research Tracking Index]]*", t2)
        self.assertIn("section: '4.1'", t2)
        s3 = self.read(self.shell).decode("utf-8")
        self.assertIn("![[4.0 Looks 2026 - AL Research Tracking Index]]\n\n"
                      "![[4.1 Looks 2026 - Part 2 - AL Research Tracking Index]]\n", s3)
        self.assertIn('group=4 target="4.1 Looks 2026 - Part 2 - AL Research Tracking Index"', s3)
        self.assertIn('group=1 target="1.0 Evaluated - AL Research Tracking Index"', s3)
        self.assertEqual(self.read(self.shell + ".pre-look-20261118.bak"), shell0)
        self.assertEqual(self.read(self.shell + ".pre-look-20261118-2.bak"), shell2)

    def test_init_when_newest_part_is_40960_bytes(self):
        self.assertEqual(self.init()[0], 0)
        p = os.path.join(self.sec, "4.0 Looks 2026 - AL Research Tracking Index.md")
        with open(p, "ab") as fh:
            fh.write(b"x" * (lw.SIZE_LIMIT - os.path.getsize(p)))
        self.assertEqual(os.path.getsize(p), 40960)
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        self.assertIn("4.1 Looks 2026 - Part 2", out)

    def test_init_newest_part_40959_refused(self):
        self.assertEqual(self.init()[0], 0)
        p = os.path.join(self.sec, "4.0 Looks 2026 - AL Research Tracking Index.md")
        with open(p, "ab") as fh:
            fh.write(b"x" * (lw.SIZE_LIMIT - 1 - os.path.getsize(p)))
        self.assertRefused(self.init(), "under 40 KB", self.shell, self.read(self.shell))

    def test_init_existing_year_refused(self):
        self.assertEqual(self.init()[0], 0)
        before = self.read(self.shell)
        self.assertRefused(self.init(), "under 40 KB", self.shell, before)
        self.assertEqual(len([f for f in os.listdir(self.sec) if f.endswith(".md")]), 3)

    def test_new_year_next_number_and_crlf_shell(self):
        self.write(self.shell, self.read(self.shell).replace(b"\n", b"\r\n"), binary=True)
        self.assertEqual(self.init()[0], 0)
        code, out, err = self.init(year="2027")
        self.assertEqual(code, 0, err)
        self.assertTrue(os.path.exists(os.path.join(
            self.sec, "5.0 Looks 2027 - AL Research Tracking Index.md")))
        s = self.read(self.shell)
        self.assertNotIn(b"\n", s.replace(b"\r\n", b""))
        self.assertIn(b"<!-- grow: group=5 ", s)

    def test_part_numbers_past_nine_and_missing_grow_line(self):
        for m in range(0, 10):
            name = ("4.0 Looks 2026 - AL Research Tracking Index" if m == 0 else
                    "4.%d Looks 2026 - Part %d - AL Research Tracking Index" % (m, m + 1))
            body = note_text() + ("x" * (lw.SIZE_LIMIT if m == 9 else 10))
            self.write(os.path.join(self.sec, name + ".md"), body)
        self.write(self.shell, "# shell\n\n![[4.9 Looks 2026 - Part 10 - AL Research Tracking Index]]")
        code, out, err = self.init()
        self.assertEqual(code, 0, err)
        self.assertTrue(os.path.exists(os.path.join(
            self.sec, "4.10 Looks 2026 - Part 11 - AL Research Tracking Index.md")))
        s = self.read(self.shell).decode("utf-8")
        self.assertIn("no grow line", out)
        self.assertEqual(s, "# shell\n\n<!-- grow: group=4 target=\"4.10 Looks 2026 - Part 11 - AL "
                            "Research Tracking Index\" insert=after soft=40 -->\n![[4.9 Looks 2026 - "
                            "Part 10 - AL Research Tracking Index]]\n\n![[4.10 Looks 2026 - Part 11 - "
                            "AL Research Tracking Index]]\n")

    def test_dry_run_wording_for_shell(self):
        self.write(self.shell, "# shell")   # no final line ending
        before = self.read(self.shell)
        code, out, err = self.init("--dry-run")
        self.assertEqual(code, 0, err)
        self.assertIn("would be added", out)
        self.assertNotIn("was added", out)
        self.assertEqual(self.read(self.shell), before)
        code, out, err = self.init()
        self.assertIn("was added", out)

    def test_dry_run_and_abbr_not_in_map(self):
        before = self.read(self.shell)
        code, out, err = self.init("--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(self.read(self.shell), before)
        self.assertEqual(len([f for f in os.listdir(self.sec)]), 2)
        res = self.run_lw("init", "--sections", self.sec, "--shell", self.shell, "--abbr", "QQ",
                          "--year", "2026", "--map", self.map, "--session", "ABC-S12",
                          "--operator", "Operator One")
        self.assertRefused(res, "holon_lens_map", self.shell, before)

    def test_frozen_shell_still_takes_embed(self):
        self.write(self.shell, "---\nx: 1\n---\n*Frozen 2026-11-18 (D183): old rows kept.*\n")
        code, out, err = self.init()
        self.assertEqual(code, 0, err)


if __name__ == "__main__":
    unittest.main()
