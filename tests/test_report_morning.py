"""Tests for bin/report-morning. Provider-free: Drop is a fake that counts requests."""
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
rm.time.sleep = lambda seconds: None


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

    def test_message_fits_drop_limits(self):
        rows = [dict(repo=f"r{i}", path="/x/", title="t", lede="l" * 300, status="done", stats=[], asks=["a"])
                for i in range(20)]
        msg = rm.message(rows, "2026-11-25")
        self.assertLessEqual(len(msg["summary"]), rm.SUMMARY_MAX)
        self.assertLessEqual(len(msg["title"]), rm.TITLE_MAX)
        self.assertIn("more in the report", msg["summary"])
        self.assertEqual(msg["event_id"], "reports:morning:2026-11-25")
        self.assertEqual(msg["source_url"], "https://reports.khamel.com/reports/morning-2026-11-25/")


class Send(unittest.TestCase):
    def test_one_post_then_bounded_receipt_reads(self):
        calls = []

        def fake(method, url, token, body=None):
            calls.append(method)
            state = "delivered" if len(calls) == 3 else "pending"
            return dict(receipt_id="r1", state=state, provider_receipt={"channel_id": "C", "ts": "1"}
                        if state == "delivered" else None)

        receipt = rm.send({"event_id": "e"}, "http://drop", "t", "C", http=fake)
        self.assertEqual(receipt["state"], "delivered")
        self.assertEqual(calls, ["POST", "GET", "GET"])

    def test_simulated_hour_of_runs_stays_bounded(self):
        """The job runs once a day; even 60 runs in one hour that never deliver cap at 13 requests each."""
        calls = []

        def stuck(method, url, token, body=None):
            calls.append(method)
            return dict(receipt_id="r1", state="pending", provider_receipt=None)

        for _ in range(60):
            rm.send({"event_id": "e"}, "http://drop", "t", "C", http=stuck)
        self.assertEqual(calls.count("POST"), 60)
        self.assertEqual(len(calls), 60 * 13)


if __name__ == "__main__":
    unittest.main()
