import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import scripts.save_attempt as save_attempt


class SaveAttemptTests(unittest.TestCase):
    def test_completed_working_copy_is_preserved_with_outputs(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            working_dir = root / "working"
            attempt_dir = root / "attempts"
            working_dir.mkdir()
            working_path = (
                working_dir
                / "project1_module_0_python_foundations_test_working.ipynb"
            )
            notebook = {
                "cells": [
                    {
                        "cell_type": "code",
                        "execution_count": 3,
                        "metadata": {"language": "python"},
                        "outputs": [{"output_type": "stream", "name": "stdout", "text": ["PASS\n"]}],
                        "source": ["print('PASS')"],
                    }
                ],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
            working_path.write_text(json.dumps(notebook), encoding="utf-8")

            original_working_dir = save_attempt.WORKING_DIRS["learning"]
            original_attempt_dir = save_attempt.ATTEMPT_DIRS["learning"]
            save_attempt.WORKING_DIRS["learning"] = working_dir
            save_attempt.ATTEMPT_DIRS["learning"] = attempt_dir
            try:
                created = save_attempt.save_attempts("0", False, "test")
                self.assertEqual(
                    created[0].name,
                    "project1_module_0_python_foundations_test_attempt.ipynb",
                )
                self.assertEqual(
                    json.loads(created[0].read_text(encoding="utf-8")), notebook
                )

                with self.assertRaises(FileExistsError):
                    save_attempt.save_attempts("0", False, "test")

                recreated = save_attempt.save_attempts("0", True, "test")
                self.assertEqual(recreated, created)
            finally:
                save_attempt.WORKING_DIRS["learning"] = original_working_dir
                save_attempt.ATTEMPT_DIRS["learning"] = original_attempt_dir

    def test_practice_and_test_working_copies_are_selected_independently(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            working_dir = root / "working"
            attempt_dir = root / "attempts"
            working_dir.mkdir()
            notebook = {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
            practice_path = (
                working_dir / "project1_module_0_python_foundations_working.ipynb"
            )
            test_path = (
                working_dir
                / "project1_module_0_python_foundations_test_working.ipynb"
            )
            practice_path.write_text(json.dumps(notebook), encoding="utf-8")
            test_path.write_text(json.dumps(notebook), encoding="utf-8")

            original_working_dir = save_attempt.WORKING_DIRS["learning"]
            original_attempt_dir = save_attempt.ATTEMPT_DIRS["learning"]
            save_attempt.WORKING_DIRS["learning"] = working_dir
            save_attempt.ATTEMPT_DIRS["learning"] = attempt_dir
            try:
                practice = save_attempt.save_attempts("0", False, "practice")
                test = save_attempt.save_attempts("0", False, "test")
                self.assertEqual(
                    [path.name for path in practice],
                    ["project1_module_0_python_foundations_attempt.ipynb"],
                )
                self.assertEqual(
                    [path.name for path in test],
                    ["project1_module_0_python_foundations_test_attempt.ipynb"],
                )
            finally:
                save_attempt.WORKING_DIRS["learning"] = original_working_dir
                save_attempt.ATTEMPT_DIRS["learning"] = original_attempt_dir


if __name__ == "__main__":
    unittest.main()
