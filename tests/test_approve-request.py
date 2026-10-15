import copy
import unittest
import campusaccess

from campusaccess import approve-request

from campusaccess.approve-request import (
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
        approve-request.FAKE_RECORDS["A001"] = self.record
        
    # ---- CASE 2 / checkpoint B2 ------------------------------------------
    def test_issue_before_approval_is_rejected_and_record_unchanged(self):
        # Arrange: take a SNAPSHOT of the record. Use copy.deepcopy(...)
        #          so it is a real copy, not the same object.
        # Act:     call issue_card("A001") inside self.assertRaises(ValueError)
        # Assert:  self.record == snapshot (nothing changed)
        self.fail("TODO: write this test")

    # ---- CASE 3 / checkpoint B3 ------------------------------------------
    def test_blank_approver_is_rejected_and_record_unchanged(self):
        # Try approving with "   " (spaces only). Also think: None, "".
        # The record must still be status "requested", approved_by None.
        self.fail("TODO: write this test")

    # ---- CASE 4 / checkpoint B4 ------------------------------------------
    def test_full_workflow_requested_to_returned(self):
        # approve with "M01" -> check status "approved" and approved_by "M01"
        # issue              -> check status "issued"
        # return             -> check status "returned"
        self.fail("TODO: write this test")

    # ---- CASE 5 / checkpoint B5 ------------------------------------------
    def test_double_return_is_rejected(self):
        # Run the full workflow, then call return_card again inside
        # assertRaises. Check the status is STILL "returned".
        self.fail("TODO: write this test")

    def test_issue_after_return_is_rejected(self):
        # Same setup as above, but try issue_card on the returned record.
        self.fail("TODO: write this test")

    def test_approve_twice_is_rejected(self):
        # After a good approval, approving again must fail and keep the
        # first approver's name unchanged.
        self.fail("TODO: write this test")


if __name__ == "__main__":
    unittest.main()