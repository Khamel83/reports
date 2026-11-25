"""Tests for bin/report-morning."""
import fcntl
import importlib.machinery
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "..", "bin")
# Real git commits in tests must not depend on the machine's git config (signing, hooks).
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def load(name, file):
    loader = importlib.machinery.SourceFileLoader(name, os.path.join(BIN, file))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    loader.exec_module(module)
    return module


rm = load("report_morning", "report-morning")
ri = load("report_index", "report-index")


def page(kind="bed", status="done", lede="Shipped the fix.", asks=()):
    cards = "".join(f'<div class="card ask"><h3>{a}</h3><p>x</p></div>' for a in asks)
    return (f'<title>Night &amp; day</title><meta name="report:kind" content="{kind}">'
            f'<meta name="bed:status" content="{status}"><p class="lede">{lede}</p>'
            f'<div class="stats"><div class="stat"><b>3</b>PRs</div></div>{cards}')


class Build(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)

    def put(self, repo, slug, body):
        os.makedirs(os.path.join(self.root, repo, slug))
        with open(os.path.join(self.root, repo, slug, "index.html"), "w") as handle:
            handle.write(body)

    def test_picks_only_bed_pages_of_that_morning(self):
        self.put("alpha", "bed-2026-11-25", page(asks=["Pick a <b>name</b>"]))
        self.put("beta", "bed-2026-11-25-api", page(status="blocked", lede="Waits on a key."))
        self.put("gamma", "bed-2026-11-24", page())             # other night
        self.put("delta", "bed-2026-11-25", page(kind="plan"))  # not a bed report
        self.put("delta", "bed-2026-11-250", page())            # not this date
        rows = rm.collect(self.root, "2026-11-25")
        self.assertEqual([r["repo"] for r in rows], ["alpha", "beta"])
        self.assertEqual(rows[0]["asks"], ["Pick a name"])
        self.assertEqual(rows[0]["stats"], [("3", "PRs")])
        self.assertEqual(rows[1]["status"], "blocked")
        out = rm.render(rows, "2026-11-25")
        self.assertIn('href="/_/tokens.css"', out)
        self.assertIn("alpha: Pick a name", out)
        self.assertIn("Night &amp; day", out)
        self.assertNotIn("Not counted", out)

    def test_unreadable_ask_warns(self):
        import contextlib, io
        self.put("alpha", "bed-2026-11-25", page() + '<div class="card ask" id="x"><h3>Hidden</h3></div>')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = rm.collect(self.root, "2026-11-25")
        self.assertEqual(rows[0]["asks"], [])
        self.assertIn("do not match the bed markup", err.getvalue())
        self.assertIn("Not counted: 1 ask cards or numbers in alpha", rm.render(rows, "2026-11-25"))

    def test_meta_in_any_attribute_order(self):
        self.put("alpha", "bed-2026-11-25", "<meta content='bed' name='report:kind'>"
                 "<meta  content=\"blocked\"  name=\"bed:status\">")
        rows = rm.collect(self.root, "2026-11-25")
        self.assertEqual([r["status"] for r in rows], ["blocked"])

    def test_bed_dated_page_of_another_kind_warns(self):
        import contextlib, io
        self.put("alpha", "bed-2026-11-25", page(kind="report"))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(rm.collect(self.root, "2026-11-25"), [])
        self.assertIn("not in the morning report", err.getvalue())

    def test_non_utf8_page_is_skipped(self):
        os.makedirs(os.path.join(self.root, "alpha", "bed-2026-11-25"))
        with open(os.path.join(self.root, "alpha", "bed-2026-11-25", "index.html"), "wb") as handle:
            handle.write(b"\xff\xfe bad")
        self.put("beta", "bed-2026-11-25", page())
        import contextlib, io
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual([r["repo"] for r in rm.collect(self.root, "2026-11-25")], ["beta"])

    def test_impossible_date_is_refused(self):
        self.assertFalse(rm.real_date("2026-02-30"))
        self.assertTrue(rm.real_date("2026-11-25"))

    def test_unknown_status_is_counted(self):
        self.put("alpha", "bed-2026-11-25", page(status="sleeping"))
        out = rm.render(rm.collect(self.root, "2026-11-25"), "2026-11-25")
        self.assertIn("1 with no status", out)
        self.assertIn("<b>1</b>not done", out)

    def test_restyle_commit_does_not_move_the_date(self):
        self.put("alpha", "bed-2026-11-25", page())
        git = lambda *a, **dates: subprocess.run(["git", "-C", self.root, *a], check=True, capture_output=True,
                                                 env={**GIT_ENV, **dates})
        git("init", "-q")
        git("add", "-A")
        git("commit", "-qm", "report: alpha",
            GIT_AUTHOR_DATE="2026-11-25T01:00:00-08:00", GIT_COMMITTER_DATE="2026-11-25T01:00:00-08:00")
        with open(os.path.join(self.root, "alpha", "bed-2026-11-25", "index.html"), "a") as handle:
            handle.write(" ")
        git("commit", "-qam", "restyle: stylesheet 1",
            GIT_AUTHOR_DATE="2026-11-25T04:00:00-08:00", GIT_COMMITTER_DATE="2026-11-25T04:00:00-08:00")
        when = rm.collect(self.root, "2026-11-25")[0]["when"]
        self.assertEqual(when.hour, 1)


