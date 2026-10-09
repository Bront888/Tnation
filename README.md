# CampusFlow

CampusFlow is a standard-library Python command-line ticket tracker built for the AI-Native Engineering Sprint.

## Scope

- Create and view support tickets.
- Calculate priority from urgency and affected-user count.
- Assign tickets and enforce the ticket lifecycle.
- Display an open-only queue sorted by priority and numeric ID.
- Report totals and breakdowns by status and priority.
- Persist tickets to JSON.

## Constraints

- Python standard library only for the application and tests.
- `unittest` for automated tests and `json` for persistence.
- No database, web API, or third-party application framework.

## Team

- Engineer A: Bront888 — ticket foundation and JSON persistence.
- Engineer B: chikafor — assignment, workflow, queue, and reports.

## Locked design decisions

- Queue policy: `open-only`.
- Resolved-ticket policy: all mutations are blocked until an explicit reopen.
- Storage owner: Engineer A; both engineers agree on and test the persistence contract.

See [docs/design-decisions.md](docs/design-decisions.md) for the shared data model, function contracts, error behavior, and acceptance rules.

## Run tests

```bash
python -m unittest discover -s tests -v
```

The implementation and test modules will be added during the sprint.
