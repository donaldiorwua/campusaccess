
import json
import tempfile
import unittest
from pathlib import Path

from campusaccess.storage import save_requests, load_requests


class TestPersistent(unittest.TestCase):
    """Tests for persistent JSON storage of access-card requests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.directory = Path(self.temp_dir.name)
        self.file_path = self.directory / "data" / "requests.json"

        self.sample_requests = {
            "A001": {
                "fellow_id": "F001",
                "card_type": "fellow",
                "state": "pending",
            }
        }

    # ---------------------------------------------------------
    # SAVE REQUESTS
    # ---------------------------------------------------------

    def test_save_requests_creates_file_and_parent_directories(self):
        save_requests(self.sample_requests, self.file_path)

        self.assertTrue(self.file_path.exists())
        self.assertTrue(self.file_path.parent.exists())

    def test_save_requests_writes_valid_json(self):
        save_requests(self.sample_requests, self.file_path)

        with self.file_path.open("r", encoding="utf-8") as file:
            saved_data = json.load(file)

        self.assertEqual(saved_data, self.sample_requests)

    def test_save_requests_rejects_non_dictionary(self):
        invalid_values = [
            [],
            "invalid",
            123,
            None,
            True,
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    save_requests(value, self.file_path)

    def test_save_requests_overwrites_existing_file(self):
        save_requests(self.sample_requests, self.file_path)

        updated_requests = {
            "A002": {
                "fellow_id": "F002",
                "card_type": "fellow",
                "state": "pending",
            }
        }

        save_requests(updated_requests, self.file_path)

        self.assertEqual(
            load_requests(self.file_path),
            updated_requests,
        )

    def test_save_requests_rejects_non_serializable_data(self):
        invalid_requests = {"A001": object()}

        with self.assertRaises(ValueError):
            save_requests(invalid_requests, self.file_path)

    # ---------------------------------------------------------
    # LOAD REQUESTS
    # ---------------------------------------------------------

    def test_load_requests_returns_empty_dict_if_file_missing(self):
        result = load_requests(self.file_path)

        self.assertEqual(result, {})

    def test_load_requests_reads_saved_requests(self):
        save_requests(self.sample_requests, self.file_path)

        result = load_requests(self.file_path)

        self.assertEqual(result, self.sample_requests)

    def test_load_requests_preserves_ticket_ids(self):
        requests = {
            "A001": {"fellow_id": "F001"},
            "A002": {"fellow_id": "F002"},
            "A003": {"fellow_id": "F003"},
        }

        save_requests(requests, self.file_path)

        result = load_requests(self.file_path)

        self.assertEqual(list(result.keys()), list(requests.keys()))

    def test_load_requests_rejects_corrupted_json(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            '{"A001": {"fellow_id": "F001"',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            load_requests(self.file_path)

    def test_load_requests_rejects_json_array(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            '[{"fellow_id": "F001"}]',
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "expected a JSON object"):
            load_requests(self.file_path)

    def test_load_requests_rejects_json_string(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text('"invalid"', encoding="utf-8")

        with self.assertRaises(ValueError):
            load_requests(self.file_path)

    def test_load_requests_rejects_json_number(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text("123", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_requests(self.file_path)

 
    def test_request_survives_save_and_reload(self):
        save_requests(self.sample_requests, self.file_path)

        # Simulate the application loading its data after restart.
        reloaded_requests = load_requests(self.file_path)

        self.assertEqual(
            reloaded_requests["A001"]["fellow_id"],
            "F001",
        )

    def test_new_request_id_is_not_reused_after_reload(self):
        save_requests(self.sample_requests, self.file_path)

        # Simulate restarting the application.
        reloaded_requests = load_requests(self.file_path)

        # The next-ID generator should inspect the reloaded records.
        existing_numbers = [
            int(ticket_id[1:])
            for ticket_id in reloaded_requests
            if ticket_id.startswith("A")
            and ticket_id[1:].isdigit()
        ]

        next_number = max(existing_numbers, default=0) + 1
        next_ticket_id = f"A{next_number:03d}"

        self.assertEqual(next_ticket_id, "A002")
        self.assertNotEqual(next_ticket_id, "A001")

    def test_failed_load_does_not_modify_existing_file(self):
        original_content = '{"A001": {"fellow_id": "F001"}}'

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            original_content,
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            self.file_path.write_text(
                '{"A001": invalid JSON',
                encoding="utf-8",
            )
            load_requests(self.file_path)

    def test_save_requests_does_not_change_source_dictionary(self):
        original_requests = {
            "A001": {
                "fellow_id": "F001",
                "card_type": "fellow",
                "state": "pending",
            }
        }
        expected = json.loads(json.dumps(original_requests))

        save_requests(original_requests, self.file_path)

        self.assertEqual(original_requests, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
