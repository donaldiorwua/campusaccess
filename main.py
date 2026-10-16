from pathlib import Path

from campusaccess.create_request import (
    create_card,
)

from campusaccess.storage import (
    load_requests,
    save_requests,
)

from campusaccess.workflow import (
    approve_request,
    issue_card,
    return_card,
)

DATA_FILE = Path(__file__).resolve().parent / "data" / "cards.json"

def load_application_data():
    try:
        return load_requests(DATA_FILE)
    except FileNotFoundError:
        return {}


def save_application_data(cards):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    save_requests(cards, DATA_FILE)


def display_cards(cards):
    if not cards:
        print("cards not found.")
        return

    for card_id, record in cards.items():
        print(f"\n{card_id}")
        for field, value in record.items():
            print(f"  {field.replace('_', ' ').title()}: {value}")
    

def run_menu():
    try:
        cards = load_application_data()
    except (ValueError, OSError) as e:
        print("Error: could not load the data file:", e)
        print("Fix or remove the file, then start again. Nothing was changed.")
        return

    try:
        while True:
            print("1. Create cards")
            print("2. Approve request")
            print("3. Issue card")
            print("4. Return card")
            print("5. Display Cards")
            print("6. save and Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                fellow_id = input("Fellow ID: ").strip()
                card_type = input("Card type (visitor/student/staff): ").strip()
                try:
                    new_request = create_card(fellow_id, card_type, cards)
                    print("Request created:", new_request)
                    print()
                except ValueError as e:
                    print("Error:", e)
                    print()

            elif choice == "2":
                request_id = input("Request ID: ").strip()
                approved_by = input("Approved by: ")
                try:
                    approve_request(cards, request_id, approved_by)
                    print("Request Approved!")
                    print()
                except ValueError as e:
                    print("Error:", e)
                    print()

            elif choice == "3":
                request_id = input("Request ID: ").strip()
                try:
                    issue_card(cards, request_id)
                    print("Card Issued!")
                    print()
                except ValueError as e:
                    print("Error:", e)
                    print()

            elif choice == "4":
                request_id = input("Request ID: ").strip()
                try:
                    return_card(cards, request_id)
                    print("Card Returned!")
                    print()
                except ValueError as e:
                    print("Error:", e)
                    print()

            elif choice == "5":
                display_cards(cards)

            elif choice == "6":
                try:
                    save_application_data(cards)
                    print("Cards Saved!")
                    print("Exiting...")
                    break
                except (ValueError, OSError) as e:
                    print("Error:", e)
                    print()
           
            else:
                print(f"\n'{choice}' is not a valid option. Please enter 1, 2, 3, 4, 5, or 6.")
                print()

    except (EOFError, KeyboardInterrupt):
        print("\n Interrupted. Unsaved changes were not saved.")


if __name__ == "__main__":
    run_menu()    