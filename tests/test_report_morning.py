"""Tests for bin/report-morning."""
import importlib.machinery
import importlib.util
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("report_morning", os.path.join(HERE, "..", "bin", "report-morning"))
spec = importlib.util.spec_from_loader("report_morning", loader)
rm = importlib.util.module_from_spec(spec)
loader.exec_module(rm)


def page(kind="bed", status="done", lede="Shipped the fix.", asks=()):
    cards = "".join(f'<div class="card ask"><h3>{a}</h3><p>x</p></div>' for a in asks)
    return (f'<title>Night &amp; day</title><meta name="report:kind" content="{kind}">'
            f'<meta name="bed:status" content="{status}"><p class="lede">{lede}</p>'
            f'<div class="stats"><div class="stat"><b>3</b>PRs</div></div>{cards}')


class Build(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

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

    def test_unreadable_ask_warns(self):
        import contextlib, io
        self.put("alpha", "bed-2026-11-25", page() + '<div class="card ask" id="x"><h3>Hidden</h3></div>')
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rows = rm.collect(self.root, "2026-11-25")
        self.assertEqual(rows[0]["asks"], [])
        self.assertIn("does not match the bed markup", err.getvalue())

    def test_unknown_status_is_counted(self):
        self.put("alpha", "bed-2026-11-25", page(status="sleeping"))
        out = rm.render(rm.collect(self.root, "2026-11-25"), "2026-11-25")
        self.assertIn("1 with no status", out)
        self.assertIn("<b>1</b>not done", out)

    def test_restyle_commit_does_not_move_the_date(self):
        import subprocess
        self.put("alpha", "bed-2026-11-25", page())
        git = lambda *a, **env: subprocess.run(["git", "-C", self.root, *a], check=True, capture_output=True,
                                               env={**os.environ, **env})
        git("init", "-q")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "x", "--allow-empty")
        git("add", "-A")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "report: alpha",
            GIT_AUTHOR_DATE="2026-11-25T01:00:00-08:00", GIT_COMMITTER_DATE="2026-11-25T01:00:00-08:00")
        with open(os.path.join(self.root, "alpha", "bed-2026-11-25", "index.html"), "a") as handle:
            handle.write(" ")
        git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "restyle: stylesheet 1",
            GIT_AUTHOR_DATE="2026-11-25T04:00:00-08:00", GIT_COMMITTER_DATE="2026-11-25T04:00:00-08:00")
        when = rm.collect(self.root, "2026-11-25")[0]["when"]
        self.assertEqual(when.hour, 1)


if __name__ == "__main__":
    unittest.main()
