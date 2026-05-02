from database.postgres.dao.base import BaseDAO
from database.postgres.tables.task import TaskDB


class TaskDAO(BaseDAO[TaskDB]):
    model = TaskDB
