"""
Run from the project root:
    python3 -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import main as menu

ID = "A001"
FELLOW_ID = "F001"
CARD_TYPE = "visitor"
STATUS = "requested"
APPROVED_BY = None,

CREATE = ["1", FELLOW_ID, CARD_TYPE]
APPROVE = ["2", "A001", "M01"]
ISSUE = ["3", "A001"]
RETURN = ["4", "A001"]
SAVE_EXIT = ["6"]


class TestWholeProject(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data_file = Path(tmp.name) / "cards.json"
        patcher = mock.patch.object(menu, "DATA_FILE", self.data_file)
        patcher.start()
        self.addCleanup(patcher.stop)

    def use_menu(self, *steps):
        """Type the given steps into the menu, return everything it printed.
        If the menu asks for more input than given, the test errors out."""
        answers = [a for step in steps for a in step]
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=answers):
            with contextlib.redirect_stdout(out):
                menu.run_menu()
        return out.getvalue()

    def saved(self):
        """The saved file as {id: record}."""
        data = json.loads(self.data_file.read_text())
        if isinstance(data, list):
            data = {r["id"]: r for r in data}
        return data

    # CASE 1
    def test_create_request_starts_as_requested(self):
        self.use_menu(CREATE, SAVE_EXIT)
        self.assertEqual(self.saved()["A001"], {
            "id": "A001", "fellow_id": FELLOW_ID, "card_type": CARD_TYPE,
            "status": "requested", "approved_by": None,
        })

    # CASE 2
    def test_issue_before_approval_is_rejected_and_nothing_changes(self):
        self.use_menu(CREATE, SAVE_EXIT)
        before = self.saved()["A001"]
        out = self.use_menu(ISSUE, SAVE_EXIT)
        self.assertIn("Error", out)
        self.assertEqual(self.saved()["A001"], before)

    # CASE 3
    def test_blank_approver_is_rejected_and_nothing_changes(self):
        self.use_menu(CREATE, SAVE_EXIT)
        before = self.saved()["A001"]
        out = self.use_menu(["2", "A001", "   "], SAVE_EXIT)
        self.assertIn("Error", out)
        self.assertEqual(self.saved()["A001"], before)

    # CASE 4
    def test_full_workflow_survives_restart(self):
        self.use_menu(CREATE, APPROVE, ISSUE, RETURN, SAVE_EXIT)
        record = self.saved()["A001"]
        self.assertEqual(record["status"], "returned")
        self.assertEqual(record["approved_by"], "M01")

    # CASE 5
    def test_second_return_and_issue_after_return_are_rejected(self):
        self.use_menu(CREATE, APPROVE, ISSUE, RETURN, SAVE_EXIT)
        before = self.saved()["A001"]
        out = self.use_menu(RETURN, ISSUE, SAVE_EXIT)
        self.assertEqual(out.count("Error"), 2)
        self.assertEqual(self.saved()["A001"], before)

    # CASE 6
    def test_ids_stay_unique_after_restart(self):
        self.use_menu(CREATE, SAVE_EXIT)
        self.use_menu(CREATE, SAVE_EXIT)
        self.assertEqual(set(self.saved()), {"A001", "A002"})

    # CASE 7
    def test_malformed_json_is_reported_and_file_is_not_overwritten(self):
        bad = "{ this is not valid json"
        self.data_file.write_text(bad)
        out = self.use_menu(SAVE_EXIT)   # unused if the menu stops at load
        self.assertIn("error", out.lower())
        self.assertEqual(self.data_file.read_text(), bad)

    # CASE 8
    def test_invalid_menu_options_give_feedback_and_allow_retry(self):
        out = self.use_menu(["abc"], [""], ["99"], SAVE_EXIT)
        self.assertEqual(out.count("not a valid option"), 3)
        self.assertEqual(self.saved(), {})   # still reached save-and-exit

    # unknown ID
    def test_unknown_id_is_rejected_without_crashing(self):
        out = self.use_menu(["2", "A999", "M01"], SAVE_EXIT)
        self.assertIn("Error", out)
        self.assertEqual(self.saved(), {})


if __name__ == "__main__":
    unittest.main()