class Cli(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)
        self.out = os.path.join(self.root, "out.html")

    def run_build(self, *args):
        return subprocess.run([sys.executable, os.path.join(BIN, "report-morning"), *args],
                              capture_output=True, text=True).returncode

    def test_exit_codes(self):
        self.assertEqual(self.run_build("build", self.root, "2026-02-30", self.out), 2)
        self.assertEqual(self.run_build("build", self.root, "2026-11-25", self.out), 4)  # no .git: no lock
        os.makedirs(os.path.join(self.root, ".git"))
        self.assertEqual(self.run_build("build", self.root, "2026-11-25", self.out), 3)
        os.makedirs(os.path.join(self.root, "alpha", "bed-2026-11-25"))
        with open(os.path.join(self.root, "alpha", "bed-2026-11-25", "index.html"), "w") as handle:
            handle.write(page())
        self.assertEqual(self.run_build("build", self.root, "2026-11-25", self.out), 0)
        self.assertTrue(os.path.getsize(self.out))

    def test_busy_lock_gives_up_with_4(self):
        os.makedirs(os.path.join(self.root, ".git"))
        with open(os.path.join(self.root, ".git", "report-publish.lock"), "a") as held:
            fcntl.flock(held, fcntl.LOCK_EX)
            with mock.patch.object(rm.time, "sleep"), \
                    mock.patch.object(sys, "argv", ["report-morning", "build", self.root, "2026-11-25", self.out]), \
                    self.assertRaises(SystemExit) as stop:
                rm.main()
        self.assertEqual(stop.exception.code, 4)


class Index(unittest.TestCase):
    def test_morning_copy_and_banner_follow_the_newest_morning_page(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root, True)
        page_dir = os.path.join(root, "reports", "morning-2026-11-25")
        os.makedirs(page_dir)
        with open(os.path.join(page_dir, "index.html"), "w") as handle:
            handle.write('<title>While you slept</title><meta name="report:kind" content="morning">')
        with mock.patch.object(sys, "argv", ["report-index", root]):
            ri.main()
        self.assertIn("While you slept", open(os.path.join(root, "morning", "index.html")).read())
        self.assertIn('href="/morning/"', open(os.path.join(root, "index.html")).read())
        shutil.rmtree(page_dir)
        with mock.patch.object(sys, "argv", ["report-index", root]):
            ri.main()
        self.assertFalse(os.path.exists(os.path.join(root, "morning", "index.html")))
        self.assertNotIn('href="/morning/"', open(os.path.join(root, "index.html")).read())


if __name__ == "__main__":
    unittest.main()
