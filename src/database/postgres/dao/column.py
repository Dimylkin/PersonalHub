from database.postgres.dao.base import BaseDAO
from database.postgres.tables.column import ColumnDB


class ColumnDAO(BaseDAO[ColumnDB]):
    model = ColumnDB
