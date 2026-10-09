
#JSON persistence for CampusFlow tickets.

import json
import os
import tempfile
from pathlib import Path

from .tickets import calculate_priority


class StorageError(Exception):
    #Raised when ticket data cannot be safely loaded or saved.


REQUIRED_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_STATUSES = {"open", "in_progress", "resolved"}


def _validate_tickets(tickets):
    #Reject invalid records before loading or saving them.
    if not isinstance(tickets, list):
        raise StorageError("Ticket data must be a JSON list.")

    seen_ids = set()

    for index, ticket in enumerate(tickets):
        location = f"Ticket at index {index}"

        if not isinstance(ticket, dict):
            raise StorageError(f"{location} must be an object.")

        missing = REQUIRED_FIELDS - ticket.keys()
        if missing:
            fields = ", ".join(sorted(missing))
            raise StorageError(f"{location} is missing fields: {fields}.")

        ticket_id = ticket["id"]
        if (
            isinstance(ticket_id, bool)
            or not isinstance(ticket_id, int)
            or ticket_id <= 0
        ):
            raise StorageError(
                f"{location} has an invalid positive integer ID."
            )

        if ticket_id in seen_ids:
            raise StorageError(
                f"Duplicate ticket ID {ticket_id} in stored data."
            )
        seen_ids.add(ticket_id)

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise StorageError(f"{location} has an invalid title.")

        if ticket["category"] not in VALID_CATEGORIES:
            raise StorageError(f"{location} has an invalid category.")

        if ticket["urgency"] not in VALID_URGENCIES:
            raise StorageError(f"{location} has an invalid urgency.")

        users = ticket["affected_users"]
        if (
            isinstance(users, bool)
            or not isinstance(users, int)
            or users <= 0
        ):
            raise StorageError(
                f"{location} has an invalid affected_users value."
            )

        if ticket["priority"] not in VALID_PRIORITIES:
            raise StorageError(f"{location} has an invalid priority.")

        expected_priority = calculate_priority(ticket["urgency"], users)
        if ticket["priority"] != expected_priority:
            raise StorageError(
                f"{location} has priority {ticket['priority']!r}; "
                f"expected {expected_priority!r}."
            )

        if ticket["status"] not in VALID_STATUSES:
            raise StorageError(f"{location} has an invalid status.")

        assigned_to = ticket["assigned_to"]
        if assigned_to is not None and (
            not isinstance(assigned_to, str) or not assigned_to.strip()
        ):
            raise StorageError(
                f"{location} has an invalid assigned_to value."
            )


def load_tickets(path):
    # Load and validate tickets; a missing file means a fresh start.
    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise StorageError(
            f"Cannot read ticket data from {file_path}: invalid JSON."
        ) from exc
    except OSError as exc:
        raise StorageError(
            f"Cannot read ticket data from {file_path}: {exc}"
        ) from exc

    _validate_tickets(tickets)
    return tickets


def save_tickets(path, tickets):
    #Validate and atomically save tickets as JSON.
    _validate_tickets(tickets)
    file_path = Path(path)
    temporary_path = None

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(tickets, temporary_file, indent=2, ensure_ascii=False)
            temporary_file.write("\n")

        os.replace(temporary_path, file_path)
    except (OSError, TypeError, ValueError) as exc:
        raise StorageError(
            f"Cannot save ticket data to {file_path}: {exc}"
        ) from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
