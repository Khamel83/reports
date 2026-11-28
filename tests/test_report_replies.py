"""python3 -m unittest discover -s tests"""
import contextlib
import importlib.machinery
import importlib.util
import io
import os
import pathlib
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("report_replies", os.path.join(HERE, "..", "bin", "report-replies"))
spec = importlib.util.spec_from_loader("report_replies", loader)
rr = importlib.util.module_from_spec(spec)
loader.exec_module(rr)


class FakeInbox:
    def __init__(self):
        self.items, self.content, self.calls = [], {}, []

    def add(self, repo, slug, text):
        seq = len(self.items) + 1
        drop_id = f"d{seq}"
        self.items.append({"drop_id": drop_id, "sequence_id": seq, "client": "reports"})
        self.content[drop_id] = {"schema": "reports.reply.v1", "reply_id": f"r{seq}", "repo": repo, "slug": slug,
                                 "text": text, "sent_at": "2026-11-27T00:00:00Z"}

    def get(self, base, path):
        self.calls.append(path)
        if path.endswith("/content"):
            return self.content[path.split("/")[3]]
        after = int(path.split("after=")[1].split("&")[0])
        items = [i for i in self.items if i["sequence_id"] > after]
        return {"items": items, "has_more": False, "next_after": items[-1]["sequence_id"] if items else after}


class Clock:
    def __init__(self):
        self.now = 0.0
        self.hooks = {}

    def sleep(self, s):
        self.now += s
        for t, fn in list(self.hooks.items()):
            if self.now >= t:
                fn()
                del self.hooks[t]

    def __call__(self):
        return self.now


class Wait(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_cache, self.old_get = rr.CACHE, rr.get
        rr.CACHE = pathlib.Path(self.tmp.name) / "cache.json"
        self.inbox = FakeInbox()
        rr.get = self.inbox.get
        self.clock = Clock()

    def tearDown(self):
        rr.CACHE, rr.get = self.old_cache, self.old_get
        self.tmp.cleanup()

    def run_wait(self, limit=rr.WAIT_LIMIT):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = rr.wait("http://x", "g2k", "page", limit=limit, sleep=self.clock.sleep, clock=self.clock)
        return code, out.getvalue()

    def test_prints_first_new_reply_within_a_minute(self):
        self.inbox.add("g2k", "page", "old answer")
        self.clock.hooks[150] = lambda: self.inbox.add("g2k", "page", "new answer")
        code, out = self.run_wait()
        self.assertEqual(code, 0)
        self.assertIn("new answer", out)
        self.assertNotIn("old answer", out)
        self.assertLessEqual(self.clock.now, 150 + rr.WAIT_EVERY)

    def test_other_pages_do_not_end_the_wait(self):
        self.clock.hooks[60] = lambda: self.inbox.add("g2k", "other", "x")
        self.clock.hooks[300] = lambda: self.inbox.add("infra", "page", "y")
        code, _ = self.run_wait(limit=600)
        self.assertEqual(code, 1)

    def test_gives_up_after_two_hours(self):
        code, _ = self.run_wait()
        self.assertEqual(code, 1)
        self.assertGreaterEqual(self.clock.now, 2 * 60 * 60)

    def test_requests_in_one_simulated_hour(self):
        self.run_wait(limit=60 * 60)
        lists = [c for c in self.inbox.calls if c.startswith("/v1/drops?")]
        self.assertLessEqual(len(lists), 61)  # one at start plus one a minute
        self.assertEqual(len(self.inbox.calls), len(lists))  # no content reads without new replies


if __name__ == "__main__":
    unittest.main()
