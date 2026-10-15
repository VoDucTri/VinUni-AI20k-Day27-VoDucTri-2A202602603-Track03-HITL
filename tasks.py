"""Task management module."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool = False
    priority: int = 1  # 1 = low, 2 = medium, 3 = high, 4 = critical
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    def mark_completed(self) -> None:
        self.completed = True
        self.updated_at = datetime.now()

    def update_priority(self, new_priority: int) -> None:
        if new_priority not in (1, 2, 3, 4):
            raise ValueError(f"Invalid priority: {new_priority}")
        self.priority = new_priority
        self.updated_at = datetime.now()


def filter_tasks_by_priority(tasks: list[Task], min_priority: int) -> list[Task]:
    """Return tasks with priority greater than or equal to min_priority."""
    return [t for t in tasks if t.priority >= min_priority]
