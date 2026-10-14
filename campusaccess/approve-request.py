# def approve_request():, is legal only if the records current status is requested for that operation.
# def issue_card():, is legal only if the records current status is approved for that operation.
# def return_card():, is legal only if the records current status is issued for that operation.

def approve_request(request_id, approved_by): 
    record = "find the record using A's lookup" 
    if record["status"] != "requested": 
        raise ValueError("record is not available") 
    if approved_by is None or approved_by.strip() == "": 
        raise ValueError("Approved_by is required")

    record["approved"] = "borrowed"
    record["borrowed_by"] = approved_by.strip()
    # changed_record = the current record 