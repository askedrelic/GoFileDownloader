"""Module for tracking and displaying the progress of multiple tasks.

It uses the Rich library to create dynamic, formatted progress bars and tables for
monitoring task completion.
"""
from __future__ import annotations

from collections import deque

from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Column, Table


class ProgressManager:
    """Class to manage and track the progress of multiple tasks."""

    def __init__(
        self,
        task_name: str,
        item_description: str,
        color: str = "light_cyan3",
        overall_buffer_size: int = 5,
    ) -> None:
        """Initialize a progress tracking system for a specific task."""
        self.task_name = task_name
        self.item_description = item_description
        self.color = color
        self.overall_progress = self._create_progress_bar()
        self.task_progress = self._create_progress_bar()
        self.num_tasks = 0
        self.overall_buffer = deque(maxlen=overall_buffer_size)

    def add_overall_task(self, description: str, num_tasks: int) -> None:
        """Add an overall progress task with a given description and total tasks."""
        self.num_tasks = num_tasks
        overall_description = self._adjust_description(description)
        self.overall_progress.add_task(
            f"[{self.color}]{overall_description}", total=num_tasks, completed=0,
        )

    def add_task(self, current_task: int = 0, total: int = 100) -> int:
        """Add an individual task to the task progress bar."""
        task_description = (
            f"[{self.color}]{self.item_description} {current_task + 1}/{self.num_tasks}"
        )
        return self.task_progress.add_task(task_description, total=total)

    def update_task(
            self,
            task_id: int,
            completed: int | None = None,
            advance: int = 0,
            *,
            visible: bool = True,
        ) -> None:
        """Update the progress of an individual task and the overall progress."""
        self.task_progress.update(
            task_id,
            completed=completed if completed is not None else None,
            advance=advance if completed is None else None,
            visible=visible,
        )
        self._update_overall_task(task_id)

    def create_progress_table(self) -> Panel:
        """Create a formatted progress table for tracking the download."""
        progress_table = Table.grid()
        progress_table.add_row(
            Panel.fit(
                self.overall_progress,
                title=f"[bold {self.color}]Overall Progress",
                border_style="bright_blue",
                padding=(1, 1),
                width=40,
            ),
            Panel.fit(
                self.task_progress,
                title=f"[bold {self.color}]{self.task_name} Progress",
                border_style="medium_purple",
                padding=(1, 1),
                width=40,
            ),
        )
        return progress_table

    # Private methods
    def _update_overall_task(self, task_id: int) -> None:
        """Advance the overall progress removes old tasks from the buffer."""
        # Access the latest task dynamically
        current_overall_task = self.overall_progress.tasks[-1]

        # If the task is finished, remove it and update the overall progress
        if self.task_progress.tasks[task_id].finished:
            self.overall_progress.advance(current_overall_task.id)
            self.task_progress.update(task_id, visible=False)

        # Track completed overall tasks
        if current_overall_task.finished:
            self.overall_buffer.append(current_overall_task)

        # Cleanup completed overall tasks
        self._cleanup_completed_overall_tasks()

    def _cleanup_completed_overall_tasks(self) -> None:
        """Remove the oldest completed overall task from the buffer."""
        if len(self.overall_buffer) == self.overall_buffer.maxlen:
            completed_overall_id = self.overall_buffer.popleft().id
            self.overall_progress.remove_task(completed_overall_id)

    # Static methods
    @staticmethod
    def _adjust_description(description: str, max_length: int = 8) -> str:
        """Truncate a string to a specified maximum length, adding an ellipsis."""
        return (
            description[:max_length] + "..."
            if len(description) > max_length
            else description
        )

    @staticmethod
    def _create_progress_bar(columns: list[Column] | None = None) -> Progress:
        """Create and returns a progress bar for tracking download progress."""
        if columns is None:
            columns = [
                SpinnerColumn(),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            ]
        return Progress("{task.description}", *columns)
