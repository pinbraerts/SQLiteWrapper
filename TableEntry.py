import sqlite3

from ColumnType import ColumnType

from utils import _clb, DefaultArg

class _TableEntry(type):
    @property
    def ITEMS_DESCRIPTION(cls):
        if cls._itemsd is None:
            cls._itemsd = tuple(
                ColumnType(i, j) for i, j in cls.__dict__.items()
                    if not i.startswith('_') and not _clb(i)
            )
        return cls._itemsd

    @property
    def ITEMS_PLACEHOLDER(cls):
        if cls._itemsp is None:
            cls._itemsp = ", ".join("?" * len(cls.ITEMS_DESCRIPTION))
        return cls._itemsp


class TableEntry(metaclass=_TableEntry):
    _itemsd = None
    _itemsp = None

    @classmethod
    def fromColumnRow(klass, _, row):
        return klass(*row)

    @classmethod
    def fromRow(klass, row):
        return klass(*row)

    @classmethod
    def fromDict(klass, dct):
        return klass(*tuple(
            dct.get(i.name, DefaultArg) for i in self.description
        ))

    def __init__(self, *args):
        i = 0
        while i < len(args) and i < len(self.description):
            descr = self.description[i]
            if args[i] is DefaultArg:
                setattr(self, descr.name, descr())
            else:
                setattr(self, descr.name, descr(args[i]))
            i += 1
        while i < len(self.description):
            descr = self.description[i]
            setattr(self, descr.name, descr())
            i += 1

    def __str__(self):
        res = "{ " + ', '.join("{}: {}"
                .format(i.name, getattr(self, i.name))
                for i in self.description
            ) + " }"
        return res

    def __repr__(self):
        return str(self)

    @property
    def description(self):
        return self.__class__.ITEMS_DESCRIPTION

    @property
    def placeholder(self):
        return self.__class__.ITEMS_PLACEHOLDER

    def tolist(self):
        return tuple(getattr(self, i.name) for i in self.description)
