"""Streamlit interface that calls the real PawPal+ backend."""

from datetime import date, datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", daily_available_minutes=120)

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("Your smart pet-care planner | Schedule, prioritize, and track daily routines")
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

with st.sidebar:
    st.header("👤 Owner settings")
    new_owner_name = st.text_input("Owner name", value=owner.name)
    if new_owner_name.strip():
        owner.name = new_owner_name.strip()
    owner.daily_available_minutes = st.number_input(
        "Daily care time available (minutes)",
        min_value=1,
        max_value=1440,
        value=owner.daily_available_minutes,
        step=5,
    )
    preference_options = ["any", "morning", "afternoon", "evening"]
    owner.preferred_time_of_day = st.selectbox(
        "Preferred care time",
        preference_options,
        index=preference_options.index(owner.preferred_time_of_day),
    )
    st.info("Data stays in this browser session. A new session resets it.")

st.subheader("1 · Manage pets")
with st.form("add_pet_form", clear_on_submit=True):
    first, second = st.columns(2)
    pet_name = first.text_input("Pet name", placeholder="Bella")
    species = second.selectbox("Species", ["dog", "cat", "bird", "other"])
    add_pet = st.form_submit_button("➕ Add pet")
    if add_pet:
        try:
            owner.add_pet(Pet(pet_name, species))
            st.success(f"Added {pet_name.strip()}!")
        except (TypeError, ValueError) as exc:
            st.error(str(exc))

if owner.pets:
    st.write("**Your pets:** " + " · ".join(f"{pet.name} ({pet.species})" for pet in owner.pets))
else:
    st.info("Add a pet above to start planning care tasks.")

st.divider()
st.subheader("2 · Schedule a task")
if owner.pets:
    with st.form("new_task_form", clear_on_submit=False):
        pet_choice = st.selectbox("Which pet?", [pet.name for pet in owner.pets])
        title = st.text_input("Task description", placeholder="Morning walk")
        c1, c2, c3 = st.columns(3)
        selected_date = c1.date_input("Date", value=date.today())
        selected_time = c2.time_input("Time", value=datetime.strptime("08:00", "%H:%M").time())
        duration = c3.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        c4, c5 = st.columns(2)
        priority = c4.selectbox("Priority", ["high", "medium", "low"])
        frequency = c5.selectbox("Repeat", ["once", "daily", "weekly"])
        add_task = st.form_submit_button("➕ Add task")
        if add_task:
            try:
                task = Task(
                    title=title,
                    time=selected_time.strftime("%H:%M"),
                    due_date=selected_date,
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
                pet = owner.get_pet(pet_choice)
                if pet is None:
                    raise ValueError("Please select an existing pet.")
                pet.add_task(task)
                st.success(f"Scheduled '{task.title}' for {pet.name}.")
            except (TypeError, ValueError) as exc:
                st.error(str(exc))
else:
    st.caption("Add at least one pet to enable task scheduling.")

all_records = scheduler.sort_by_time()
if all_records:
    with st.expander("✏️ Edit an existing task"):
        task_options = list(range(len(all_records)))
        task_index = st.selectbox(
            "Select task to edit",
            task_options,
            format_func=lambda i: (
                f"{all_records[i][0].name} · {all_records[i][1].title} "
                f"({all_records[i][1].due_date} {all_records[i][1].time})"
            ),
        )
        edit_pet, original = all_records[task_index]
        with st.form(f"edit_task_{id(original)}"):
            edited_title = st.text_input("Description", value=original.title)
            e1, e2, e3 = st.columns(3)
            edited_date = e1.date_input("Scheduled date", value=original.due_date)
            edited_time = e2.time_input("Scheduled time", value=original.start_at().time())
            edited_duration = e3.number_input(
                "Duration", min_value=1, max_value=240, value=original.duration_minutes
            )
            e4, e5 = st.columns(2)
            priorities = ["high", "medium", "low"]
            frequencies = ["once", "daily", "weekly"]
            edited_priority = e4.selectbox("Priority", priorities, index=priorities.index(original.priority))
            edited_frequency = e5.selectbox("Repeat", frequencies, index=frequencies.index(original.frequency))
            if st.form_submit_button("Save changes"):
                try:
                    updated = Task(
                        edited_title,
                        edited_time.strftime("%H:%M"),
                        edited_date,
                        int(edited_duration),
                        edited_priority,
                        edited_frequency,
                        original.completed,
                    )
                    replace_index = next(
                        index for index, existing in enumerate(edit_pet.tasks) if existing is original
                    )
                    edit_pet.tasks[replace_index] = updated
                    st.session_state.flash = "Task updated."
                    st.rerun()
                except (TypeError, ValueError) as exc:
                    st.error(str(exc))

st.divider()
st.subheader("3 · View tasks and mark complete")
filter1, filter2, filter3 = st.columns(3)
day = filter1.date_input("Schedule date", value=date.today(), key="schedule_day")
pet_filter = filter2.selectbox("Show pet", ["All pets"] + [pet.name for pet in owner.pets])
status_filter = filter3.selectbox("Show status", ["All", "Pending", "Completed"])
status = {"All": None, "Pending": False, "Completed": True}[status_filter]
records = scheduler.sort_by_time(
    scheduler.filter_tasks(
        on_date=day,
        pet_name=None if pet_filter == "All pets" else pet_filter,
        completed=status,
    )
)
if records:
    st.dataframe(
        [
            {
                "Time": task.time,
                "Pet": pet.name,
                "Activity": task.title,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority.title(),
                "Repeat": task.frequency.title(),
                "Status": "Done ✅" if task.completed else "Pending",
            }
            for pet, task in records
        ],
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No tasks match these filters.")

pending = [(pet, task) for pet, task in records if not task.completed]
if pending:
    done_index = st.selectbox(
        "Select a task to complete",
        range(len(pending)),
        format_func=lambda i: f"{pending[i][0].name} — {pending[i][1].title} ({pending[i][1].time})",
    )
    if st.button("✅ Mark complete"):
        pet, task = pending[done_index]
        next_task = scheduler.mark_task_complete(pet.name, task)
        if next_task:
            st.session_state.flash = f"Completed! Next '{task.title}' is {next_task.due_date} at {next_task.time}."
        else:
            st.session_state.flash = f"Completed '{task.title}'."
        st.rerun()

st.divider()
st.subheader("4 · Build smart daily plan")
st.caption("The scheduler selects high-priority tasks first, honors fixed start times, and respects the daily time budget.")
conflicts = scheduler.detect_conflicts(day)
for warning in conflicts:
    st.warning(warning)

if st.button("🗓️ Generate daily plan", type="primary"):
    plan, skipped = scheduler.build_daily_plan(day)
    if plan:
        used = sum(task.duration_minutes for _, task in plan)
        st.success(f"Scheduled {len(plan)} tasks: {used}/{owner.daily_available_minutes} available minutes.")
        st.table(
            [
                {
                    "Start": task.time,
                    "Pet": pet.name,
                    "Task": task.title,
                    "Duration": f"{task.duration_minutes} min",
                    "Why selected": f"{task.priority.title()} priority; fits available time",
                }
                for pet, task in plan
            ]
        )
    else:
        st.info("No pending tasks fit this date and time budget.")
    for reason in skipped:
        st.warning(reason)

st.caption("PawPal+ uses a transparent, priority-first scheduling algorithm. It does not automatically move a task to a different time.")
