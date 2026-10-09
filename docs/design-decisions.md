Document structure
1. Purpose and scope
   CampusFlow's purpose, six-hour challenge constraints, required features, and out-of-scope items such as databases, web APIs, and third-party frameworks.
2. Architecture and module responsibilities
   CLI versus business logic; responsibilities of tickets, workflow, storage, and reports.
3. Ticket data model
   Field names, types, valid values, initial defaults, input normalization, and ID uniqueness.
4. Priority algorithm
   The four ordered rules, precedence, and boundary cases such as exactly 3 or 10 affected users.
5. Workflow and mutation policy
   Allowed transitions, assignment prerequisite, explicit reopening, and all-mutations restriction for resolved tickets.
6. Queue and reporting semantics
   Open-only filtering, priority/ID ordering, report keys, and zero-count behavior.
7. Persistence and error handling
   JSON format, missing-file behavior, malformed-file handling, ID continuity, and exception contracts.
8. Shared function contracts
   The agreed signatures, return types, and error behavior from Section 1.
9. Team ownership and integration
   Engineer A and B responsibilities, branch conventions, PR requirements, and review expectations.
10. Testing and acceptance
    Validation boundaries, workflow failures, persistence reloads, sorting, empty reports, and the full test command.
11. AI learning and verification
    Link to the AI learning log, verification methods, rejected suggestions, and the required documented correction or rejection.