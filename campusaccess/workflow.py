# def approve_request():, is legal only if the records current status is requested for that operation.
# def issue_card():, is legal only if the records current status is approved for that operation.
# def return_card():, is legal only if the records current status is issued for that operation.
# requested → approved → issued → returned

def get_record(cards, request_id):
    if request_id not in cards:
        raise ValueError(f"Unknown record ID: {request_id}")
    return cards[request_id]

def approve_request(cards, request_id, approved_by): 
    record = get_record(cards, request_id)

    if record["status"] != "requested": 
        raise ValueError(f"Cannot approve: status must be 'requested', but it is '{record['status']}'.") 
    if approved_by is None or approved_by.strip() == "": 
        raise ValueError("Approved_by is required")

    record["status"] = "approved"
    record["approved_by"] = approved_by.strip()

def issue_card(cards, request_id):
    record = get_record(cards, request_id)

    if record["status"] != "approved":
        raise ValueError(f"Cannot Issue: status must be 'approved', but it is '{record['status']}'.") 
    if record["approved_by"] is None or record["approved_by"].strip() == "": 
        raise ValueError("Cannot issue: this request has no approver on record")
    
    record["status"] = "issued"

def return_card(cards, request_id):
    record = get_record(cards, request_id)

    if record["status"] != "issued":
        raise ValueError(f"Cannot return: status must be 'issued', but it is '{record['status']}'.")
    
    record["status"] = "returned"
