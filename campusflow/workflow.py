"""Assignment, ticket lifecycle, and open-queue operations.

Business functions in this module do not perform CLI input/output.
"""

from __future__ import annotations

from typing import Any, Iterable

Ticket = dict[str, Any]

_VALID_STATUSES = {"open", "in_progress", "resolved"}
_PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _find_ticket(tickets: Iterable[Ticket], ticket_id: int) -> Ticket:
    """Return a ticket by its integer ID, or raise KeyError."""
    if isinstance(ticket_id, bool) or not isinstance(ticket_id, int):
        raise KeyError(ticket_id)

    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    raise KeyError(ticket_id)


def assign_ticket(
    tickets: list[Ticket], ticket_id: int, staff_name: str
) -> Ticket:
    """Assign a ticket to a nonblank staff name.

    Resolved tickets are immutable until explicitly reopened.
    """
    ticket = _find_ticket(tickets, ticket_id)

    if ticket.get("status") == "resolved":
        raise ValueError("Resolved tickets must be reopened before reassignment.")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank.")

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(
    tickets: list[Ticket], ticket_id: int, new_status: str
) -> Ticket:
    """Apply an allowed forward status transition to a ticket."""
    ticket = _find_ticket(tickets, ticket_id)

    if ticket.get("status") == "resolved":
        raise ValueError("Resolved tickets must be reopened before modification.")
    if not isinstance(new_status, str):
        raise ValueError("Status must be a string.")

    requested_status = new_status.strip().lower()
    if requested_status not in _VALID_STATUSES:
        raise ValueError(
            f"Invalid status {new_status!r}. Expected open, in_progress, or resolved."
        )

    current_status = ticket.get("status")
    allowed_next = {
        "open": "in_progress",
        "in_progress": "resolved",
    }
    if allowed_next.get(current_status) != requested_status:
        raise ValueError(
            f"Invalid status transition: {current_status!r} -> {requested_status!r}."
        )
    if requested_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("A ticket must be assigned before it can be in progress.")

    ticket["status"] = requested_status
    return ticket


def reopen_ticket(tickets: list[Ticket], ticket_id: int) -> Ticket:
    """Explicitly reopen a resolved ticket, setting its status to open."""
    ticket = _find_ticket(tickets, ticket_id)
    if ticket.get("status") != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")

    ticket["status"] = "open"
    return ticket


def get_open_queue(tickets: list[Ticket]) -> list[Ticket]:
    """Return open tickets sorted by priority, then ascending numeric ID.

    The source list is not reordered. Only tickets with status exactly 'open'
    are included.
    """
    open_tickets = [ticket for ticket in tickets if ticket.get("status") == "open"]

    def sort_key(ticket: Ticket) -> tuple[int, int]:
        priority = ticket.get("priority")
        ticket_id = ticket.get("id")
        if priority not in _PRIORITY_ORDER:
            raise ValueError(f"Unknown ticket priority: {priority!r}.")
        if (
            isinstance(ticket_id, bool)
            or not isinstance(ticket_id, int)
            or ticket_id < 1
        ):
            raise ValueError(f"Ticket ID must be a positive integer; got {ticket_id!r}.")
        return (_PRIORITY_ORDER[priority], ticket_id)

    return sorted(open_tickets, key=sort_key)
