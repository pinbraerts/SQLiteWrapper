from DatabaseTable import DatabaseTable
from TableEntry import TableEntry
from ColumnModifiers import *


class UsersTable(DatabaseTable):
    TABLE_NAME = "users"

    class User(TableEntry):
        id = int | primary_key
        name = str


# UsersTable().delete()
# UsersTable().create().insert([
#     User(0, "test"),
#     User(1, "test1")
# ])
print(list(UsersTable().all()))
