import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import scripts.reset_notebook as reset_notebook


class ResetNotebookTests(unittest.TestCase):
    def test_test_working_copy_is_distinct_and_requires_force_to_replace(self) -> None:
        source = reset_notebook.find_source_notebooks("0", "test")[0]

        with TemporaryDirectory() as temporary:
            original_working_dir = reset_notebook.WORKING_DIRS["learning"]
            reset_notebook.WORKING_DIRS["learning"] = Path(temporary)
            try:
                created = reset_notebook.reset_notebooks("0", False, "test")
                self.assertEqual(
                    created[0].name,
                    "project1_module_0_python_foundations_test_working.ipynb",
                )
                self.assertNotEqual(created[0], source)
                notebook = json.loads(created[0].read_text(encoding="utf-8"))
                notebook_source = "\n".join(
                    "".join(cell["source"]) for cell in notebook["cells"]
                )
                self.assertIn("graded by AI", notebook_source)
                self.assertIn("awaiting AI review", notebook_source)
                self.assertNotIn("written_points", notebook_source)

                with self.assertRaises(FileExistsError):
                    reset_notebook.reset_notebooks("0", False, "test")

                recreated = reset_notebook.reset_notebooks("0", True, "test")
                self.assertEqual(recreated, created)
            finally:
                reset_notebook.WORKING_DIRS["learning"] = original_working_dir

    def test_analysis_practice_uses_analysis_working_directory(self) -> None:
        source = reset_notebook.find_source_notebooks(
            "0", "practice", "analysis"
        )[0]

        with TemporaryDirectory() as temporary:
            original_working_dir = reset_notebook.WORKING_DIRS["analysis"]
            reset_notebook.WORKING_DIRS["analysis"] = Path(temporary)
            try:
                created = reset_notebook.reset_notebooks(
                    "0", False, "practice", "analysis"
                )
                self.assertEqual(
                    created[0].name,
                    "project1_analysis_module_0_spatial_questions_working.ipynb",
                )
                self.assertNotEqual(created[0], source)
            finally:
                reset_notebook.WORKING_DIRS["analysis"] = original_working_dir


if __name__ == "__main__":
    unittest.main()