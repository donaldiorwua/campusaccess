import copy
import unittest
import campusaccess

from campusaccess import workflow

from campusaccess.workflow import (
    approve_request,
    issue_card,
    return_card,
)

class TestApproveRequest(unittest.TestCase):

    def setUp(self):
        # A fresh record before EVERY test, so tests cannot affect each other.
        self.record = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "visitor",
            "status": "requested",
            "approved_by": None,
        }
        workflow.FAKE_RECORDS["A001"] = self.record
        
    # ---- CASE 2 / checkpoint B2 ------------------------------------------
    def test_issue_before_approval_is_rejected_and_record_unchanged(self):
        snapshot = copy.deepcopy(self.record)
        with self.assertRaises(ValueError):
            issue_card("A001")
        self.assertEqual(self.record, snapshot)

    # ---- CASE 3 / checkpoint B3 ------------------------------------------
    def test_blank_approver_is_rejected_and_record_unchanged(self):
        snapshot = copy.deepcopy(self.record)
        with self.assertRaises(ValueError):
            approve_request("A001", None)
        self.assertEqual(self.record, snapshot)

        with self.assertRaises(ValueError):
            approve_request("A001", "   ")
        self.assertEqual(self.record, snapshot)

        with self.assertRaises(ValueError):
            approve_request("A001", "")
        self.assertEqual(self.record, snapshot)

    # ---- CASE 4 / checkpoint B4 ------------------------------------------
    def test_full_workflow_requested_to_returned(self):
        approve_request("A001", "M01")
        self.assertEqual(self.record["status"], "approved")
        self.assertEqual(self.record["approved_by"], "M01")

        issue_card("A001")
        self.assertEqual(self.record["status"], "issued")

        return_card("A001")
        self.assertEqual(self.record["status"], "returned")

    # ---- CASE 5 / checkpoint B5 ------------------------------------------
    def test_double_return_is_rejected(self):
        approve_request("A001", "M01")
        issue_card("A001")
        return_card("A001")
        with self.assertRaises(ValueError):
            return_card("A001")
        self.assertEqual(self.record["status"], "returned")


    def test_issue_after_return_is_rejected(self):
        approve_request("A001", "M01")
        issue_card("A001")
        return_card("A001")
        with self.assertRaises(ValueError):
            issue_card("A001")
        self.assertEqual(self.record["status"], "returned")


    def test_approve_twice_is_rejected(self):
        approve_request("A001", "M01")
        with self.assertRaises(ValueError):
            approve_request("A001", "M02")
        self.assertEqual(self.record["approved_by"], "M01")


if __name__ == "__main__":
    unittest.main()