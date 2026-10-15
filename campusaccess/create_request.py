import datetime
import re


def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str):
        raise TypeError("fellow_id must be a string.")

    cleaned_id = fellow_id.strip()

    if not cleaned_id:
        raise ValueError("fellow_id cannot be blank.")

    if not re.fullmatch(r"FE-\d{3}", cleaned_id):
        raise ValueError(
            "fellow_id must follow the format FE-001."
        )

    return cleaned_id

def validate_card_type(card_type):
    if not isinstance(card_type, str):
        raise TypeError("card_type must be a string.")

    cleaned_card_type = card_type.strip().title()

    if not cleaned_card_type:
        raise ValueError("card_type cannot be blank.")

    valid_card_types = {"Fellow", "Staff", "Visitor", "Other"}

    if cleaned_card_type not in valid_card_types:
        raise ValueError(
            "Invalid card_type. Must be Fellow, Staff, Visitor, or Other."
        )

    return cleaned_card_type

def validate_request_status(raw_request):
    cleaned_request_status = raw_request.strip().title()
    request_status = ["Requested", "Approved"]
    if cleaned_request_status not in request_status:
        raise ValueError("Invalid card_type. Must be Fellow, Staff, Visitor, or Other.")
    return cleaned_request_status

def generate_id(current_cards):
    if not current_cards:
        return "A001"

    card_numbers = [
        int(card_id[1:])
        for card_id in current_cards
        if card_id.startswith("A") and card_id[1:].isdigit()
    ]

    next_number = max(card_numbers, default=0) + 1
    return f"A{next_number:03d}"

def create_card(fellow_id, card_type, current_cards):
    validated_fellow_id = validate_fellow_id(fellow_id)
    validated_card_type = validate_card_type(card_type)

    new_id = generate_id(current_cards)
    date_time = datetime.datetime.now().isoformat()

    new_request = {
        "id": new_id,
        "fellow_id": validated_fellow_id,
        "card_type": validated_card_type,
        "request_status": "requested",
        "approved_by": None,
        "created_at": date_time
    }

    current_cards[new_id] = new_request

    return new_request