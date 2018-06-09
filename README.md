# SQLiteWrapper
Wrapper for the **sqlite3** Python 3 library

## Preparations
Just inherit from the `DatabaseTable` class and specify `TABLE_NAME`,
`DATABASE_NAME` and `ENTRY_TYPE` class variables by strings and class inherited
from the `TableEntry` class respectively:
``` Python
from DatabaseTable import DatabaseTable
from TableEntry import TableEntry

class MyEntry(TableEntry):
  name = str  # init field by it's type

class MyTable(DatabaseTable):
  ENTRY_TYPE = MyEntry
  TABLE_NAME = "my_table_name"
```

## Usage
You can use your table class in with-as statement, by chaining or directly

#### With-As
``` Python
with MyTable() as table:
  # table.createTable() is called implicitly
  table.insert(MyEntry("Josh"), MyEntry("Dave"))
  print(table.all().fetchall())
```

#### Chaining
``` Python
MyTable().createTable().insert(MyEntry("Josh"), MyEntry("Dave")).close()
```

#### Direct calls
``` Python
table = MyTable()
table.createTable()
table.insert(MyEntry("Josh"), MyEntry("Dave"))
print(table.all().fetchall())
table.close()
```

## Autofill
- `__init__`, `__str__`, `__repr__` and `__copy__` methods for `MyEntry`

- factory methods for constructing from **sqlite3** `Column-Row` pair,
`tuple` (or just `Row`) and dictionary (or `JSON` object) for `MyEntry`

- nested `MyEntry` class is detected automatically.


## Column Modifiers
#### SQL
You could use stringified SQL type names with modifiers in the `MyEntry` class:
``` Python
class MyEntry:
  id = "INTEGER PRIMARY KEY"
  name = "TEXT UNIQUE FAIL"
```

#### Python
Or pipe-style modifiers from the `ColumnModifiers` module:
``` Python
from ColumnModifiers import *

class MyEntry:
  id = int | primary_key
  name = str | unique | conflict(Conflict.Fail)
```
