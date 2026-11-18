#!/usr/bin/env python3
"""
look_write.py - the look line writer (Conventions Registry 38.0).

created: 2026-11 (DataWizard)
edit_log:
  - Seed 1.15.0 2026-11-18 - 0.1.2 first Seed release; names made generic in comments
    and in three messages (session id and For examples, confirmations note header)

A look line is one row of a 12-cell markdown table in a ledger section note
that carries `look_ledger: <ABBR>` in its frontmatter. The grammar is the
Conventions Registry 38.0 grammar paragraph. This
script is the only writer of look lines. It appends; it never edits or
deletes an existing line.

Python 3 standard library only, 3.9 safe, ASCII source. Every path is an
argument; there is no vault-specific default. Run with `python3 -I -B`.

COMMANDS
  init    --sections DIR --shell PATH --abbr X --year YYYY --map PATH
          --session ID --operator NAME [--today D] [--dry-run]
      Makes the next section note of that year (`<n>.0 Looks <year> - <ABBR>
      Research Tracking Index.md`, then `<n>.1 Looks <year> - Part 2 - ...`)
      with birth metadata, `look_ledger`, the `## Looks <year>` heading and
      the header row, and adds its embed (and grow line) to the shell.
  add     --ledger PATH --map PATH --subject S --kind K --key SCHEME:VALUE
          [--key ...] --date D --depth W --relevance W [--for ABBR]
          --outcome W [--trigger T] [--finding F] [--view-note "[[X]]"]
          --session ID [--model M] [--from PTR [--from ...]] [--vault ROOT]
          [--today D] [--dry-run]
      Appends one line at the end of the note's table.
  check   --ledger PATH [--map PATH] [--json]
      Validates every table of the note and prints each line id. Read-only.
  find    --vault ROOT (--url U | --name N | --all) [--json]
      Read-only. Lists every look line in every flagged ledger under ROOT
      that matches.
  confirm --note PATH --line ID --what key|outcome|depth --by NAME
          [--key SCHEME:VALUE] [--core CORE_ID] [--ledger PATH]
          [--session ID] [--create] [--today D] [--dry-run]
      Appends one line to the confirmations note. Never edits a line.

Every writing command takes --dry-run: it prints what would change and
writes nothing (no backup either).

EXIT CODES  0 done; 1 refused (file unchanged); 2 usage error (argparse);
            3 VERIFY FAILED (the write happened but the read-back differs);
            4 refused because the note is 40 KB or more (run init for the
              next part, then add again).

WRITE SAFETY
  - Files are read and written as bytes. The file's own line ending (the
    first one found; LF if none) is used for new lines. Every old byte stays
    identical. If the file lacks a final line ending, one is added before the
    appended line and the output says so.
  - Backups (`<file>.pre-look-YYYYMMDD.bak`, created exclusively, never
    overwritten, byte-compared to the file): add and confirm write one
    before their first write to a file on a given day; init always backs up
    the shell before editing it (a second init that day gets `-2.bak`, ...).
    Backups are never deleted (`.bak` names are skipped by every reader).
    A VERIFY FAILED message names the backup.
  - Appends use open('ab'); init's shell edit rewrites the file in place
    (open 'wb'); no temp file and no rename (the vault mount may block
    delete and rename-over).
  - --dry-run runs the same code path, including the changed-on-disk check,
    and stops just before the backup and the write.
  - The file is read again just before the write; if its bytes changed, the
    write is refused.
  - After the write the file is read back: old bytes identical and the new
    line last (for the shell edit in init: the whole file equals the planned
    bytes). Otherwise VERIFY FAILED, exit 3.

ADD REFUSES (exit 1, file unchanged)
  a word outside the allowed word lists (lower case only); a key with no scheme or an
  unknown scheme; a key value with `; ` or ` raw:`; a space in a URL (write
  %20); a URL key without http:// or https://; a name/host that is empty
  after normalising; a bad repo or core value; the same key twice; a Date
  that is not ISO or not in the note's year; a For or flag value not in
  holon_lens_map, or For equal to the ledger's own abbreviation; a Trigger
  missing for `queued` or present for another Outcome; a View note that is
  not one wikilink; a bad session id, model or from= pointer; a cell with a
  line break, tab or other control character; a cell ending in a lone
  backslash; an input that already holds `\\|` (give the plain pipe, the
  writer escapes it); a note without `look_ledger`; a note with no
  `## Looks <year>` heading or more than one; a note with not exactly one
  table, a header that is not the 12 look columns, a row without 12 cells,
  or text (or a blank line) after the table; a frozen note (a line that
  starts with `*Frozen ` and contains `(D183)`); a note of 40,960 bytes or
  more on disk before the append (start the next part with init); a line id
  already in the note; a map file with no holon_lens_map row; a file that
  changed on disk between read and write. With --vault, a from= file pointer
  whose `<file>.md` is not found (search: the project's holon_lens_map folder
  and the ledger note's own folder, recursively, skip list applied); without
  --vault the pointer is not checked and a warning is printed.

INIT
  The year's parts are the .md notes directly in --sections whose
  frontmatter has `look_ledger: <ABBR>` and whose body has the heading
  `## Looks <year>`. The newest part is the one with the highest section
  number in its file name (`<n>.<m> ...`, compared as numbers, so 4.10 is
  after 4.9). No part yet: <n> is one more than the highest whole number
  that starts any .md file name in the folder (1 if none) and the note is
  `<n>.0`. Parts exist: refused while the newest part is under 40,960
  bytes; else the next free `<n>.<m+1>` (Part m+2). The shell gets, for a
  first part: a blank line, `<!-- grow: group=<n> target="<name>"
  insert=after soft=40 -->` and `![[<name>]]` at its end; for a later part:
  a blank line and `![[<name>]]` right below the previous part's embed, and
  the group's grow line target set to the new part (a grow line is added
  above the group's first embed when the shell has none for that group).
  init may write to a frozen shell. The section note is created first, then
  the shell is written.

FIND
  Walks ROOT, reads `.md` files only (so never a `.bak`), skips any folder whose
  name contains `xArchive` or `_to_delete`, starts with `_Archive`, is
  `Archive` or `Rendered`, or starts with `.` (case-insensitive; one skip
  list for every reader). A note counts only if its frontmatter
  has `look_ledger`. Every 12-cell look table row in it is a line.
  --url U: U is normalised as add does (pipes unescaped; no scheme means
  https://; a literal space becomes %20 here, where add refuses it); a line matches when one of its url keys has the same
  normalised value. --name N: N is slugged as add does; a line matches when
  one of its name keys equals the slug or the slug of its Subject does.
  Text output: one line per match, tab-separated:
      <id> <project> <ledger path>#<row> <subject> <key cell>
  --json output: one JSON object {"version": <look_write version>,
  "schema": 1, "lines": [...]}; "lines" holds one object per line, sorted
  by ledger path then row, with these fields (a caller can
  consume them):
      id          10 lower-case hex digits (the line id)
      project     the note's look_ledger value
      ledger      path of the note relative to ROOT, with `/`
      row         1-based data row number over every table in the file
      line        1-based line number in the file
      subject, kind, key, date, depth, relevance, for, outcome, trigger,
      finding, view_note, by
                  the 12 cell values, trimmed and unescaped
      keys        list of {"scheme", "value", "raw" (string or null),
                  "strong" (true for core and repo)}
  A row that is not 12 cells is skipped with a warning on stderr.

CONFIRMATIONS NOTE (written only by confirm)
  A markdown note whose last block is one table:
      | Line | What | Key | Core | Date | By |
  One row per confirmation: line id, what (key, outcome or depth), the
  normalised key (`scheme:value`, no raw part; empty unless what is key),
  the core_id (empty if none), the ISO date, the name. Cells use the same
  escaping as look lines. --create makes the note if it is missing (with
  birth metadata and a header line that says scripts write and read it,
  never MCP); without --create a missing note is refused. --key is required
  for --what key unless --ledger is given and the line has exactly one key;
  with --ledger the line id must exist in that ledger and --key must be one
  of its keys; without --ledger the id is not checked (the look index
  reports unknown ids). --key and --core are refused for outcome and depth.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import unicodedata
from urllib.parse import urlsplit

VERSION = "0.1.2"

COLS = ["Subject", "Kind", "Key", "Date", "Depth", "Relevance", "For",
        "Outcome", "Trigger", "Finding", "View note", "By"]
FIELDS = ["subject", "kind", "key", "date", "depth", "relevance", "for",
          "outcome", "trigger", "finding", "view_note", "by"]
CONF_COLS = ["Line", "What", "Key", "Core", "Date", "By"]

KINDS = ("tool", "org", "link", "work", "place", "question")
DEPTHS = ("listed", "light", "moderate", "deep", "tested", "not set")
RELEVANCES = ("high", "medium", "low", "none", "not set")
OUTCOMES = ("queued", "adopt", "test", "watch", "applied", "confirms",
            "reference", "pass", "duplicate", "superseded", "unavailable")
SCHEMES = ("core", "repo", "url", "host", "name")
STRONG = ("core", "repo")
SIZE_LIMIT = 40 * 1024

# Session id: a solo id ABBR-S<digits> (for example ABC-S12), a
# multi-operator id kept whole PROJ_YYYY-MM-DD_INITIALS_NN (session-closer
# skill, Session Identifier Format), or exactly `unlogged`.
SESSION_RE = re.compile(
    r"^(unlogged|[A-Z][A-Z0-9]*-S[0-9]+|[A-Z][A-Z0-9]*_[0-9]{4}-[0-9]{2}-[0-9]{2}_[A-Z]+_[0-9]{2})$")
ABBR_RE = re.compile(r"^[A-Z][A-Z0-9]{0,9}$")
CORE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
GITHUB_REPO_RE = re.compile(r"^github-repo~[a-z0-9_.-]+/[a-z0-9_.-]+$")
GIT_REPO_RE = re.compile(r"^git-repo~[a-z0-9.-]+(:[0-9]+)?/[a-z0-9_.-]+/[a-z0-9_.-]+$")
WIKILINK_RE = re.compile(r"^\[\[[^\[\]]+\]\]$")
FROM_DB_RE = re.compile(r"^(research_items|queued_items)#[0-9]+$")
FROM_FILE_RE = re.compile(r"^([^/\\#]+)#(h?)([1-9][0-9]*)$")
LINE_ID_RE = re.compile(r"^[0-9a-f]{10}$")
PART_RE = re.compile(r"^([0-9]+)\.([0-9]+) ")
CTRL_RE = re.compile(r"[\x00-\x1f\x7f]")


class Refused(Exception):
    pass


class VerifyFailed(Exception):
    pass


class TooBig(Refused):
    """The note is 40 KB or more: exit code 4, so a runner can start the next part."""
    pass


# ------------------------------------------------------------ key rules
# slugify and host_of: copied from the project's key-slug helper, so the
# writer needs no import; keep in sync with that helper.
def slugify(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"\([^)]*\)", " ", s).strip()
    if s.startswith("the "):
        s = s[4:]
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def host_of(url):
    """Return (host, path) - lowercase netloc, no www., no port."""
    u = (url or "").strip()
    if not u:
        return "", ""
    if "://" not in u:
        u = "http://" + u
    try:
        p = urlsplit(u)
        h = (p.hostname or "").lower()
    except ValueError:
        return "", ""
    if h.startswith("www."):
        h = h[4:]
    if h and any(ord(ch) > 127 for ch in h):
        try:
            h = h.encode("idna").decode("ascii")
        except UnicodeError:
            return "", p.path
    return h, p.path


def norm_url(u):
    """G S11: lowercase the host, drop www., drop a trailing / (all of them;
    not when the URL has a query string or fragment), drop the scheme.
    Returns None when u has no http:// or https:// scheme."""
    m = re.match(r"^(https?)://([^/?#]*)(.*)$", u, re.I | re.S)
    if not m:
        return None
    host = m.group(2).lower()
    if host.startswith("www."):
        host = host[4:]
    if not host:
        return None
    rest = m.group(3)
    if "?" in rest or "#" in rest:
        return host + rest      # keep a trailing / after a query or fragment
    return (host + rest).rstrip("/")


