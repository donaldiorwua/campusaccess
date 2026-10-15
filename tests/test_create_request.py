
import unittest
from campusaccess.create_request import create_card as request


class TestRequestCreation(unittest.TestCase):

    def setUp(self):
        self.original_requests = request.requests.copy()
        request.requests.clear()

    def tearDown(self):
        request.requests.clear()
        request.requests.update(self.original_requests)

    # Successful creation

    def test_create_first_request(self):
        request = request.create_request("FE-001", "fellow")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "FE-001")
        self.assertEqual(request["card_type"], "fellow")
        self.assertEqual(request["request_status"], "requested")
        self.assertIsNotNone(request["created_at"])

    def test_request_contains_required_fields(self):
        request = request.create_request("FE-001", "visitor")

        expected_fields = {
            "id",
            "fellow_id",
            "card_type",
            "request_status",
            "created_at",
        }

        self.assertEqual(set(request.keys()), expected_fields)

    def test_approver_is_initially_none_if_included_in_schema(self):
        request = request.create_request("FE-001", "visitor")

        # The shared approval workflow requires this field.
        self.assertIn("approved_by", request)
        self.assertIsNone(request["approved_by"])

    def test_all_valid_card_types(self):
        for card_type in ("fellow", "staff", "visitor", "other"):
            with self.subTest(card_type=card_type):
                request.requests.clear()

                request = request.create_request("FE-001", card_type)

                self.assertEqual(request["card_type"], card_type)

    def test_sequential_ids_in_current_session(self):
        first = request.create_request("FE-001", "fellow")
        second = request.create_request("FE-002", "staff")

        self.assertEqual(first["id"], "A001")
        self.assertEqual(second["id"], "A002")

    def test_request_is_added_to_memory(self):
        request = request.create_request("FE-001", "visitor")

        self.assertIn(request["id"], request.requests)

    # Invalid fellow IDs

    def test_reject_blank_fellow_id(self):
        with self.assertRaises((ValueError, TypeError)):
            request.create_request("", "fellow")

    def test_reject_whitespace_fellow_id(self):
        with self.assertRaises((ValueError, TypeError)):
            request.create_request("   ", "fellow")

    def test_reject_non_string_fellow_id(self):
        for fellow_id in (None, 123, ["FE-001"]):
            with self.subTest(fellow_id=fellow_id):
                with self.assertRaises((ValueError, TypeError)):
                    request.create_request(fellow_id, "fellow")

    def test_reject_malforequested_fellow_id(self):
        # Assumes FE-001 is the agreed forequestat.
        for fellow_id in ("F", "FE-", "FE-ABC", "001"):
            with self.subTest(fellow_id=fellow_id):
                with self.assertRaises((ValueError, TypeError)):
                    request.create_request(fellow_id, "fellow")

    # Invalid card types

    def test_reject_invalid_card_type(self):
        with self.assertRaises((ValueError, TypeError)):
            request.create_request("FE-001", "administrator")

    def test_reject_non_string_card_type(self):
        for card_type in (None, 123, ["fellow", "staff"]):
            with self.subTest(card_type=card_type):
                with self.assertRaises((ValueError, TypeError)):
                    request.create_request("FE-001", card_type)

    def test_reject_blank_card_type(self):
        for card_type in ("", "   "):
            with self.subTest(card_type=card_type):
                with self.assertRaises((ValueError, TypeError)):
                    request.create_request("FE-001", card_type)

    # Failed creation must not alter existing records

    def test_invalid_request_does_not_add_record(self):
        request.create_request("FE-001", "fellow")
        before = request.requests.copy()

        with self.assertRaises((ValueError, TypeError)):
            request.create_request("", "visitor")

        self.assertEqual(request.requests, before)

    def test_failed_creation_does_not_consume_id(self):
        request.create_request("FE-001", "fellow")

        with self.assertRaises((ValueError, TypeError)):
            request.create_request("", "visitor")

        request = request.create_request("FE-002", "staff")

        self.assertEqual(request["id"], "A002")


if __name__ == "__main__":
    unittest.main(verbosity=2)
