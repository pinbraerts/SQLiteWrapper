import sqlite3

from utils import _iterable

class DatabaseTable:
    CREATE_IF = "create table "
    DELETE_IF = "drop table "
    IF_EXISTS = "if exists "
    IN_NOT_EXISTS = "if not exists "
    SHOULD_SPECIFY = " shoud specify "
    SELECT_ALL = "select * from "
    INSERT_INTO = "insert into {} values ({})"

    def create(self, check_not_exist=True):
        self.connection.execute(
            self.CREATE_IF +
            (self.IF_NOT_EXISTS if check_not_exist else "") +
            self.TABLE_NAME + str(self.ENTRY_TYPE.ITEMS_DESCRIPTION)
        )
        return self

    def close(self):
        self.connection.commit()
        self.connection.close()

    def delete(self, check_if_exists=True):
        self.connection.execute(
            self.DELETE_IF +
            (self.IF_EXISTS if check_if_exists else "") +
            self.TABLE_NAME
        )
        return self

    def all(self):
        return self.connection.execute(self.SELECT_ALL + self.TABLE_NAME)

    def __init__(self):
        if not hasattr(self, "TABLE_NAME"):
            raise ArgumentError(
                self.__class__.name + self.SHOULD_SPECIFY + "TABLE_NAME"
            )
        if not hasattr(self, "DATABASE_NAME"):
            self.DATABASE_NAME = self.TABLE_NAME.lower() + ".db"
        if not hasattr(self, "ENTRY_TYPE"):
            try:
                self.ENTRY_TYPE = next(
                    i for j, i in self.__class__.__dict__.items()
                    if not j.startswith("_") and isinstance(i, type)
                )
            except StopIteration:
                raise ArgumentError(
                    self.__class__.name + self.SHOULD_SPECIFY + "ENTRY_TYPE"
                )
        self.connection = sqlite3.connect(self.DATABASE_NAME)
        self.connection.row_factory = self.ENTRY_TYPE.fromColumnRow

    def insert(self, *items):
        if len(items) == 1:
            items = items[0]
        if _iterable(items):
            self.connection.executemany(
                self.INSERT_INTO.format(
                    self.TABLE_NAME, self.ENTRY_TYPE.ITEMS_PLACEHOLDER
                ), (i.tolist() for i in items)
            )
        elif isinstance(items, self.ENTRY_TYPE):
            self.connection.execute(
                self.INSERT_INTO.format(
                    self.TABLE_NAME, self.ENTRY_TYPE.ITEMS_PLACEHOLDER
                ), items.tolist()
            )
        return self

    def __enter__(self):
        return self.create()

    def __exit__(self, type, value, traceback):
        self.close()
