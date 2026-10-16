# Creation request Dictionary:
request = {
    "id": "A001",
    "fellow_id": "FE-001",
    "card_type": "visitor",
    "request_status": "requested",
    "approved_by": None,
    "created_at": "2026-10-14T10:17:00"
}

# JSON Data Persistent:
request = [
        {
        "id": "A001",
        "fellow_id": "FE-001",
        "card_type": "visitor",
        "request_status": "requested",
        "approved_by": None,
        "created_at": "2026-10-14T10:17:00"
    },
        request = {
        "id": "A002",
        "fellow_id": "FE-002",
        "card_type": "visitor",
        "request_status": "requested",
        "approved_by": None,
        "created_at": "2026-10-14T10:17:00"
    }
]

# Signatures:
## Engineer A:
create_request(fellow_id, card_type):

get_request(request_id):

save_requests(cards, file_path):

load_requests(file_path):


## Engineer B:
approve_request(request_id, approved_by):

 issue_card(request_id):

 return_card(request_id):

 run_menu()

 # Module names
    campusaccess/create_request
    campusaccess/storage
    campusaccess/workflow

    test/test_create_request
    test/test_storage
    test/test_workflow