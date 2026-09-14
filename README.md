# MCON-233 Simcha Planner

This is the starter repository for the Fall 2026 MCON-233 group project. Each
team will incrementally design, test, secure, and deploy its own AI-enabled
Simcha Planner using Python and Flask.

The project continues the development workflow introduced in Lesson 1: work in
a Python 3.12+ virtual environment, install dependencies from
`requirements.txt`, run tests locally, protect credentials, and submit work
through Git. Lesson 1 was an individual exercise; this is a group project.

## One assignment, separate team repositories

The CS++ group assignment is shared by the class, but teams do **not** all work
in one repository. When you join your assigned team, CS++ creates or assigns a
separate repository for that team.

```text
Shared Simcha Planner assignment
├── Team One repository
├── Team Two repository
└── Team Three repository
```

Before cloning, verify that the repository URL belongs to your assigned team.
Do not create a new team, join a different team, or clone this instructor
template unless your instructor directs you to do so.

Every team member clones the same **team repository** to her own development
environment. Team members collaborate through branches, commits, pull requests,
reviews, and the shared Jira backlog.

## Product vision

The Simcha Planner will help a user organize an event such as a bar/bat mitzvah,
vort, sheva brachos, community dinner, or birthday celebration. Over the
semester, teams will add event details, a checklist and timeline, a budget, and
a focused AI planning assistant.

The first sprint is intentionally small: create an accessible public homepage
that clearly introduces the product. Database models, authentication, AI
integration, and event-planning features belong to later sprints.

## Sprint 1 goal

> Deliver an accessible Simcha Planner homepage that explains the product,
> passes its automated tests, and is ready to deploy publicly.

### Homepage Story

> As a visitor, I want to understand what the Simcha Planner does so that I can
> decide whether I want to use it.

### Acceptance criteria

- The page identifies the product as the Simcha Planner.
- The page explains what information users will be able to organize.
- The page identifies several supported types of simchas.
- The page contains a clear **Start Planning** call to action.
- The page uses meaningful headings, landmarks, labels, and accessible color
  contrast.
- Keyboard focus is visible and the page can be operated without a mouse.
- The layout works on both narrow and wide screens.
- A test confirms that the `/` route returns HTTP status `200`.
- The page is available at the team's public Render URL by the end of Sprint 1.

The starter supplies an accessible document shell and a placeholder page. Your
team must design and implement the actual homepage and its homepage test.

## Visual customization

The starter's appearance is only a foundation. Your team is expected to give
its application a distinct visual identity. You may change:

- The color palette and typography
- Page spacing, borders, cards, and layout
- The header's content and appearance
- The footer's content and appearance
- Navigation labels and presentation
- The placement and styling of the call to action
- Other visual details that support your team's design

You may edit both `app/templates/base.html` and
`app/static/css/styles.css`. You may also add appropriate static assets. Keep
all required homepage content and preserve the application's accessibility:

- Keep a working skip link and a clearly identified main-content area.
- Use semantic headings and landmarks in a logical order.
- Maintain sufficient color contrast.
- Provide visible keyboard focus styles.
- Add meaningful alternative text to informative images.
- Do not communicate important information through color alone.
- Confirm that the page remains usable on narrow and wide screens.

The header and footer do not need to look like the starter. They should look
intentional, fit the team's interpretation of the Simcha Planner, and remain
consistent across application pages.

## Project structure

```text
simcha-planner/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── routes.py            # Application routes
│   ├── templates/
│   │   ├── base.html        # Shared accessible page shell
│   │   └── index.html       # Sprint 1 placeholder
│   └── static/
│       └── css/
│           └── styles.css   # Small accessible style foundation
├── tests/
│   └── test_health.py       # Starter smoke test
├── .github/
│   └── workflows/
│       └── tests.yml        # Continuous-integration build
├── .gitignore
├── requirements.txt
├── run.py                   # Local development entry point
├── wsgi.py                  # Production entry point
├── CONTRIBUTING.md          # Team workflow and Definition of Done
└── README.md
```

## Continue from Lesson 1

Use the same Python and Git skills you practiced in Lesson 1. Clone your new
team repository into your MCON-233 working directory and open that cloned
directory in IntelliJ IDEA.

Confirm the Python version:

```bash
python3 --version
```

Create a new virtual environment for this repository. Do not copy the Lesson 1
virtual environment into the project.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If IntelliJ IDEA does not select the environment automatically, configure the
project interpreter to use `.venv`.

## Run the starter application

With the virtual environment active:

```bash
python run.py
```

Open <http://127.0.0.1:5000> in a browser. Stop the development server with
<kbd>Control</kbd>+<kbd>C</kbd>.

The `/health` route is included so the team and deployment platform can verify
that the application is running:

```text
http://127.0.0.1:5000/health
```

## Run the tests

```bash
python -m pytest
```

The starter build should pass before anyone begins Sprint 1 work. The tests do
not call an AI API and do not use API credits. During Sprint 1, the team adds a
test for the homepage Story.

GitHub Actions runs the same tests for every push and pull request. A green
check means the automated build passed; it does not replace peer review or QA
verification of the Story's acceptance criteria.

## Team workflow

1. Select a Jira item from **To Do** and assign it to yourself.
2. Move it to **In Progress**.
3. Create a short-lived branch from the current default branch.
4. Make a focused change and test it locally.
5. Push the branch and open a pull request.
6. Move the Jira item to **Pull Request**.
7. Ask a teammate to review and test the change.
8. Merge only after review and a successful GitHub Actions build.
9. Verify the relevant acceptance criteria and move the item to **Done**.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before beginning work. Do not commit
directly to the default branch unless your instructor explicitly directs you
to do so.

## Credentials and environment files

This sprint does not require an AI API key. When credentials are introduced in
a later sprint, store them in a local `.env` file or in the deployment
platform's environment settings. The `.env` file is ignored by Git.

Never place a password, API key, client secret, or other credential in Python
code, HTML, screenshots, Jira, Confluence, chat messages, or Git history.

## Render deployment

The application includes the production entry point needed to run:

```bash
gunicorn wsgi:app
```

Do not configure the team's Render service before the deployment lesson unless
your instructor asks you to do so. During Lesson 3, the class will configure
Render, perform a public smoke test, verify the acceptance criteria, and
complete the Sprint Review and Retrospective.

## Starter boundaries

The starter intentionally does not include:

- A finished homepage
- Database models
- Authentication
- AI integration
- API keys
- Render service configuration
- Event-planning features

Those capabilities will be added through refined Stories in later sprints.

## Troubleshooting

- **`ModuleNotFoundError`:** Activate `.venv`, then run
  `python -m pip install -r requirements.txt`.
- **Port 5000 is already in use:** Stop the earlier Flask process before
  starting this application again.
- **Tests pass locally but fail in GitHub:** Open the workflow log and compare
  the Python version, installed dependencies, and committed files.
- **A teammate's changes are missing:** Confirm that you are in the correct
  team repository and pull the latest default branch before creating a new
  branch.
