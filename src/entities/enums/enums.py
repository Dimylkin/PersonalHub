from enum import StrEnum


class WorkspaceType(StrEnum):
    """ Область, в которой находится доска """

    WORK = "work"
    STUDY = "study"
    LIFE = "life"


class UrgencyTask(StrEnum):
    """" Уровень 'срочности' задания, которая выстраивается из личных предпочтений """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TypeColumn(StrEnum):
    """ Тип колонки отвечающий за свое состояние задач """

    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"