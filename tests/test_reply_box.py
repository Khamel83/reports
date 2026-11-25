"""python3 -m unittest discover -s tests"""
import importlib.machinery
import importlib.util
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("reply_box", os.path.join(HERE, "..", "bin", "report-reply-box"))
spec = importlib.util.spec_from_loader("reply_box", loader)
box = importlib.util.module_from_spec(spec)
loader.exec_module(box)

PAGE = ('<!doctype html><html><head><title>Pick &amp; go</title>'
        '<meta name="report:ticket" content="DO-7"><meta name="report:choices" content="A|B &lt;x&gt;">'
        '</head><body><main><h1>x</h1></main></body></html>')


class ReplyBox(unittest.TestCase):
    def test_box_has_page_fields_and_choices(self):
        page = box.apply(PAGE, "infra", "pick-go")
        self.assertEqual(page.count(box.START), 1)
        self.assertIn('<input type="hidden" name="repo" value="infra">', page)
        self.assertIn('<input type="hidden" name="slug" value="pick-go">', page)
        self.assertIn('<input type="hidden" name="ticket" value="DO-7">', page)
        self.assertIn('<input type="hidden" name="title" value="Pick &amp; go">', page)
        self.assertIn('<button class="choice" name="choice" value="A">A</button>', page)
        self.assertIn('value="B &lt;x&gt;">B &lt;x&gt;</button>', page)
        self.assertLess(page.index(box.END), page.index("</main>"))
        self.assertNotIn("<script", page)

    def test_second_run_replaces_the_box(self):
        once = box.apply(PAGE, "infra", "pick-go")
        self.assertEqual(box.apply(once, "infra", "pick-go"), once)
        moved = box.apply(once.replace("DO-7", "DO-8"), "infra", "pick-go")
        self.assertEqual(moved.count(box.START), 1)
        self.assertIn('value="DO-8"', moved)

    def test_box_goes_before_the_footer(self):
        page = box.apply(PAGE.replace("</main>", '<footer class="meta">by x</footer></main>'), "infra", "x")
        self.assertLess(page.index(box.END), page.index('<footer class="meta">'))

    def test_choices_in_a_comment_are_ignored(self):
        page = box.apply('<head><!-- <meta name="report:choices" content="A|B"> --></head><main></main>', "infra", "x")
        self.assertNotIn('class="choice"', page)

    def test_no_main_no_box(self):
        self.assertEqual(box.apply("<p>x</p>", "infra", "x"), "<p>x</p>")

    def test_tree_skips_dashboard_pages(self):
        with tempfile.TemporaryDirectory() as root:
            for rel in ("index.html", "_/by-repo/index.html", "infra/one/index.html", ".git/x/index.html"):
                os.makedirs(os.path.join(root, os.path.dirname(rel)), exist_ok=True)
                with open(os.path.join(root, rel), "w") as handle:
                    handle.write(PAGE)
            self.assertEqual(box.main(root), 1)
            self.assertEqual(box.main(root), 0)
            for rel in ("index.html", "_/by-repo/index.html"):
                with open(os.path.join(root, rel)) as handle:
                    self.assertNotIn(box.START, handle.read())


if __name__ == "__main__":
    unittest.main()
