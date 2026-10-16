# Card Request Management System

## Project Overview

The Card Request Management System is a Python application designed to create, validate, track, and store card requests for fellows, staff, visitors, and other users. It maintains request records, assigns unique sequential IDs, tracks request status, and supports saving and loading records using JSON files.

Key Features

Card Creation: Creates new card requests using the required user information.

Input Validation: Validates fellow IDs, card types, and required fields before creating a record.

Unique Request IDs: Generates sequential IDs such as A001, A002, and A003.

Request Status Tracking: Assigns an initial status of requested to each new card.

Approval Tracking: Includes an approved_by field, initially set to None.

Timestamp Recording: Records the creation date and time using an ISO-formatted timestamp.

In-Memory Storage: Maintains card requests in a Python dictionary during execution.

JSON Persistence: Saves records to JSON files and loads them back when needed.

Error Handling: Handles invalid inputs, file errors, and invalid or corrupted JSON data.

Automated Testing: Tests valid and invalid inputs, sequential IDs, record preservation, and persistence operations.

A card request contains fields such as:

{
    "request_id": "A001",
    "fellow_id": "FE-001",
    "card_type": "Fellow",
    "request_status": "requested",
    "approved_by": None,
    "created_at": "2026-10-15T10:30:00"
}

# create_card() Function

The create_card(fellow_id, card_type, current_cards) function creates a new card request.

How it works:

Receives the fellow's ID, requested card type, and existing card records.

Validates the supplied information to ensure it meets the application's requirements.

Generates the next sequential request ID based on existing records.

Creates a record containing the request details, initial status, approval information, and timestamp.

Stores the new record in the current_cards dictionary.

Returns the newly created record.

create_card()

The create_card(fellow_id, card_type, current_cards) function creates a new card request.

How it works:

Receives the fellow's ID, requested card type, and existing card records.

Validates the supplied information to ensure it meets the application's requirements.

Generates the next sequential request ID based on existing records.

Creates a record containing the request details, initial status, approval information, and timestamp.

Stores the new record in the current_cards dictionary.

Returns the newly created record.

Example usage:

current_cards = {}

card = create_card(
    "FE-001",
    "Fellow",
    current_cards
)

print(card)

The function returns the newly created card record and stores it in current_cards. Invalid input should be rejected before the dictionary is modified, preventing failed requests from corrupting existing records or consuming request IDs.

# Data Persistence

The system uses two main functions:

save_requests(cadrs, file_path): Saves request records from a dictionary to a JSON file.

load_requests(file_path): Loads saved request records from a JSON file into the application.

These functions allow records to be retained between application sessions instead of being lost when the program exits.

Testing

The project uses automated tests to verify:

Successful creation of valid card requests.

Rejection of invalid IDs, card types, and missing required values.

Sequential request ID generation.

Preservation of existing records when creation fails.

Successful saving and loading of JSON records.

Appropriate handling of missing files and corrupted JSON data.

Technologies

Python 3.13

Dictionaries for in-memory data management

JSON for data persistence

pathlib for file path handling

unittest for automated testing

Usage:

python3 main.py


Testing:

python3  -m unittest discover -s tests -v