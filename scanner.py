from token_types import Token, TokType


KEYWORDS: dict[str, TokType] = {
    "class":     TokType.CLASS,
    "public":    TokType.PUBLIC,
    "private":   TokType.PRIVATE,
    "protected": TokType.PROTECTED,
    "int":       TokType.INT,
    "float":     TokType.FLOAT,
    "str":       TokType.STR,
}


class ScanError(Exception):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"[Сканер] строка {line}, позиция {col}: {message}")


class Scanner:
    def __init__(self, source: str):
        self._src  = source
        self._idx  = 0
        self._line = 1
        self._col  = 1

    def _ch(self) -> str | None:
        return self._src[self._idx] if self._idx < len(self._src) else None

    def _advance(self) -> str | None:
        ch = self._ch()
        if ch is not None:
            self._idx += 1
            if ch == "\n":
                self._line += 1
                self._col = 1
            else:
                self._col += 1
        return ch

    def _skip_whitespace(self):
        while self._ch() is not None and self._ch().isspace():
            self._advance()

    def _skip_line_comment(self):
        while self._ch() is not None and self._ch() != "\n":
            self._advance()

    def _read_ident(self) -> Token:
        start_line, start_col = self._line, self._col
        buf = []
        while self._ch() is not None and (self._ch().isalnum() or self._ch() == "_"):
            buf.append(self._advance())
        word = "".join(buf)
        kind = KEYWORDS.get(word, TokType.IDENT)
        return Token(kind, word, start_line, start_col)

    def scan_all(self) -> list[Token]:
        tokens: list[Token] = []

        while True:
            self._skip_whitespace()
            ch = self._ch()

            if ch is None:
                break

            if ch == "/" and self._idx + 1 < len(self._src) and self._src[self._idx + 1] == "/":
                self._advance()
                self._advance()
                self._skip_line_comment()
                continue

            line, col = self._line, self._col

            if ch.isalpha() or ch == "_":
                tokens.append(self._read_ident())

            elif ch == "{":
                self._advance()
                tokens.append(Token(TokType.LBRACE, "{", line, col))

            elif ch == "}":
                self._advance()
                tokens.append(Token(TokType.RBRACE, "}", line, col))

            elif ch == ";":
                self._advance()
                tokens.append(Token(TokType.SEMI, ";", line, col))

            else:
                raise ScanError(f"неизвестный символ '{ch}'", line, col)

        tokens.append(Token(TokType.END, None, self._line, self._col))
        return tokens
