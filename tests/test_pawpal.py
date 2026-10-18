"""Automated checks for PawPal+ core behaviors and edge cases."""

from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


DAY = date(2026, 10, 18)


def test_task_completion():
    task = Task("Feed", "08:00", DAY)
    task.mark_complete()
    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "cat")
    pet.add_task(Task("Feed", "08:00", DAY))
    assert len(pet.tasks) == 1


def test_owner_aggregates_multiple_pets():
    owner = Owner("Jordan")
    for name in ("Bella", "Luna"):
        pet = Pet(name, "cat")
        pet.add_task(Task("Breakfast", "08:00", DAY))
        owner.add_pet(pet)
    assert len(owner.get_all_tasks()) == 2
    assert len(Scheduler(owner).filter_tasks(on_date=DAY)) == 2


def test_sorting_is_chronological():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    for time in ("18:30", "07:00", "12:15"):
        pet.add_task(Task("Care", time, DAY))
    result = Scheduler(owner).sort_by_time()
    assert [task.time for _, task in result] == ["07:00", "12:15", "18:30"]


def test_filter_by_pet_and_completion():
    owner = Owner("Jordan")
    bella, luna = Pet("Bella", "dog"), Pet("Luna", "cat")
    owner.add_pet(bella)
    owner.add_pet(luna)
    bella.add_task(Task("Walk", "08:00", DAY, completed=True))
    bella.add_task(Task("Feed", "09:00", DAY))
    luna.add_task(Task("Feed", "10:00", DAY))
    selected = Scheduler(owner).filter_tasks(on_date=DAY, pet_name="bella", completed=False)
    assert len(selected) == 1 and selected[0][1].title == "Feed"


def test_daily_recurrence_creates_next_day():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    old_task = Task("Feed", "08:00", DAY, frequency="daily")
    pet.add_task(old_task)
    new_task = Scheduler(owner).mark_task_complete("Mochi", old_task)
    assert old_task.completed
    assert new_task is not None
    assert new_task.due_date == DAY + timedelta(days=1)
    assert new_task.completed is False
    assert len(pet.tasks) == 2


def test_weekly_recurrence_and_no_duplicate():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    old_task = Task("Groom", "12:00", DAY, frequency="weekly")
    pet.add_task(old_task)
    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete("Mochi", old_task)
    assert next_task is not None and next_task.due_date == DAY + timedelta(days=7)
    assert scheduler.mark_task_complete("Mochi", old_task) is None
    assert len(pet.tasks) == 2


def test_exact_time_conflict_between_pets():
    owner = Owner("Jordan")
    for name in ("Bella", "Luna"):
        pet = Pet(name, "dog")
        owner.add_pet(pet)
        pet.add_task(Task("Feed", "08:00", DAY, duration_minutes=10))
    assert len(Scheduler(owner).detect_conflicts(DAY)) == 1


def test_overlapping_intervals_conflict():
    owner = Owner("Jordan")
    pet = Pet("Bella", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", DAY, duration_minutes=30))
    pet.add_task(Task("Feed", "08:20", DAY, duration_minutes=10))
    assert len(Scheduler(owner).detect_conflicts(DAY)) == 1


def test_back_to_back_tasks_do_not_conflict():
    owner = Owner("Jordan")
    pet = Pet("Bella", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", "08:00", DAY, duration_minutes=30))
    pet.add_task(Task("Feed", "08:30", DAY, duration_minutes=10))
    assert Scheduler(owner).detect_conflicts(DAY) == []


def test_priorities_win_conflict_and_budget():
    owner = Owner("Jordan", daily_available_minutes=20)
    pet = Pet("Bella", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Optional play", "08:00", DAY, 20, "low"))
    pet.add_task(Task("Medication", "08:00", DAY, 10, "high"))
    pet.add_task(Task("Breakfast", "09:00", DAY, 10, "medium"))
    plan, skipped = Scheduler(owner).build_daily_plan(DAY)
    assert {task.title for _, task in plan} == {"Medication", "Breakfast"}
    assert any("Optional play" in message for message in skipped)


def test_empty_owner_is_safe():
    scheduler = Scheduler(Owner("Jordan"))
    assert scheduler.build_daily_plan(DAY) == ([], [])
    assert scheduler.detect_conflicts(DAY) == []


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        Task("Feed", "25:30", DAY)
    with pytest.raises(ValueError):
        Task("Feed", "09:00", DAY, duration_minutes=0)
    owner = Owner("Jordan")
    owner.add_pet(Pet("Mochi", "cat"))
    with pytest.raises(ValueError):
        owner.add_pet(Pet("mochi", "dog"))


def test_preference_breaks_same_priority_budget_tie():
    owner = Owner("Jordan", daily_available_minutes=15, preferred_time_of_day="evening")
    pet = Pet("Mochi", "cat")
    owner.add_pet(pet)
    pet.add_task(Task("Morning play", "08:00", DAY, 15, "medium"))
    pet.add_task(Task("Evening play", "19:00", DAY, 15, "medium"))
    plan, skipped = Scheduler(owner).build_daily_plan(DAY)
    assert [task.title for _, task in plan] == ["Evening play"]
    assert len(skipped) == 1
