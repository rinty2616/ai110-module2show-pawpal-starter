"""CLI-first demonstration of the PawPal+ backend."""

from datetime import date
from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create two pets, schedule activities, and exercise smart features."""
    demo_day = date(2026, 10, 18)  # Fixed for repeatable sample output.
    owner = Owner("Jordan", daily_available_minutes=60)
    bella = Pet("Bella", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(bella)
    owner.add_pet(luna)

    # Deliberately inserted out of time order to demonstrate sorting.
    bella.add_task(Task("Grooming", "15:30", demo_day, 20, "low"))
    luna.add_task(Task("Medication", "09:00", demo_day, 10, "high", "daily"))
    luna.add_task(Task("Breakfast", "08:00", demo_day, 10, "medium", "daily"))
    walk = Task("Morning walk", "08:00", demo_day, 30, "high", "daily")
    bella.add_task(walk)

    scheduler = Scheduler(owner)
    print(f"Today's Schedule - {demo_day}")
    for pet, task in scheduler.sort_by_time(scheduler.filter_tasks(on_date=demo_day)):
        print(f"  {task.time} | {pet.name:<5} | {task.title:<13} | {task.priority} | {task.duration_minutes} min")

    print("\nConflict warnings:")
    for warning in scheduler.detect_conflicts(demo_day):
        print(f"  WARNING: {warning}")

    plan, skipped = scheduler.build_daily_plan(demo_day)
    print("\nGenerated daily plan (60-minute budget):")
    for pet, task in plan:
        print(f"  {task.time} | {pet.name}: {task.title} ({task.priority}, {task.duration_minutes} min)")
    for reason in skipped:
        print(f"  NOTE: {reason}")

    next_task = scheduler.mark_task_complete("Bella", walk)
    if next_task:
        print(f"\nCompleted '{walk.title}'. Next occurrence: {next_task.due_date} at {next_task.time}")


if __name__ == "__main__":
    main()
