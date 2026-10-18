# 🐾 PawPal+

**PawPal+** is a Python and Streamlit pet-care planner. One owner can manage multiple pets, schedule walks/feedings/medications, prioritize tasks, and view a daily plan that respects a limited time budget. The backend is built with four object-oriented classes and verified by a CLI demo and automated tests.

## Features

- **Multi-pet management:** The `Owner` keeps a list of `Pet` objects; each pet stores its own tasks. `Owner.get_all_tasks()` supplies every pet's tasks to the scheduler.
- **Task details:** Scheduled date, start time, duration, priority (`high`, `medium`, `low`), recurrence (`once`, `daily`, `weekly`), and completion status.
- **Add and edit tasks:** Forms in the Streamlit app add pets and tasks or edit an existing task.
- **Sort by time:** `Scheduler.sort_by_time()` returns tasks in chronological order.
- **Filter:** `Scheduler.filter_tasks()` can select a date, pet name, and completion status.
- **Conflict warnings:** `Scheduler.detect_conflicts()` identifies overlapping *unfinished* tasks, including tasks for different pets.
- **Recurring care:** `Scheduler.mark_task_complete()` marks an occurrence complete and adds a new daily or weekly task dated 1 or 7 days later; one-time tasks do not repeat.
- **Daily plan:** `Scheduler.build_daily_plan()` selects high-priority work first, then uses the owner's preferred part of day to break same-priority ties. It respects the time budget and avoids simultaneous activities. Accepted tasks display in chronological order. Skipped tasks receive an explanation.
- **Session memory:** Streamlit's `st.session_state` keeps owner, pets, and tasks available while using the app within the same browser session.

## System architecture

| Class | Purpose |
|---|---|
| `Task` | One care activity, validation, completion status, start/end timestamps |
| `Pet` | A named pet and its tasks |
| `Owner` | Pet registry and shared daily time budget/preferences; aggregates tasks across pets |
| `Scheduler` | Cross-pet filtering, time sorting, conflict warnings, recurrence, daily planning |

See `diagrams/uml_draft.mmd` and `diagrams/uml_final.mmd`. Paste either file's contents into [Mermaid Live Editor](https://mermaid.live/) to see the diagram.

## Setup (Mac / Linux)

Requires Python 3.10+ (Python 3.11 or newer recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` instead.

### Run the CLI demo

```bash
python main.py
```

### Run the web app

```bash
streamlit run app.py
```

The app opens in your browser. The Streamlit demo keeps information for the current browser session and does **not** save to a database.

## Sample Output

Actual output from `python main.py`:

```text
Today's Schedule - 2026-10-18
  08:00 | Bella | Morning walk  | high | 30 min
  08:00 | Luna  | Breakfast     | medium | 10 min
  09:00 | Luna  | Medication    | high | 10 min
  15:30 | Bella | Grooming      | low | 20 min

Conflict warnings:
  WARNING: Conflict on 2026-10-18: Bella's 'Morning walk' at 08:00 overlaps Luna's 'Breakfast' at 08:00.

Generated daily plan (60-minute budget):
  08:00 | Bella: Morning walk (high, 30 min)
  09:00 | Luna: Medication (high, 10 min)
  15:30 | Bella: Grooming (low, 20 min)
  NOTE: Skipped Luna's 'Breakfast': overlaps Bella's 'Morning walk' (higher/equal selection priority).

Completed 'Morning walk'. Next occurrence: 2026-10-19 at 08:00
```

## Smarter Scheduling

| Feature | Method | Behavior |
|---|---|---|
| Sorting | `Scheduler.sort_by_time()` | Sorts by date and `HH:MM` time; ties use priority |
| Filtering | `Scheduler.filter_tasks()` | Filters by date, pet, or completed/pending |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when unfinished tasks on the same date overlap by duration |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completes the current task and creates another for tomorrow or next week |
| Daily plan | `Scheduler.build_daily_plan()` | Uses priority, preferred time of day, limited minutes, and nonoverlapping time slots |

**Planning logic:** High-priority tasks are considered first. Within one priority level, the owner's preferred daypart (`any`, `morning`, `afternoon`, `evening`) is considered before start time. If a task exceeds the remaining daily budget or overlaps a previously accepted task, it is skipped with a reason. The final plan is sorted chronologically, not by priority.

**Tradeoffs / limits:** This is a clear greedy scheduler, not a mathematical optimizer. It does not relocate tasks to new time slots, and it may not produce the maximum possible number of tasks. Conflicts are checked within each scheduled date, not across the midnight boundary. The UI saves data in memory only.

## Testing PawPal+

```bash
python -m pytest
```

The automated tests cover task completion/addition, multiple pets, time sorting, filtering, daily and weekly recurrence, duplicate recurrence prevention, exact-time and interval conflicts, back-to-back tasks, budget/priority selection, preferences, empty owners, and invalid inputs.

A successful local test run with `python -m pytest` produced:

```text
=================== test session starts ====================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/rintykawsar/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 14 items

tests/test_pawpal.py ..............                  [100%]

==================== 14 passed in 0.02s ====================

============================== 14 passed in 0.03s ==============================
```

**Confidence level:** ★★★★☆ (4/5). The core Python logic has automated tests, but browser-based Streamlit interaction and persistent storage are not covered by the automated suite.

## Demo Walkthrough

1. Run `streamlit run app.py` and enter your owner's name and available minutes in the sidebar. Optionally choose a preferred time of day.
2. Add **Bella (dog)** and **Luna (cat)** using the pet form.
3. Schedule Bella's **Morning walk** for 08:00, high priority, 30 minutes; and Luna's **Breakfast** for 08:00, medium priority, 10 minutes.
4. Add Luna's **Medication** at 09:00 and set it to repeat daily.
5. On the schedule date, the app lists tasks in time order and warns about the two 08:00 activities overlapping. Click **Generate daily plan** to view selected tasks and any skipped reasons.
6. Mark Medication complete. The current occurrence becomes completed and a new one is created for the following day.
7. Use the **Edit an existing task** expander to change a task's date, duration, priority, or frequency.

See the **Sample Output** above for CLI evidence, which can be reproduced without the web UI.

## Project files

```text
PawPal_Plus_Project/
├── app.py
├── pawpal_system.py
├── main.py
├── requirements.txt
├── tests/
│   └── test_pawpal.py
├── diagrams/
│   ├── uml_draft.mmd
│   └── uml_final.mmd
├── README.md
├── reflection.md
├── ai_interactions.md
└── SETUP_GUIDE.md
```

## Using the assignment's GitHub starter

The recommended submission path is to **fork CodePath's original starter repository**, clone your fork, then put the completed files from this example into that cloned folder. Keep the fork's `.git/` folder. Commit meaningful changes to your own fork and push them before submitting. See `SETUP_GUIDE.md`.
