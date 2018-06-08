NoneType = None.__class__
from ColumnModifiers import *

class ColumnType:
    DEFAULT_DATA_TYPE = "INTEGER"

    _TYPE2SQLITE = {
        NoneType: "NULL",
        int: "INTEGER",
        float: "REAL",
        str: "TEXT",
        bytes: "BLOB"
    }

    _SQLITE2TYPE = {
        "NULL": NoneType,
        "INTEGER": int,
        "REAL": float,
        "TEXT": str,
        "BLOB": bytes
    }

    def type2SQLite(self, t):
        return self._TYPE2SQLITE[t]

    def SQLite2type(self, t):
        return self._SQLITE2TYPE[t.upper()]

    def __init__(self, name, datatype=None, arguments=None):
        if isinstance(datatype, str):
            datatype, *arguments = datatype.split()
            arguments = ' '.join(arguments)
            datatype = self.SQLite2type(datatype)
        elif isinstance(datatype, Annotator):
            datatype, arguments = datatype.origin, datatype.mod
        if arguments is None:
            arguments = ""
        if datatype is None:
            datatype = ColumnType.DEFAULT_DATA_TYPE
        self.arguments = arguments
        self.datatype = datatype
        self.sqltype = self.type2SQLite(datatype)
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.datatype(*args, **kwargs)

    def __str__(self):
        return "{} {} {}".format(
            self.name,
            self.sqltype,
            self.arguments
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.sqltype == other
        elif isinstance(other, type):
            return self.datatype == other
        return False