def build_key(spec):
    """Turn one SCHEME:VALUE input into (scheme, value, raw). Refuses."""
    if ":" not in spec:
        raise Refused("key %r has no scheme (use core:, repo:, url:, host: or name:)" % spec)
    scheme, value = spec.split(":", 1)
    if scheme not in SCHEMES:
        raise Refused("key %r has an unknown scheme %r (schemes: %s)"
                      % (spec, scheme, ", ".join(SCHEMES)))
    value = value.strip(" ")
    if "; " in value:
        raise Refused("key %r contains '; ' (write the ';' as %%3B)" % spec)
    if " raw:" in value:
        raise Refused("key %r contains ' raw:'" % spec)
    if CTRL_RE.search(value):
        raise Refused("key %r holds a line break, tab or control character" % spec)
    if "\\|" in value:
        raise Refused("key %r holds '\\|'; give the plain pipe, the writer escapes it" % spec)
    if scheme == "url":
        if re.search(r"\s", value):
            raise Refused("URL %r holds a space; write it as %%20" % value)
        n = norm_url(value)
        if n is None:
            raise Refused("URL key %r must start with http:// or https:// and name a host" % value)
        raw = value if value != "https://" + n else None
        return ("url", n, raw)
    if scheme == "host":
        if "/" in value or re.search(r"\s", value):
            raise Refused("host key %r must be a bare host name" % value)
        h, _ = host_of(value)
        if not h:
            raise Refused("host key %r is empty after normalising" % value)
        return ("host", h, None)
    if scheme == "name":
        s = slugify(value)
        if not s:
            raise Refused("name key %r is empty after slugging" % value)
        return ("name", s, None)
    if scheme == "repo":
        v = value.lower()
        if v.endswith(".git"):
            v = v[:-4]
        if not (GITHUB_REPO_RE.match(v) or GIT_REPO_RE.match(v)):
            raise Refused("repo key %r is neither github-repo~owner/repo nor "
                          "git-repo~host/owner/repo" % value)
        return ("repo", v, None)
    # core
    if not CORE_RE.match(value):
        raise Refused("core key %r is not a core_id (lower-case slug)" % value)
    return ("core", value, None)


