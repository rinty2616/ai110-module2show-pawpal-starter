"""Object-oriented pet care models and scheduling algorithms for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from typing import Iterable


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
FREQUENCIES = {"once", "daily", "weekly"}


@dataclass
class Task:
    """Store one scheduled pet-care activity."""

    title: str
    time: str  # 24-hour HH:MM, such as "08:30"
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate task information when a task is created."""
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Task title cannot be empty.")
        try:
            parsed = datetime.strptime(self.time, "%H:%M")
            if parsed.strftime("%H:%M") != self.time:
                raise ValueError
        except ValueError as exc:
            raise ValueError("Time must use 24-hour HH:MM format (for example 08:30).") from exc
        if not isinstance(self.due_date, date) or isinstance(self.due_date, datetime):
            raise ValueError("due_date must be a date.")
        if not isinstance(self.duration_minutes, int) or isinstance(self.duration_minutes, bool) or self.duration_minutes <= 0:
            raise ValueError("Duration must be a positive whole number of minutes.")
        self.priority = self.priority.lower()
        self.frequency = self.frequency.lower()
        if self.priority not in PRIORITY_ORDER:
            raise ValueError("Priority must be low, medium, or high.")
        if self.frequency not in FREQUENCIES:
            raise ValueError("Frequency must be once, daily, or weekly.")

    def mark_complete(self) -> None:
        """Mark this occurrence of the task as complete."""
        self.completed = True

    def start_at(self) -> datetime:
        """Return this task's scheduled start as a datetime."""
        hour, minute = map(int, self.time.split(":"))
        return datetime.combine(self.due_date, datetime.min.time()).replace(
            hour=hour, minute=minute
        )

    def end_at(self) -> datetime:
        """Return the estimated end based on its duration."""
        return self.start_at() + timedelta(minutes=self.duration_minutes)


@dataclass
class Pet:
    """Store a pet's details and its care activities."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Require a meaningful pet name and species."""
        self.name = self.name.strip()
        self.species = self.species.strip().lower()
        if not self.name or not self.species:
            raise ValueError("Pet name and species are required.")

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        if not isinstance(task, Task):
            raise TypeError("Only Task objects can be added to a pet.")
        self.tasks.append(task)


