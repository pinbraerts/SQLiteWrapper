from utils import _clb

class Annotator:
    def __init__(self, *mod):
        self.mod = ' '.join(str(i) for i in mod if i is not None)
        self.origin = None

    def __or__(self, other):
        if isinstance(other, Annotator):
            self.mod += other.mod
        else:
            self.origin = other
        return self

    def __ror__(self, other):
        if isinstance(other, Annotator):
            self.mod += other.mod
        else:
            self.origin = other
        return self

    @classmethod
    def map(cls, name=None):
        return lambda *args: cls(name, *args)

def annotate_all(cls):
    for i, j in cls.__dict__.items():
        if not i.startswith('_') and not _clb(i):
            setattr(cls, i, Annotator(j))
    return cls

@annotate_all
class Conflict:
    Rollback = "ROLLBACK"
    Abort = "ABORT"
    Fail = "FAIL"
    Ignore = "IGNORE"
    Replace = "REPLACE"

@annotate_all
class Order:
    Ascending = "ASC"
    Descending = "DESC"

conflict = Anontator.map()
constraint = Annotator.map("CONSTRAINT")
primary_key = Annotator("PRIMARY KEY")
autoincrement = Annotator("AUTOINCREMENT")

not_null = Annotator("NOT NULL")
unique = Annotator("UNIQUE")

default = Annotator.map("DEFAULT")
collate = Annotator.map("COLLATE")
unique = Annotator("UNIQUE")
