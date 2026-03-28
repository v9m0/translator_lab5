from enum import Enum, auto


class TokType(Enum):
    CLASS     = auto()
    PUBLIC    = auto()
    PRIVATE   = auto()
    PROTECTED = auto()
    INT       = auto()
    FLOAT     = auto()
    STR       = auto()
    IDENT     = auto()
    LBRACE    = auto()
    RBRACE    = auto()
    SEMI      = auto()
    END       = auto()


class Token:
    def __init__(self, kind: TokType, val, line: int, col: int):
        self.kind = kind
        self.val  = val
        self.line = line
        self.col  = col

    def __repr__(self):
        val_str = f" '{self.val}'" if self.val is not None else ""
        return f"<{self.kind.name}{val_str} @{self.line}:{self.col}>"