@dataclass
class Owner:
    """Manage one owner's pets and their shared time budget."""

    name: str
    daily_available_minutes: int = 120
    preferred_time_of_day: str = "any"
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate owner details and daily available time."""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Owner name cannot be empty.")
        if self.daily_available_minutes < 1:
            raise ValueError("Available minutes must be positive.")
        if self.preferred_time_of_day not in {"any", "morning", "afternoon", "evening"}:
            raise ValueError("Preference must be any, morning, afternoon, or evening.")

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner with a unique name."""
        if not isinstance(pet, Pet):
            raise TypeError("Only Pet objects can be added to an owner.")
        if self.get_pet(pet.name) is not None:
            raise ValueError(f"A pet named '{pet.name}' already exists.")
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Find a pet by name, ignoring letter case."""
        return next((pet for pet in self.pets if pet.name.lower() == name.lower()), None)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Collect tasks across every pet, preserving pet association."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Sort, filter, prioritize, and check all of an owner's tasks."""

    def __init__(self, owner: Owner):
        """Read all pet tasks through the Owner class."""
        self.owner = owner

    def filter_tasks(
        self,
        on_date: date | None = None,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by due date, pet name, and completion status."""
        results = self.owner.get_all_tasks()
        if on_date is not None:
            results = [(pet, task) for pet, task in results if task.due_date == on_date]
        if pet_name:
            results = [(pet, task) for pet, task in results if pet.name.lower() == pet_name.lower()]
        if completed is not None:
            results = [(pet, task) for pet, task in results if task.completed == completed]
        return results

    def sort_by_time(
        self, records: Iterable[tuple[Pet, Task]] | None = None
    ) -> list[tuple[Pet, Task]]:
        """Sort tasks chronologically, breaking ties by priority."""
        if records is None:
            records = self.owner.get_all_tasks()
        return sorted(
            records,
            key=lambda item: (
                item[1].due_date,
                item[1].time,
                PRIORITY_ORDER[item[1].priority],
                item[0].name.lower(),
            ),
        )

    def _preference_rank(self, task: Task) -> int:
        """Favor the owner's preferred part of day among equal-priority tasks."""
        preference = self.owner.preferred_time_of_day
        hour = int(task.time[:2])
        task_daypart = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
        return 0 if preference == "any" or preference == task_daypart else 1

    @staticmethod
    def _overlap(first: Task, second: Task) -> bool:
        """Return whether two scheduled task intervals overlap."""
        return first.start_at() < second.end_at() and second.start_at() < first.end_at()

    def detect_conflicts(self, on_date: date | None = None) -> list[str]:
        """Return warnings for overlapping unfinished tasks on the same date."""
        tasks = self.sort_by_time(self.filter_tasks(on_date=on_date, completed=False))
        warnings: list[str] = []
        for i, (first_pet, first_task) in enumerate(tasks):
            for second_pet, second_task in tasks[i + 1 :]:
                if first_task.due_date != second_task.due_date:
                    continue
                if self._overlap(first_task, second_task):
                    warnings.append(
                        f"Conflict on {first_task.due_date}: "
                        f"{first_pet.name}'s '{first_task.title}' at {first_task.time} "
                        f"overlaps {second_pet.name}'s '{second_task.title}' "
                        f"at {second_task.time}."
                    )
        return warnings

    def mark_task_complete(self, pet_name: str, task: Task) -> Task | None:
        """Complete a task and generate its next daily or weekly occurrence."""
        pet = self.owner.get_pet(pet_name)
        if pet is None or not any(existing is task for existing in pet.tasks):
            raise ValueError("The selected task does not belong to that pet.")
        if task.completed:
            return None  # Prevent duplicate future occurrences.
        task.mark_complete()
        if task.frequency == "once":
            return None
        days = 1 if task.frequency == "daily" else 7
        next_task = replace(task, due_date=task.due_date + timedelta(days=days), completed=False)
        pet.add_task(next_task)
        return next_task

    def build_daily_plan(
        self, on_date: date | None = None, available_minutes: int | None = None
    ) -> tuple[list[tuple[Pet, Task]], list[str]]:
        """Prefer urgent tasks while respecting the owner's time and fixed slots."""
        day = on_date or date.today()
        budget = self.owner.daily_available_minutes if available_minutes is None else available_minutes
        if budget < 0:
            raise ValueError("Time budget cannot be negative.")
        candidates = self.filter_tasks(on_date=day, completed=False)
        # Higher-priority jobs are picked first; preferences break ties.
        candidates.sort(
            key=lambda item: (
                PRIORITY_ORDER[item[1].priority], self._preference_rank(item[1]),
                item[1].time, item[0].name.lower()
            )
        )
        selected: list[tuple[Pet, Task]] = []
        skipped: list[str] = []
        used_minutes = 0
        for pet, task in candidates:
            if used_minutes + task.duration_minutes > budget:
                skipped.append(
                    f"Skipped {pet.name}'s '{task.title}': exceeds the {budget}-minute daily budget."
                )
                continue
            overlapping = next(
                ((other_pet, other_task) for other_pet, other_task in selected if self._overlap(task, other_task)),
                None,
            )
            if overlapping:
                other_pet, other_task = overlapping
                skipped.append(
                    f"Skipped {pet.name}'s '{task.title}': overlaps "
                    f"{other_pet.name}'s '{other_task.title}' (higher/equal selection priority)."
                )
                continue
            selected.append((pet, task))
            used_minutes += task.duration_minutes
        return self.sort_by_time(selected), skipped
