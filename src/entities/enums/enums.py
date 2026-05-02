from enum import StrEnum


class WorkspaceType(StrEnum):
    WORK = "work"
    STUDY = "study"
    LIFE = "life"


class UrgencyTask(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TypeColumn(StrEnum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"