import tempfile
import unittest
from pathlib import Path

from scripts.export_markdown import export_markdown_files


class ExportMarkdownTests(unittest.TestCase):
    def test_exports_markdown_files_to_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "raw_exports_all"
            dst = root / "local_md"
            (src / "article-a").mkdir(parents=True)
            (src / "article-b").mkdir(parents=True)

            (src / "article-a" / "a.md").write_text("# A\n", encoding="utf-8")
            (src / "article-b" / "b.md").write_text("# B\n", encoding="utf-8")
            (src / "article-b" / "b.jpg").write_text("img", encoding="utf-8")

            summary = export_markdown_files(src, dst, "苍何", "all")

            self.assertEqual(summary["exported"], 2)
            self.assertTrue((dst / "苍何" / "all").exists())
            exported = list((dst / "苍何" / "all").glob("*.md"))
            self.assertEqual(len(exported), 2)


if __name__ == "__main__":
    unittest.main()
