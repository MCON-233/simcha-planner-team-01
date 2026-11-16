# Contributing to the Simcha Planner

This repository belongs to one project team. Every team member is responsible
for the quality of the shared product and must contribute through Jira, Git,
pull requests, reviews, and testing.

## Before beginning an item

- Confirm that the item belongs to the current Sprint.
- Read its description and acceptance criteria.
- Ask questions during backlog refinement if the work is unclear.
- Assign the item to yourself and move it from **To Do** to **In Progress**.
- Pull the latest default branch before creating your branch.

## Branches

Create one short-lived branch for one focused Jira item. Include the Jira issue
key when it is available.

Examples:

```text
MC233-12-homepage-introduction
MC233-18-visible-focus-styles
MC233-25-homepage-route-test
```

Do not commit directly to the default branch unless the instructor explicitly
directs you to do so.

## Commits

Commit a coherent change with a concise message that explains its purpose.

```text
Add supported simcha types to homepage
Improve keyboard focus visibility
Test successful homepage response
```

Do not commit `.env`, virtual environments, IDE settings, credentials, or
generated cache files.

## Pull requests

Before opening a pull request:

1. Run `python -m pytest` locally.
2. Review your own changes.
3. Push the branch.
4. Open a pull request linked to the Jira item.
5. Explain what changed and how to verify it.
6. Move the Jira item to **Pull Request**.
7. Request review from at least one teammate.

The author responds to review comments and does not approve her own pull
request. Merge only after the reviewer approves it and GitHub Actions passes.

## QA verification

Passing tests do not automatically make a Story complete. A teammate who did
not implement the Story must verify each acceptance criterion and record the
result in the pull request or Jira item.

## Jira workflow

```text
To Do → In Progress → Pull Request → Done
```

- **To Do:** Refined, understood, and ready to begin.
- **In Progress:** A team member is actively working on it.
- **Pull Request:** Implementation is complete and awaiting review, tests, or
  QA verification.
- **Done:** Reviewed, merged, successfully built, and verified.

## Definition of Done

An item may move to **Done** only when all applicable statements are true:

- [ ] The agreed requirements are implemented.
- [ ] Relevant automated tests were added or updated.
- [ ] `python -m pytest` passes locally.
- [ ] The pull request explains the change and how to verify it.
- [ ] At least one teammate approved the pull request.
- [ ] The GitHub Actions build passes.
- [ ] The change is merged into the default branch.
- [ ] Another team member verified the Story's acceptance criteria.
- [ ] The deployed version was checked when deployment is part of the Story.
- [ ] Jira and relevant documentation are current.

## Individual accountability

Every student must be prepared to locate, run, explain, debug, and modify her
contribution. A team submission does not remove individual responsibility.
