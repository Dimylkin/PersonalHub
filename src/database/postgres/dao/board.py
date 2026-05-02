from database.postgres.dao.base import BaseDAO
from database.postgres.tables.board import BoardDB


class BoardDAO(BaseDAO[BoardDB]):
    model = BoardDB
