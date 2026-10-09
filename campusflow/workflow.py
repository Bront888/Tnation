# ticket assignment, workflow transitions, reopening, and queue ordering.

from .tickets import PRIORITY_ORDER, find_ticket

VALID_STATUSES = {"open", "in_progress". "resolved"}


def assign_ticket(tickets, ticket_id, staff_name):
    # assign or reassign a ticket that has not been resolved
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Resolved tickets must be reopened before reassignment.")

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be blank.")

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    # apply an allowed transition to to a ticket
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen a resolved ticket before changing its status")

    if not isinstance(new_status, str):
        raise ValueError("Status must be a string.")

    new_status = new_status.strip().casefold()

    if new_status not in VALID_STATUSES:
        raise ValueError(
            "Invalid status. Choose open, in_progress, or resolved."
        )
    
    current_status = ticket["status"]

    allowed_transitions = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": set(),
    }

    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign the ticket before marking it in progress.")

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    # explicitly reopen a resolved ticket.
    ticket = find_ticket(tickets, ticket_id)

    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket


def get_open_queue(tickets):
    # return open tickets by priority, then ascending numeric ID.
    queue = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]    

    queue.sort(
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]]
            ticket("id")
        )
    )
    return queue