def render_key(k):
    s = "%s:%s" % (k[0], k[1])
    if k[2]:
        s += " raw:" + k[2]
    return s


def build_key_cell(specs):
    keys = [build_key(s) for s in specs]
    if not keys:
        raise Refused("at least one --key is needed")
    seen = set()
    for k in keys:
        if (k[0], k[1]) in seen:
            raise Refused("key %s:%s is given twice" % (k[0], k[1]))
        seen.add((k[0], k[1]))
    keys.sort(key=lambda k: SCHEMES.index(k[0]))   # stable: given order kept
    return "; ".join(render_key(k) for k in keys), keys


def parse_key_cell(cell):
    """Parse a stored Key cell. Returns (keys, errors)."""
    keys, errs = [], []
    if not cell:
        return keys, ["Key is empty"]
    last = -1
    seen = set()
    for part in cell.split("; "):
        m = re.match(r"^([a-z]+):(.*)$", part, re.S)
        if not m:
            errs.append("key %r has no scheme" % part)
            continue
        scheme, val = m.group(1), m.group(2)
        if scheme not in SCHEMES:
            errs.append("key %r has an unknown scheme" % part)
            continue
        raw = None
        if scheme == "url" and " raw:" in val:
            val, raw = val.split(" raw:", 1)
        keys.append((scheme, val, raw))
        if scheme == "url" and re.match(r"^https?://", val, re.I):
            errs.append("key %r is not in normal form (a url value has no scheme)" % part)
            continue
        try:
            if scheme == "url":
                k = build_key("url:" + (raw if raw is not None else "https://" + val))
            else:
                k = build_key(part)
            if render_key(k) != part:
                errs.append("key %r is not in normal form (expected %r)" % (part, render_key(k)))
        except Refused as e:
            errs.append(str(e))
        idx = SCHEMES.index(scheme)
        if idx < last:
            errs.append("key %r is out of order (core, repo, url, host, name)" % part)
        last = max(last, idx)
        if (scheme, val) in seen:
            errs.append("key %s:%s appears twice" % (scheme, val))
        seen.add((scheme, val))
    return keys, errs


# ------------------------------------------------------------ By cell
def build_by(session, model, froms):
    if not SESSION_RE.match(session or ""):
        raise Refused("session id %r is not a session id: use ABBR-S<n> (for example ABC-S12), "
                      "PROJ_YYYY-MM-DD_INITIALS_NN (for example ABC_2026-01-15_OP_01), or unlogged" % session)
    parts = [session]
    if model is not None:
        if not model.strip() or "; " in model or CTRL_RE.search(model):
            raise Refused("model %r is empty or holds '; ' or a control character" % model)
        parts.append("model=" + model.strip())
    files, dbs = [], []
    for f in froms or []:
        f = f.strip()
        if f.startswith("from="):
            f = f[5:]
        if FROM_DB_RE.match(f):
            dbs.append("from=" + f)
        elif FROM_FILE_RE.match(f) and not f.split("#")[0].endswith(".md") \
                and "; " not in f:
            files.append("from=" + f)
        else:
            raise Refused("from pointer %r is not <file>#<n>, <file>#h<n>, "
                          "research_items#<id> or queued_items#<id> "
                          "(<file> is the name without .md and without a path)" % f)
    return "; ".join(parts + files + dbs)


def check_by(cell):
    errs = []
    parts = cell.split("; ")
    if not SESSION_RE.match(parts[0]):
        errs.append("By %r does not start with a session id or 'unlogged'" % cell)
    stage = 0   # 0 model allowed, 1 file from, 2 db from
    for p in parts[1:]:
        if p.startswith("model="):
            if stage > 0 or not p[6:].strip():
                errs.append("By part %r is out of order or empty" % p)
            stage = max(stage, 1)
        elif p.startswith("from="):
            f = p[5:]
            if FROM_DB_RE.match(f):
                stage = 2
            elif FROM_FILE_RE.match(f) and not f.split("#")[0].endswith(".md"):
                if stage == 2:
                    errs.append("By part %r: file pointers go before db pointers" % p)
                stage = max(stage, 1)
            else:
                errs.append("By part %r is not a from= pointer form" % p)
        else:
            errs.append("By part %r is not model= or from=" % p)
    return errs


def file_pointers(by_cell):
    out = []
    for p in by_cell.split("; ")[1:]:
        if p.startswith("from=") and not FROM_DB_RE.match(p[5:]):
            m = FROM_FILE_RE.match(p[5:])
            if m:
                out.append(m.group(1))
    return out


