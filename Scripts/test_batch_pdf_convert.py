#!/usr/bin/env python3
"""
test_batch_pdf_convert.py - tests for batch_pdf_convert.py --output-dir.

created: 2026-11 (DataWizard)
edit_log:
  - 2026-11 - first version; covers the --output-dir option

Standard library unittest only. No PDF engine is needed: the Docling call
is replaced by a stub that returns fixed markdown. Fixtures are made in a
fresh temp folder per test, outside the vault, removed after the test. Run
from any folder:

    python3 -I "<scripts folder>/test_batch_pdf_convert.py" -v
"""
import contextlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "batch_pdf_convert", os.path.join(HERE, "batch_pdf_convert.py"))
bpc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bpc)

SHORT_MD = "# Sample\n\n" + ("alpha beta gamma delta " * 30) + "\n"


def long_md():
    parts = ["# Sample"]
    for n in range(1, 5):
        parts.append("## Chapter %d" % n)
        parts.append("word " * 1600)
    return "\n\n".join(parts) + "\n"


class OutputDirTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="bpc_test_"))
        self.src = self.tmp / "src"
        self.out = self.tmp / "out"
        self.src.mkdir()
        self.pdf = self.src / "Sample Doc.pdf"
        self.pdf.write_bytes(b"%PDF-1.4 stub\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_main(self, args, md=SHORT_MD):
        argv = ["batch_pdf_convert.py"] + [str(a) for a in args]
        buf = io.StringIO()
        with mock.patch.object(bpc, "convert_with_docling",
                               return_value=md) as stub, \
                mock.patch.object(sys, "argv", argv), \
                contextlib.redirect_stdout(buf):
            bpc.main()
        return stub, buf.getvalue()

    def logs_in(self, folder):
        return sorted(Path(folder).glob("conversion_log_*.md"))

    # (a) with --output-dir: .md in output folder, nothing beside the PDF
    def test_output_dir_places_md(self):
        stub, _ = self.run_main([self.pdf, "--force", "--output-dir", self.out])
        self.assertEqual(stub.call_count, 1)
        self.assertTrue((self.out / "Sample Doc.md").is_file())
        self.assertEqual(sorted(p.name for p in self.src.iterdir()),
                         ["Sample Doc.pdf"])

    # (b) without --output-dir: unchanged, .md beside the PDF
    def test_default_beside_pdf(self):
        self.run_main([self.pdf, "--force"])
        self.assertTrue((self.src / "Sample Doc.md").is_file())
        self.assertFalse(self.out.exists())

    # (c) long output: PDF Sections/ in the output folder
    def test_long_output_sections_in_output_dir(self):
        self.run_main([self.pdf, "--force", "--output-dir", self.out],
                      md=long_md())
        shell = self.out / "Sample Doc.md"
        self.assertTrue(shell.is_file())
        self.assertIn("has_sections: true", shell.read_text(encoding="utf-8"))
        secs = self.out / "PDF Sections" / "Sample Doc"
        self.assertTrue(secs.is_dir())
        self.assertTrue(list(secs.glob("S01 - *.md")))
        self.assertFalse((self.src / "PDF Sections").exists())

    # (d) log location: output folder with --output-dir, input folder without,
    #     --log-dir still wins
    def test_log_goes_to_output_dir(self):
        self.run_main([self.pdf, "--force", "--output-dir", self.out])
        self.assertEqual(len(self.logs_in(self.out)), 1)
        self.assertEqual(self.logs_in(self.src), [])

    def test_log_default_input_dir(self):
        self.run_main([self.pdf, "--force"])
        self.assertEqual(len(self.logs_in(self.src)), 1)

    def test_log_dir_overrides(self):
        logs = self.tmp / "logs"
        logs.mkdir()
        self.run_main([self.pdf, "--force", "--output-dir", self.out,
                       "--log-dir", logs])
        self.assertEqual(len(self.logs_in(logs)), 1)
        self.assertEqual(self.logs_in(self.out), [])

    # skip check uses the output folder
    def test_skip_check_uses_output_dir(self):
        self.out.mkdir()
        (self.out / "Sample Doc.md").write_text("existing\n", encoding="utf-8")
        stub, _ = self.run_main([self.pdf, "--output-dir", self.out])
        self.assertEqual(stub.call_count, 0)
        self.assertEqual((self.out / "Sample Doc.md").read_text(
            encoding="utf-8"), "existing\n")

    def test_dry_run_uses_output_dir(self):
        self.out.mkdir()
        (self.out / "Sample Doc.md").write_text("existing\n", encoding="utf-8")
        stub, text = self.run_main([self.pdf, "--dry-run",
                                    "--output-dir", self.out])
        self.assertEqual(stub.call_count, 0)
        self.assertIn("[SKIP - .md exists]", text)
        self.assertIn("Would convert: 0 / 1", text)

    # (e) directory input plus --output-dir: error exit, nothing written
    def test_directory_with_output_dir_errors(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_main([self.src, "--output-dir", self.out])
        self.assertNotEqual(cm.exception.code, 0)
        self.assertFalse(self.out.exists())
        self.assertEqual(self.logs_in(self.src), [])


if __name__ == "__main__":
    unittest.main()
