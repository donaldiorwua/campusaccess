import unittest
import campusaccess.create_request


class TestRequestCreation(unittest.TestCase):

    def setUp(self):
        # Each test starts with an empty card dictionary.
        self.current_cards = {}

    # Successful creation

    def test_create_first_request(self):
        created_card = campusaccess.create_request.create_card(
            "FE-001", "fellow", self.current_cards
        )

        self.assertEqual(created_card["id"], "A001")
        self.assertEqual(created_card["fellow_id"], "FE-001")
        self.assertEqual(created_card["card_type"], "Fellow")
        self.assertEqual(created_card["request_status"], "requested")
        self.assertIsNotNone(created_card["created_at"])

    def test_request_contains_required_fields(self):
        created_card = campusaccess.create_request.create_card(
            "FE-001", "visitor", self.current_cards
        )

        expected_fields = {
            "id",
            "fellow_id",
            "card_type",
            "request_status",
            "approved_by",
            "created_at",
        }

        self.assertEqual(set(created_card.keys()), expected_fields)

    def test_approver_is_initially_none(self):
        created_card = campusaccess.create_request.create_card(
            "FE-001", "visitor", self.current_cards
        )

        self.assertIn("approved_by", created_card)
        self.assertIsNone(created_card["approved_by"])

    def test_all_valid_card_types(self):
        for card_type in ("fellow", "staff", "visitor", "other"):
            with self.subTest(card_type=card_type):
                current_cards = {}

                created_card = (
                    campusaccess.create_request.create_card(
                        "FE-001", card_type, current_cards
                    )
                )

                self.assertEqual(
                    created_card["card_type"], card_type.title()
                )

    def test_sequential_ids_in_current_session(self):
        first = campusaccess.create_request.create_card(
            "FE-001", "fellow", self.current_cards
        )
        second = campusaccess.create_request.create_card(
            "FE-002", "staff", self.current_cards
        )

        self.assertEqual(first["id"], "A001")
        self.assertEqual(second["id"], "A002")

    def test_request_is_added_to_memory(self):
        created_card = campusaccess.create_request.create_card(
            "FE-001", "visitor", self.current_cards
        )

        self.assertIn(created_card["id"], self.current_cards)
        self.assertEqual(
            self.current_cards[created_card["id"]], created_card
        )

    # Invalid fellow IDs

    def test_reject_blank_fellow_id(self):
        with self.assertRaises((ValueError, TypeError)):
            campusaccess.create_request.create_card(
                "", "fellow", self.current_cards
            )

    def test_reject_whitespace_fellow_id(self):
        with self.assertRaises((ValueError, TypeError)):
            campusaccess.create_request.create_card(
                "   ", "fellow", self.current_cards
            )

    def test_reject_non_string_fellow_id(self):
        for fellow_id in (None, 123, ["FE-001"]):
            with self.subTest(fellow_id=fellow_id):
                with self.assertRaises((ValueError, TypeError)):
                    campusaccess.create_request.create_card(
                        fellow_id, "fellow", self.current_cards
                    )

    def test_reject_malformed_fellow_id(self):
        # Assumes FE-001 is the agreed ID format.
        for fellow_id in ("F", "FE-", "FE-ABC", "001"):
            with self.subTest(fellow_id=fellow_id):
                with self.assertRaises((ValueError, TypeError)):
                    campusaccess.create_request.create_card(
                        fellow_id, "fellow", self.current_cards
                    )

    # Invalid card types

    def test_reject_invalid_card_type(self):
        with self.assertRaises((ValueError, TypeError)):
            campusaccess.create_request.create_card(
                "FE-001", "administrator", self.current_cards
            )

    def test_reject_non_string_card_type(self):
        for card_type in (None, 123, ["fellow", "staff"]):
            with self.subTest(card_type=card_type):
                with self.assertRaises((ValueError, TypeError)):
                    campusaccess.create_request.create_card(
                        "FE-001", card_type, self.current_cards
                    )

    def test_reject_blank_card_type(self):
        for card_type in ("", "   "):
            with self.subTest(card_type=card_type):
                with self.assertRaises((ValueError, TypeError)):
                    campusaccess.create_request.create_card(
                        "FE-001", card_type, self.current_cards
                    )

    # Failed creation must not alter existing records

    def test_invalid_request_does_not_add_record(self):
        campusaccess.create_request.create_card(
            "FE-001", "fellow", self.current_cards
        )
        before = self.current_cards.copy()

        with self.assertRaises((ValueError, TypeError)):
            campusaccess.create_request.create_card(
                "", "visitor", self.current_cards
            )

        self.assertEqual(self.current_cards, before)

    def test_failed_creation_does_not_consume_id(self):
        campusaccess.create_request.create_card(
            "FE-001", "fellow", self.current_cards
        )

        with self.assertRaises((ValueError, TypeError)):
            campusaccess.create_request.create_card(
                "", "visitor", self.current_cards
            )

        created_card = campusaccess.create_request.create_card(
            "FE-002", "staff", self.current_cards
        )

        self.assertEqual(created_card["id"], "A002")


if __name__ == "__main__":
    unittest.main(verbosity=2)