# ------------------------------------------------------------ cells and rows
def split_cells(line):
    """Split a table row on unescaped pipes. Cells keep their escapes and
    their spaces (adapted from an earlier row splitter)."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i = [], [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("\\|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(cur))
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append("".join(cur))
    return cells


def is_sep(line):
    s = line.strip()
    if not s.startswith("|"):
        return False
    cells = [c.strip() for c in split_cells(s)]
    return any(c for c in cells) and all(re.match(r"^:?-{3,}:?$", c) for c in cells if c)


def unescape(cell):
    return cell.replace("\\|", "|")


def escape(value):
    return value.replace("|", "\\|")


def cell_values(cells):
    return [unescape(c.strip(" ")) for c in cells]


def line_id(values):
    """G S33: sha256 of the UTF-8 bytes of the 12 trimmed, unescaped values
    joined by a tab; first 10 hex digits, lower case."""
    return hashlib.sha256("\t".join(values).encode("utf-8")).hexdigest()[:10]


def render_row(values):
    return "|" + "|".join((" %s " % escape(v)) if v else "" for v in values) + "|"


def render_sep(n):
    return "|" + "|".join(["---"] * n) + "|"


def cell_errors(name, v):
    errs = []
    if CTRL_RE.search(v):
        errs.append("%s holds a line break, tab or control character" % name)
    if v.endswith("\\"):
        errs.append("%s ends in a lone backslash" % name)
    if "\\|" in v:
        errs.append("%s holds a backslash right before a pipe; give the plain pipe, "
                    "the writer escapes it (only \\| is an escape)" % name)
    return errs


# ------------------------------------------------------------ note parsing
def decode(data, path):
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("%s is not valid UTF-8" % path)


def eol_of(data):
    i = data.find(b"\n")
    if i > 0 and data[i - 1:i] == b"\r":
        return b"\r\n"
    return b"\n"


def frontmatter_value(lines, key):
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            for l in lines[1:i]:
                m = re.match(r"^%s:\s*(.*?)\s*$" % re.escape(key), l)
                if m:
                    return m.group(1).strip("'\""), i
            return None, i
    return None, None


def parse_note(text):
    lines = text.split("\n")
    lines = [l[:-1] if l.endswith("\r") else l for l in lines]
    look, fm_end = frontmatter_value(lines, "look_ledger")
    start = fm_end + 1 if fm_end is not None else 0
    years, tables, heads = [], [], []
    frozen = False
    infence = False
    rowno = 0
    i = start
    n = len(lines)
    while i < n:
        st = lines[i].strip()
        if st.startswith("```"):
            infence = not infence
            i += 1
            continue
        if infence:
            i += 1
            continue
        m = re.match(r"^## Looks ([0-9]{4})\s*$", st)
        if m:
            years.append(int(m.group(1)))
            heads.append(i)
        if st.startswith("*Frozen ") and "(D183)" in st:
            frozen = True
        if st.startswith("|") and i + 1 < n and is_sep(lines[i + 1]) and not is_sep(lines[i]):
            header = [c.strip() for c in split_cells(lines[i])]
            sep = split_cells(lines[i + 1])
            rows = []
            j = i + 2
            while j < n and lines[j].strip().startswith("|"):
                rowno += 1
                cells = split_cells(lines[j])
                rows.append({"idx": j, "n": rowno, "cells": cells})
                j += 1
            tables.append({"idx": i, "header": header, "sep": sep, "rows": rows, "end": j})
            i = j
            continue
        i += 1
    return {"lines": lines, "look": look, "years": years, "tables": tables,
            "frozen": frozen, "heads": heads}


# ------------------------------------------------------------ map
def read_map(path):
    """Read holon_lens_map from a Vault Config note: the Paths table row
    `| holon_lens_map | `<prefix>/=<ABBR>; ...` (...) |`. Returns
    {ABBR: prefix}."""
    try:
        with open(path, "rb") as fh:
            text = decode(fh.read(), path)
    except OSError as e:
        raise Refused("cannot read map file %s: %s" % (path, e))
    for line in text.split("\n"):
        m = re.match(r"^\|\s*holon_lens_map\s*\|\s*`([^`]*)`", line)
        if m:
            out = {}
            for part in m.group(1).split(";"):
                part = part.strip()
                if "=" in part:
                    pre, ab = part.rsplit("=", 1)
                    out[ab.strip()] = pre.strip()
            return out
    raise Refused("map file %s has no holon_lens_map row; add a Paths row "
                  "`| holon_lens_map | `<folder>/=<ABBR>` |` to Vault Config" % path)


def need_in_map(abbr, amap, what):
    if abbr not in amap:
        raise Refused("%s %r is not in holon_lens_map; add `<folder>/=%s` to the "
                      "holon_lens_map row in Vault Config Paths" % (what, abbr, abbr))


# ------------------------------------------------------------ validation
def validate_values(v, own, amap, year):
    """v: 12 unescaped values. Returns a list of error strings."""
    errs = []
    for name, val in zip(COLS, v):
        errs += cell_errors(name, val)
    d = dict(zip(FIELDS, v))
    if not d["subject"]:
        errs.append("Subject is empty")
    if d["kind"] not in KINDS:
        errs.append("Kind %r is not one of %s" % (d["kind"], ", ".join(KINDS)))
    errs += parse_key_cell(d["key"])[1]
    try:
        if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", d["date"]):
            raise ValueError
        dt = datetime.date(int(d["date"][:4]), int(d["date"][5:7]), int(d["date"][8:]))
        if year is not None and dt.year != year:
            errs.append("Date %s is not in the note's year %d (a line goes in a "
                        "section of the year of its Date)" % (d["date"], year))
    except ValueError:
        errs.append("Date %r is not an ISO date YYYY-MM-DD" % d["date"])
    if d["depth"] not in DEPTHS:
        errs.append("Depth %r is not one of %s" % (d["depth"], ", ".join(DEPTHS)))
    if d["relevance"] not in RELEVANCES:
        errs.append("Relevance %r is not one of %s" % (d["relevance"], ", ".join(RELEVANCES)))
    if d["outcome"] not in OUTCOMES:
        errs.append("Outcome %r is not one of %s" % (d["outcome"], ", ".join(OUTCOMES)))
    f = d["for"]
    if f:
        if not ABBR_RE.match(f):
            errs.append("For %r is not a project abbreviation; it must be upper case (e.g. ABC)" % f)
        elif own is not None and f == own:
            errs.append("For %r is the ledger's own abbreviation; leave For empty" % f)
        elif amap is not None and f not in amap:
            errs.append("For %r is not in holon_lens_map; add `<folder>/=%s` to the "
                        "holon_lens_map row in Vault Config Paths" % (f, f))
    if d["outcome"] == "queued" and not d["trigger"]:
        errs.append("Trigger is required when Outcome is queued")
    if d["outcome"] != "queued" and d["trigger"]:
        errs.append("Trigger must be empty unless Outcome is queued")
    if d["view_note"] and not WIKILINK_RE.match(d["view_note"]):
        errs.append("View note %r is not one wikilink [[...]]" % d["view_note"])
    if not d["by"]:
        errs.append("By is empty")
    else:
        errs += check_by(d["by"])
    return errs


def note_year(note, path):
    if len(note["years"]) != 1:
        raise Refused("%s must have exactly one '## Looks <year>' heading (found %d)"
                      % (path, len(note["years"])))
    return note["years"][0]


def the_table(note, path):
    """The one look table, structurally sound and last in the file."""
    ts = note["tables"]
    if len(ts) != 1:
        raise Refused("%s must hold exactly one table (found %d)" % (path, len(ts)))
    t = ts[0]
    if not note["heads"] or t["idx"] < note["heads"][0]:
        raise Refused("%s: the table is not under the '## Looks <year>' heading" % path)
    if t["header"] != COLS:
        raise Refused("%s: the table header is not the 12 look columns" % path)
    if len(t["sep"]) != 12:
        raise Refused("%s: the separator row does not have 12 cells" % path)
    for r in t["rows"]:
        if len(r["cells"]) != 12:
            raise Refused("%s: row %d (line %d) has %d cells, not 12"
                          % (path, r["n"], r["idx"] + 1, len(r["cells"])))
    tail = note["lines"][t["end"]:]
    if tail not in ([], [""]):
        raise Refused("%s: there is text or a blank line after the table; a line can "
                      "only be appended at the end of the table" % path)
    return t


# ------------------------------------------------------------ IO
def read_bytes(path):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as e:
        raise Refused("cannot read %s: %s" % (path, e))


def write_backup(path, data, today, always):
    """Create `<file>.pre-look-YYYYMMDD.bak` exclusively (never overwrite a
    .bak). With always=False an existing daily backup is enough; with
    always=True (init's shell edit) a taken name gets -2, -3, ... The
    backup is byte-compared to `data`."""
    base = "%s.pre-look-%s" % (path, today.replace("-", ""))
    bak = base + ".bak"
    if os.path.exists(bak):
        if not always:
            return None
        k = 2
        while os.path.exists("%s-%d.bak" % (base, k)):
            k += 1
        bak = "%s-%d.bak" % (base, k)
    try:
        with open(bak, "xb") as fh:
            fh.write(data)
    except OSError as e:
        raise Refused("cannot write the backup %s: %s; nothing written" % (bak, e))
    if read_bytes(bak) != data:
        raise Refused("the backup %s does not match the file; nothing written" % bak)
    return bak


backup_once = write_backup   # tests patch this name


def append_verified(path, old, new, today, dry):
    """Append bytes `new` to a file whose bytes were `old`. With dry=True the
    same checks run and the function stops just before the backup and write.
    Returns the backup path (or None)."""
    if read_bytes(path) != old:
        raise Refused("%s changed on disk between read and write; nothing written" % path)
    if dry:
        return None
    bak = backup_once(path, old, today, False)
    if read_bytes(path) != old:
        raise Refused("%s changed on disk between read and write; nothing written" % path)
    with open(path, "ab") as fh:
        fh.write(new)
    back = read_bytes(path)
    if back != old + new:
        raise VerifyFailed("%s: read-back differs (old bytes identical: %s; new line last: %s); "
                           "backup: %s" % (path, back[:len(old)] == old, back.endswith(new),
                                           bak or "the existing daily .pre-look .bak"))
    return bak


def rewrite_verified(path, old, new, today, dry):
    """Rewrite a file in place (open 'wb'; no temp file, no rename). Used
    only for init's shell edit; a backup is always taken first."""
    if read_bytes(path) != old:
        raise Refused("%s changed on disk between read and write; nothing written" % path)
    if dry:
        return None
    bak = backup_once(path, old, today, True)
    if read_bytes(path) != old:
        raise Refused("%s changed on disk between read and write; nothing written" % path)
    with open(path, "wb") as fh:
        fh.write(new)
    if read_bytes(path) != new:
        raise VerifyFailed("%s: read-back differs from the planned bytes; backup: %s"
                           % (path, bak))
    return bak


def create_verified(path, data, dry):
    if dry:
        return
    try:
        with open(path, "xb") as fh:
            fh.write(data)
    except FileExistsError:
        raise Refused("%s already exists; nothing written" % path)
    if read_bytes(path) != data:
        raise VerifyFailed("%s: read-back differs from the planned bytes" % path)


def today_of(args):
    t = getattr(args, "today", None) or datetime.date.today().isoformat()
    try:
        datetime.date(int(t[:4]), int(t[5:7]), int(t[8:10]))
        if not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", t):
            raise ValueError
    except ValueError:
        raise Refused("--today %r is not an ISO date" % t)
    return t


def yq(s):
    return "'" + s.replace("'", "''") + "'"


# ------------------------------------------------------------ skip list
def skip_dir(name):
    low = name.lower()
    return ("xarchive" in low or "_to_delete" in low or low.startswith("_archive")
            or low == "archive" or low == "rendered" or low.startswith("."))


def skip_file(name):
    """Read .md files only; a backup ends in .bak, so it is never .md."""
    return not name.endswith(".md")


def skipped_path(path):
    """True when any folder in `path` is skipped by skip_dir.
    One rule for every reader (a look index script can import skip_dir/skipped_path)."""
    parts = os.path.normpath(os.path.abspath(path)).split(os.sep)[:-1]
    return any(p and skip_dir(p) for p in parts)


def walk_md(top):
    for r, dirs, files in os.walk(top):
        dirs[:] = sorted(d for d in dirs if not skip_dir(d))
        for f in sorted(files):
            if not skip_file(f):
                yield os.path.join(r, f)


def head_flag(path):
    """Read only the frontmatter; return the look_ledger value or None."""
    try:
        with open(path, "rb") as fh:
            first = fh.readline()
            if first.strip() != b"---":
                return None
            for raw in fh:
                s = raw.strip()
                if s == b"---":
                    return None
                m = re.match(rb"^look_ledger:\s*(.*?)\s*$", raw.rstrip(b"\r\n"))
                if m:
                    return m.group(1).strip(b"'\"").decode("utf-8", "replace")
    except OSError:
        return None
    return None


# ------------------------------------------------------------ commands
def cmd_add(a):
    today = today_of(a)
    amap = read_map(a.map)
    old = read_bytes(a.ledger)
    note = parse_note(decode(old, a.ledger))
    own = note["look"]
    if not own:
        raise Refused("%s has no look_ledger flag in its frontmatter" % a.ledger)
    need_in_map(own, amap, "look_ledger value")
    if note["frozen"]:
        raise Refused("%s carries a frozen banner (D183); add to the current year section" % a.ledger)
    year = note_year(note, a.ledger)
    t = the_table(note, a.ledger)
    if len(old) >= SIZE_LIMIT:
        raise TooBig("%s is %d bytes, 40 KB (40,960 bytes) or more; start the next part "
                      "with `look_write.py init`" % (a.ledger, len(old)))
    for name, val in (("Subject", a.subject), ("Trigger", a.trigger), ("Finding", a.finding),
                      ("View note", a.view_note), ("For", a.for_)):
        if val and "\\|" in val:
            raise Refused("%s holds '\\|'; give the plain pipe, the writer escapes it" % name)
    key_cell, _ = build_key_cell(a.key or [])
    by = build_by(a.session, a.model, a.from_)
    v = [(x or "").strip(" ") for x in
         (a.subject, a.kind, key_cell, a.date, a.depth, a.relevance, a.for_, a.outcome,
          a.trigger, a.finding, a.view_note, by)]
    errs = validate_values(v, own, amap, year)
    if errs:
        raise Refused("; ".join(errs))
    lid = line_id(v)
    have = {}
    for r in t["rows"]:
        have[line_id(cell_values(r["cells"]))] = r["n"]
    if lid in have:
        raise Refused("line id %s is already in %s (row %d)" % (lid, a.ledger, have[lid]))
    row = render_row(v)
    back = cell_values(split_cells(row))
    if len(back) != 12 or back != v:
        raise Refused("the line would break the table (it does not split back into the "
                      "same 12 cells)")
    ptrs = file_pointers(by)
    if ptrs:
        if a.vault:
            places = [os.path.dirname(os.path.abspath(a.ledger)),
                      os.path.join(a.vault, amap[own])]
            for p in ptrs:
                found = set()
                for top in places:
                    if os.path.isdir(top):
                        for f in walk_md(top):
                            if os.path.basename(f) == p + ".md":
                                found.add(os.path.realpath(f))
                if not found:
                    raise Refused("from= file %r not found as %s.md in the project folder "
                                  "%s or the ledger's folder" % (p, p, amap[own]))
                if len(found) > 1:
                    raise Refused("from= file %r is ambiguous: %d files share the name %s.md "
                                  "(%s)" % (p, len(found), p, "; ".join(sorted(found))))
        else:
            sys.stderr.write("WARNING: from= file pointer(s) not checked (no --vault): %s\n"
                             % ", ".join(ptrs))
    eol = eol_of(old)
    fix = b"" if (not old or old.endswith(b"\n")) else eol
    new = fix + row.encode("utf-8") + eol
    if skipped_path(a.ledger):
        sys.stderr.write("WARNING: %s is in a skipped folder; find and the look index "
                         "will not see this line\n" % a.ledger)
    if fix:
        print("NOTE: %s has no final line ending; one %s before the line"
              % (a.ledger, "would be added" if a.dry_run else "was added"))
    bak = append_verified(a.ledger, old, new, today, a.dry_run)
    if a.dry_run:
        print("DRY RUN: would append to %s (line id %s):" % (a.ledger, lid))
        print(row)
        return 0
    if bak:
        print("backup: %s" % bak)
    print("added %s to %s" % (lid, a.ledger))
    return 0


def cmd_check(a):
    data = read_bytes(a.ledger)
    note = parse_note(decode(data, a.ledger))
    amap = read_map(a.map) if a.map else None
    errs = []
    own = note["look"]
    if not own:
        errs.append("no look_ledger flag in the frontmatter")
    elif amap is not None and own not in amap:
        errs.append("look_ledger %r is not in holon_lens_map; add `<folder>/=%s`" % (own, own))
    if len(note["years"]) != 1:
        errs.append("exactly one '## Looks <year>' heading is needed (found %d)" % len(note["years"]))
    year = note["years"][0] if len(note["years"]) == 1 else None
    if len(note["tables"]) != 1:
        errs.append("a look ledger note holds exactly one table (found %d)" % len(note["tables"]))
    elif note["heads"] and note["tables"][0]["idx"] < note["heads"][0]:
        errs.append("the table is not under the '## Looks <year>' heading")
    if note["tables"] and note["lines"][note["tables"][-1]["end"]:] not in ([], [""]):
        errs.append("text or a blank line follows the last table row")
    out = []
    ids = {}
    for t in note["tables"]:
        if t["header"] != COLS:
            errs.append("table at line %d: header is not the 12 look columns" % (t["idx"] + 1))
            continue
        if len(t["sep"]) != 12:
            errs.append("table at line %d: separator does not have 12 cells" % (t["idx"] + 1))
        for r in t["rows"]:
            where = "row %d (line %d)" % (r["n"], r["idx"] + 1)
            if len(r["cells"]) != 12:
                errs.append("%s: %d cells, not 12" % (where, len(r["cells"])))
                continue
            v = cell_values(r["cells"])
            for e in validate_values(v, own, amap, year):
                errs.append("%s: %s" % (where, e))
            lid = line_id(v)
            if lid in ids:
                errs.append("%s: line id %s repeats row %d" % (where, lid, ids[lid]))
            ids.setdefault(lid, r["n"])
            out.append({"id": lid, "row": r["n"], "line": r["idx"] + 1, "subject": v[0]})
    if a.json:
        print(json.dumps({"ledger": a.ledger, "project": own, "frozen": note["frozen"],
                          "lines": out, "errors": errs}, indent=1, sort_keys=True))
    else:
        for o in out:
            print("%s\trow %d\t%s" % (o["id"], o["row"], o["subject"]))
        if note["frozen"]:
            print("note: frozen banner present")
        if amap is None:
            print("note: no --map given; flag and For not checked against holon_lens_map")
        for e in errs:
            print("ERROR: %s" % e)
        print("%d line(s), %d error(s)" % (len(out), len(errs)))
    return 1 if errs else 0


def line_record(root, path, note, r):
    v = cell_values(r["cells"])
    keys, _ = parse_key_cell(v[2])
    rec = {"id": line_id(v), "project": note["look"],
           "ledger": os.path.relpath(path, root).replace(os.sep, "/"),
           "row": r["n"], "line": r["idx"] + 1,
           "keys": [{"scheme": k[0], "value": k[1], "raw": k[2], "strong": k[0] in STRONG}
                    for k in keys]}
    for f, x in zip(FIELDS, v):
        rec[f] = x
    return rec


def all_lines(root):
    out = []
    for path in walk_md(root):
        if head_flag(path) is None:
            continue
        try:
            with open(path, "rb") as fh:
                text = fh.read().decode("utf-8")
        except (OSError, UnicodeDecodeError) as e:
            sys.stderr.write("WARNING: cannot read %s: %s\n" % (path, e))
            continue
        note = parse_note(text)
        if not note["look"]:
            continue
        for t in note["tables"]:
            if t["header"] != COLS:
                continue
            for r in t["rows"]:
                if len(r["cells"]) != 12:
                    sys.stderr.write("WARNING: %s row %d has %d cells; skipped\n"
                                     % (path, r["n"], len(r["cells"])))
                    continue
                out.append(line_record(root, path, note, r))
    out.sort(key=lambda o: (o["ledger"], o["row"]))
    return out


def cmd_find(a):
    if not os.path.isdir(a.vault):
        raise Refused("--vault %s is not a folder" % a.vault)
    lines = all_lines(a.vault)
    if a.url is not None:
        q = unescape(a.url.strip()).replace(" ", "%20")
        n = norm_url(q) if re.match(r"^https?://", q, re.I) else norm_url("https://" + q)
        if not n:
            raise Refused("--url %r does not normalise" % a.url)
        hits = [o for o in lines if any(k["scheme"] == "url" and k["value"] == n
                                        for k in o["keys"])]
    elif a.name is not None:
        s = slugify(unescape(a.name))
        if not s:
            raise Refused("--name %r is empty after slugging" % a.name)
        hits = [o for o in lines if slugify(o["subject"]) == s or
                any(k["scheme"] == "name" and k["value"] == s for k in o["keys"])]
    else:
        hits = lines
    if a.json:
        print(json.dumps({"version": VERSION, "schema": 1, "lines": hits},
                         indent=1, sort_keys=True, ensure_ascii=True))
    else:
        for o in hits:
            print("%s\t%s\t%s#%d\t%s\t%s" % (o["id"], o["project"], o["ledger"], o["row"],
                                             o["subject"], o["key"]))
        print("%d line(s)" % len(hits), file=sys.stderr)
    return 0


def conf_note_bytes(path, by, session, today):
    stem = os.path.basename(path)
    if stem.endswith(".md"):
        stem = stem[:-3]
    t = [
        "---",
        "title: " + yq(stem),
        "type: project-doc",
        "created: " + today,
        "updated: " + today,
        "operator: " + by,
        "origin: " + yq("%s %s - created by look_write.py confirm" % (session, today)),
        "edit_log:",
        "  - " + yq("%s %s - created by look_write.py confirm" % (session, today)),
        "---",
        "",
        "# " + stem,
        "",
        "*Written and read by scripts only (`look_write.py confirm` writes, the look index "
        "reads). Never edit by MCP or by hand. Append-only: one row per confirmation (D183).*",
        "",
        "| " + " | ".join(CONF_COLS) + " |",
        render_sep(len(CONF_COLS)),
        "",
    ]
    return "\n".join(t).encode("utf-8")


def cmd_confirm(a):
    today = today_of(a)
    if not LINE_ID_RE.match(a.line or ""):
        raise Refused("--line %r is not a line id (10 lower-case hex digits)" % a.line)
    if a.what != "key" and (a.key or a.core):
        raise Refused("--key and --core go only with --what key")
    if a.core and not CORE_RE.match(a.core):
        raise Refused("--core %r is not a core_id" % a.core)
    for name, val in (("--by", a.by), ("--session", a.session)):
        if not val or not val.strip() or CTRL_RE.search(val) or val.endswith("\\"):
            raise Refused("%s %r is empty or holds a control character" % (name, val))
    if not SESSION_RE.match(a.session):
        raise Refused("--session %r is not a session id" % a.session)
    key = ""
    if a.what == "key" and a.key:
        k = build_key(a.key)
        key = "%s:%s" % (k[0], k[1])
    if a.ledger:
        lnote = parse_note(decode(read_bytes(a.ledger), a.ledger))
        if not lnote["look"]:
            raise Refused("%s has no look_ledger flag" % a.ledger)
        found = None
        for t in lnote["tables"]:
            for r in t["rows"]:
                if len(r["cells"]) == 12:
                    v = cell_values(r["cells"])
                    if line_id(v) == a.line:
                        found = v
        if found is None:
            raise Refused("line id %s is not in %s" % (a.line, a.ledger))
        if a.what == "key":
            lkeys = ["%s:%s" % (k[0], k[1]) for k in parse_key_cell(found[2])[0]]
            if not key:
                if len(lkeys) != 1:
                    raise Refused("the line has %d keys; name one with --key" % len(lkeys))
                key = lkeys[0]
            elif key not in lkeys:
                raise Refused("key %s is not a key of line %s (%s)" % (key, a.line, "; ".join(lkeys)))
    elif a.what == "key" and not key:
        raise Refused("--what key needs --key (or --ledger and a line with one key)")
    if not a.ledger:
        print("NOTE: id not checked (no --ledger); the look index reports unknown ids")
    v = [a.line, a.what, key, a.core or "", today, a.by.strip()]
    row = render_row(v)
    if cell_values(split_cells(row)) != v:
        raise Refused("the confirmation row would break the table")
    if not os.path.exists(a.note):
        if not a.create:
            raise Refused("%s does not exist; pass --create to make it" % a.note)
        body = conf_note_bytes(a.note, a.by.strip(), a.session, today)
        data = body + row.encode("utf-8") + b"\n"
        if a.dry_run:
            print("DRY RUN: would create %s with the line:" % a.note)
            print(row)
            return 0
        create_verified(a.note, data, False)
        print("created %s; confirmed %s %s" % (a.note, a.what, a.line))
        return 0
    old = read_bytes(a.note)
    note = parse_note(decode(old, a.note))
    if len(note["tables"]) != 1 or note["tables"][0]["header"] != CONF_COLS:
        raise Refused("%s is not a confirmations note (one table with %s)"
                      % (a.note, " | ".join(CONF_COLS)))
    t = note["tables"][0]
    for r in t["rows"]:
        if len(r["cells"]) != len(CONF_COLS):
            raise Refused("%s: row %d does not have %d cells" % (a.note, r["n"], len(CONF_COLS)))
    if note["lines"][t["end"]:] not in ([], [""]):
        raise Refused("%s: text or a blank line after the table" % a.note)
    eol = eol_of(old)
    fix = b"" if (not old or old.endswith(b"\n")) else eol
    new = fix + row.encode("utf-8") + eol
    if fix:
        print("NOTE: %s has no final line ending; one %s before the line"
              % (a.note, "would be added" if a.dry_run else "was added"))
    bak = append_verified(a.note, old, new, today, a.dry_run)
    if a.dry_run:
        print("DRY RUN: would append to %s:" % a.note)
        print(row)
        return 0
    if bak:
        print("backup: %s" % bak)
    print("confirmed %s %s in %s" % (a.what, a.line, a.note))
    return 0


def section_parts(sections, abbr, year):
    parts = []
    for f in sorted(os.listdir(sections)):
        p = os.path.join(sections, f)
        if skip_file(f) or not os.path.isfile(p):
            continue
        m = PART_RE.match(f)
        if not m or head_flag(p) != abbr:
            continue
        try:
            note = parse_note(read_bytes(p).decode("utf-8"))
        except UnicodeDecodeError:
            continue
        if year in note["years"]:
            parts.append((int(m.group(1)), int(m.group(2)), f[:-3], p))
    parts.sort()
    return parts


def split_chunks(data):
    return data.split(b"\n")


def chunk_text(c):
    return c[:-1].decode("utf-8") if c.endswith(b"\r") else c.decode("utf-8")


def cmd_init(a):
    today = today_of(a)
    amap = read_map(a.map)
    if not ABBR_RE.match(a.abbr):
        raise Refused("--abbr %r is not a project abbreviation" % a.abbr)
    need_in_map(a.abbr, amap, "--abbr")
    if not re.match(r"^[0-9]{4}$", a.year):
        raise Refused("--year %r is not a 4-digit year" % a.year)
    year = int(a.year)
    if not SESSION_RE.match(a.session):
        raise Refused("--session %r is not a session id" % a.session)
    if not a.operator.strip() or CTRL_RE.search(a.operator):
        raise Refused("--operator is empty")
    if not os.path.isdir(a.sections):
        raise Refused("--sections %s is not a folder" % a.sections)
    for pth in (a.sections + os.sep + "x", a.shell):
        if skipped_path(pth):
            sys.stderr.write("WARNING: %s is in a skipped folder; find and the look index "
                             "will not see it\n" % os.path.dirname(pth))
    parts = section_parts(a.sections, a.abbr, year)
    entries = [e for e in os.listdir(a.sections) if e.endswith(".md")]
    if not parts:
        nums = [int(PART_RE.match(e).group(1)) for e in entries if PART_RE.match(e)]
        n = max(nums) + 1 if nums else 1
        m = 0
        name = "%d.0 Looks %d - %s Research Tracking Index" % (n, year, a.abbr)
        prev = None
    else:
        n, mm, prev, ppath = parts[-1]
        size = os.path.getsize(ppath)
        if size < SIZE_LIMIT:
            raise Refused("the newest part of %d, %s, is %d bytes, under 40 KB (40,960 bytes); "
                          "keep adding lines there" % (year, prev, size))
        m = mm + 1
        while any(e.startswith("%d.%d " % (n, m)) for e in entries):
            m += 1
        name = "%d.%d Looks %d - Part %d - %s Research Tracking Index" % (n, m, year, m + 1, a.abbr)
    path = os.path.join(a.sections, name + ".md")
    if os.path.exists(path):
        raise Refused("%s already exists" % path)
    shell_old = read_bytes(a.shell)
    decode(shell_old, a.shell)
    eol = eol_of(shell_old)
    shell_stem = os.path.basename(a.shell)
    if shell_stem.endswith(".md"):
        shell_stem = shell_stem[:-3]
    chunks = split_chunks(shell_old)
    texts = [chunk_text(c) for c in chunks]
    embed = "![[%s]]" % name
    if any(t.strip() == embed for t in texts):
        raise Refused("the shell already embeds %s" % name)
    grow_re = re.compile(r"^<!-- grow: group=%d " % n)
    grow_idx = [i for i, t in enumerate(texts) if grow_re.match(t.strip())]
    grow = '<!-- grow: group=%d target="%s" insert=after soft=40 -->' % (n, name)
    notes = []
    added = "would be added" if a.dry_run else "was added"
    E = eol
    if prev is None:
        if grow_idx:
            raise Refused("the shell already has a grow line for group %d" % n)
        body = shell_old
        if body and not body.endswith(b"\n"):
            body += E
            notes.append("the shell has no final line ending; one %s" % added)
        lead = b"" if (body.endswith(b"\n\n") or body.endswith(b"\r\n\r\n") or not body) else E
        shell_new = body + lead + grow.encode("utf-8") + E + embed.encode("utf-8") + E
    else:
        pe = [i for i, t in enumerate(texts) if t.strip() == "![[%s]]" % prev]
        if not pe:
            raise Refused("the shell has no embed of the previous part %s" % prev)
        at = pe[-1]
        cr = b"\r" if chunks[at].endswith(b"\r") else (b"\r" if eol == b"\r\n" else b"")
        new_chunks = list(chunks)
        if grow_idx:
            gi = grow_idx[0]
            new_c, k = re.subn(rb'target="[^"]*"', ('target="%s"' % name).encode("utf-8"),
                               new_chunks[gi], count=1)
            if k != 1:
                raise Refused("the grow line of group %d has no target" % n)
            new_chunks[gi] = new_c
        ins = [cr, embed.encode("utf-8") + cr]
        if at == len(chunks) - 1:
            # previous embed is the last line, with no final line ending
            new_chunks[at] = chunks[at] + (b"\r" if eol == b"\r\n" else b"")
            ins = [cr, embed.encode("utf-8") + cr, b""]
            notes.append("the shell has no final line ending; one %s" % added)
        new_chunks[at + 1:at + 1] = ins
        if not grow_idx:
            first = "![[%d.0 Looks %d - %s Research Tracking Index]]" % (n, year, a.abbr)
            fe = [i for i, t in enumerate(texts) if t.strip() == first]
            gi = fe[0] if (fe and fe[0] <= at) else at
            gcr = b"\r" if chunks[gi].endswith(b"\r") else b""
            new_chunks[gi:gi] = [grow.encode("utf-8") + gcr]
            notes.append("the shell has no grow line for group %d; one %s" % (n, added))
        shell_new = b"\n".join(new_chunks)
    section = "%d.%d" % (n, m)
    origin = "%s %s - created by look_write.py init" % (a.session, today)
    t = ["---",
         "title: " + yq(name),
         "type: project-doc",
         "parent: " + yq("[[%s]]" % shell_stem),
         "section: " + yq(section),
         "created: " + today,
         "updated: " + today,
         "operator: " + a.operator.strip(),
         "look_ledger: " + a.abbr,
         "origin: " + yq(origin),
         "edit_log:",
         "  - " + yq(origin),
         "---",
         "",
         "*Part of the [[%s]]*" % shell_stem]
    if prev:
        t.append("*Continuation of [[%s]]*" % prev)
    t += ["",
          "## Looks %d" % year,
          "",
          "*Lines are written only by `look_write.py add` (D183). Do not edit or delete a line.*",
          "",
          "| " + " | ".join(COLS) + " |",
          render_sep(12),
          ""]
    note_bytes = E.join(x.encode("utf-8") for x in t)
    rewrite_verified(a.shell, shell_old, shell_new, today, True)   # checks only
    if a.dry_run:
        print("DRY RUN: would create %s" % path)
        print("DRY RUN: would write the shell %s (%d -> %d bytes)" % (a.shell, len(shell_old), len(shell_new)))
        for x in notes:
            print("NOTE: " + x)
        return 0
    create_verified(path, note_bytes, False)
    try:
        bak = rewrite_verified(a.shell, shell_old, shell_new, today, False)
    except Refused as e:
        raise Refused("%s was created, but the shell was not written: %s. Add the embed "
                      "line `%s` to the shell by script, then run check" % (path, e, embed))
    for x in notes:
        print("NOTE: " + x)
    if bak:
        print("backup: %s" % bak)
    print(path)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="look_write.py", description="look line writer")
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="cmd")
    sub.required = True
    i = sub.add_parser("init")
    i.add_argument("--sections", required=True)
    i.add_argument("--shell", required=True)
    i.add_argument("--abbr", required=True)
    i.add_argument("--year", required=True)
    i.add_argument("--map", required=True)
    i.add_argument("--session", required=True)
    i.add_argument("--operator", required=True)
    i.add_argument("--today")
    i.add_argument("--dry-run", action="store_true")
    ad = sub.add_parser("add")
    ad.add_argument("--ledger", required=True)
    ad.add_argument("--map", required=True)
    ad.add_argument("--subject", required=True)
    ad.add_argument("--kind", required=True)
    ad.add_argument("--key", action="append")
    ad.add_argument("--date", required=True)
    ad.add_argument("--depth", required=True)
    ad.add_argument("--relevance", required=True)
    ad.add_argument("--for", dest="for_", default="")
    ad.add_argument("--outcome", required=True)
    ad.add_argument("--trigger", default="")
    ad.add_argument("--finding", default="")
    ad.add_argument("--view-note", default="")
    ad.add_argument("--session", required=True)
    ad.add_argument("--model")
    ad.add_argument("--from", dest="from_", action="append")
    ad.add_argument("--vault")
    ad.add_argument("--today")
    ad.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--ledger", required=True)
    c.add_argument("--map")
    c.add_argument("--json", action="store_true")
    f = sub.add_parser("find")
    f.add_argument("--vault", required=True)
    g = f.add_mutually_exclusive_group(required=True)
    g.add_argument("--url")
    g.add_argument("--name")
    g.add_argument("--all", action="store_true")
    f.add_argument("--json", action="store_true")
    co = sub.add_parser("confirm")
    co.add_argument("--note", required=True)
    co.add_argument("--line", required=True)
    co.add_argument("--what", required=True, choices=("key", "outcome", "depth"))
    co.add_argument("--by", required=True)
    co.add_argument("--key")
    co.add_argument("--core")
    co.add_argument("--ledger")
    co.add_argument("--session", default="unlogged")
    co.add_argument("--create", action="store_true")
    co.add_argument("--today")
    co.add_argument("--dry-run", action="store_true")
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    fn = {"init": cmd_init, "add": cmd_add, "check": cmd_check, "find": cmd_find,
          "confirm": cmd_confirm}[a.cmd]
    try:
        return fn(a)
    except TooBig as e:
        sys.stderr.write("REFUSED: %s\n" % e)
        return 4
    except Refused as e:
        sys.stderr.write("REFUSED: %s\n" % e)
        return 1
    except VerifyFailed as e:
        sys.stderr.write("VERIFY FAILED: %s\n" % e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
