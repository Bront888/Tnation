"""Ticket assignment, lifecycle transitions, and work-queue operations."""

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def _find_ticket(tickets, ticket_id):
    """Return a ticket by its integer ID, or raise KeyError."""
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    raise KeyError(f"Ticket {ticket_id!r} was not found")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an existing, non-resolved ticket to a named staff member."""
    ticket = _find_ticket(tickets, ticket_id)

    if ticket.get("status") == "resolved":
        raise ValueError("Resolved tickets must be reopened before they can be modified")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name must not be blank")

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Apply an allowed forward status transition to a ticket."""
    ticket = _find_ticket(tickets, ticket_id)

    if not isinstance(new_status, str):
        raise ValueError("Status must be a string")
    target_status = new_status.strip().lower()
    current_status = ticket.get("status")

    if current_status == "resolved":
        raise ValueError("Resolved tickets must be explicitly reopened before modification")
    if target_status == "open":
        raise ValueError("Use reopen_ticket to return a resolved ticket to open")
    if current_status == "open" and target_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError("A ticket must be assigned before it can enter in_progress")
        ticket["status"] = target_status
        return ticket
    if current_status == "in_progress" and target_status == "resolved":
        ticket["status"] = target_status
        return ticket

    raise ValueError(
        f"Invalid status transition: {current_status!r} -> {target_status!r}"
    )


def reopen_ticket(tickets, ticket_id):
    """Explicitly reopen a resolved ticket by setting its status to open."""
    ticket = _find_ticket(tickets, ticket_id)
    if ticket.get("status") != "resolved":
        raise ValueError("Only resolved tickets can be reopened")

    ticket["status"] = "open"
    return ticket


def get_open_queue(tickets):
    """Return open tickets sorted by priority, then ascending numeric ticket ID.

    The input collection is not reordered or otherwise modified.
    """
    def sort_key(ticket):
        priority = ticket.get("priority")
        if priority not in PRIORITY_ORDER:
            raise ValueError(f"Unknown ticket priority: {priority!r}")
        ticket_id = ticket.get("id")
        if isinstance(ticket_id, bool) or not isinstance(ticket_id, int) or ticket_id < 1:
            raise ValueError(f"Ticket ID must be a positive integer: {ticket_id!r}")
        return PRIORITY_ORDER[priority], ticket_id

    open_tickets = [ticket for ticket in tickets if ticket.get("status") == "open"]
    return sorted(open_tickets, key=sort_key)
