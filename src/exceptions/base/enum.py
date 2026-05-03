from enum import StrEnum


class ModuleEnum(StrEnum):
    """ Область проекта, в котором произошла ошибка """

    core = "core"
    database = "database"
    boards = "board"
    columns = "columns"
    tasks = "tasks"
