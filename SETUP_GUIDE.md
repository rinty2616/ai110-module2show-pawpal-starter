# PawPal+ Step-by-Step Setup Guide

These instructions are written for **Mac with VS Code and Terminal**. They also work similarly on Windows, but the virtual environment activation is different.

## Step 1 — Make your GitHub fork

1. Sign into [GitHub](https://github.com).
2. Open the [CodePath PawPal+ starter repository](https://github.com/codepath/ai110-module2show-pawpal-starter).
3. Click **Fork**, then **Create fork**. You should now have a copy under your own account.
4. On your fork click **Code** and copy the HTTPS clone URL.
5. Open Terminal and run `git clone YOUR_FORK_URL`, substituting your actual URL.
6. Use `cd` to enter the cloned folder and open it in VS Code with `code .` (or File → Open Folder).

**Important:** Do not replace the hidden `.git` folder. Git commits and pushes should go to your fork, not to the original CodePath starter.

## Step 2 — Add the project files

1. Unzip `PawPal_Plus_Project.zip`.
2. Copy the **contents inside** the `PawPal_Plus_Project` folder into your cloned fork folder.
3. Allow the new `README.md`, `reflection.md`, `app.py`, and `requirements.txt` to replace the corresponding starter files if you want to use this worked example.
4. Check that `pawpal_system.py`, `main.py`, `tests/test_pawpal.py`, and both `.mmd` files are there.

Do not submit the ZIP itself as the repository: the assignment requests a public fork with a meaningful commit history.

## Step 3 — Prepare Python

Open the VS Code terminal inside the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `python` is not found, try `python3`. Check Python's version using `python3 --version` (Python 3.10+ needed).

## Step 4 — Verify the backend (Phases 1, 2, and 4)

Open `pawpal_system.py` and read the four classes. Then run:

```bash
python main.py
```

You should see a time-sorted schedule, a conflict warning, and a recurring next-day task. Edit the demo values to make sure you understand how the behavior changes.

## Step 5 — Verify tests (Phase 5)

```bash
python -m pytest
```

Expected with the supplied code: 14 tests passing. If you make changes, test again.

## Step 6 — Launch the app (Phases 3 and 6)

```bash
streamlit run app.py
```

In the app: enter the owner's name, add at least two pets, schedule tasks, use date/pet/status filters, generate the plan, and mark a daily task complete. Confirm the following day's task appears when you switch the date filter.

## Step 7 — Review documentation and diagrams

- Open `diagrams/uml_draft.mmd` and `diagrams/uml_final.mmd` in [Mermaid Live Editor](https://mermaid.live/) to see how the design evolved.
- Check that `README.md` includes the sample CLI output and the tests you actually ran.
- Edit `reflection.md` to use **your own wording** and truthful details about your personal decisions, AI prompts, and verification.
- Keep an authentic log of your AI interactions in `ai_interactions.md` if your instructor requests it.

## Step 8 — Create meaningful commits, push, and submit

After copying the worked example into your fork and reviewing it, you can commit the source in logical groups:

```bash
git add diagrams/uml_draft.mmd
git commit -m "docs: add initial UML design"

git add pawpal_system.py main.py
git commit -m "feat: implement pet models and CLI scheduling"

git add app.py
git commit -m "feat: connect Streamlit interface"

git add requirements.txt tests/test_pawpal.py
git commit -m "test: verify task and scheduling behavior"

git add README.md reflection.md diagrams/uml_final.mmd ai_interactions.md SETUP_GUIDE.md .gitignore
git commit -m "docs: finalize PawPal project and reflection"

git push origin main
```

These are logical, accurately described file-group commits. Your course may prefer the exact incremental development history as you work; if you implement parts yourself, commit them after each stage rather than copying and committing all at once.

Finally verify your GitHub repository is **public**, contains the required files, shows your commits, and submit your fork's URL through the course submission page.

## What the classes mean in simple language

- **`Task`** = one job (e.g., "Feed Bella at 8:00 AM").
- **`Pet`** = one animal with a list of jobs.
- **`Owner`** = the person with one or more pets and an amount of time available.
- **`Scheduler`** = the planner that reads all pets' jobs and chooses a reasonable plan.
- **`st.session_state`** = temporary app storage so the owner and pets do not disappear each time you click a Streamlit button.
- **`pytest`** = automated questions that check whether your program behaves correctly.
