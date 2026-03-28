from token_types import Token, TokType
from ast_nodes import ASTNode, ClassNode, MemberNode

# FIRST для member
_MOD_TOKENS   = {TokType.PUBLIC, TokType.PRIVATE, TokType.PROTECTED}
_TYPE_TOKENS  = {TokType.INT, TokType.FLOAT, TokType.STR, TokType.IDENT}
_MEMBER_FIRST = _MOD_TOKENS | _TYPE_TOKENS


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(
            f"[Парсер] строка {token.line}, позиция {token.col}: {message}"
        )


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self._idx    = 0

    def _peek(self) -> Token:
        if self._idx >= len(self._tokens):
            return Token(TokType.END, None, 0, 0)
        return self._tokens[self._idx]

    def _consume(self) -> Token:
        tok = self._peek()
        self._idx += 1
        return tok

    def _match(self, *kinds: TokType) -> bool:
        return self._peek().kind in kinds

    def _expect(self, kind: TokType, msg: str) -> Token:
        tok = self._peek()
        if tok.kind != kind:
            raise ParseError(msg, tok)
        return self._consume()

    def _at_end(self) -> bool:
        return self._peek().kind == TokType.END

    def p_class(self) -> ClassNode:
        tok = self._expect(TokType.CLASS, "ожидается ключевое слово 'class'")
        name_tok = self._expect(TokType.IDENT, "ожидается имя класса после 'class'")
        self._expect(TokType.LBRACE, f"ожидается '{{' после имени класса '{name_tok.val}'")
        members = self._p_members()
        self._expect(TokType.RBRACE, "ожидается '}' в конце тела класса")

        if not self._at_end():
            raise ParseError(
                f"неожиданный токен '{self._peek().val}' после закрывающей скобки",
                self._peek()
            )

        return ClassNode(name=name_tok.val, members=members, line=tok.line)

    def _p_members(self) -> list[MemberNode]:
        members = []
        while self._match(*_MEMBER_FIRST):
            members.append(self._p_member())
        return members

    def _p_member(self) -> MemberNode:
        modifier = self._p_mod()
        type_str = self._p_type()
        name_tok = self._expect(
            TokType.IDENT,
            f"ожидается имя поля после типа '{type_str}'"
        )
        self._expect(
            TokType.SEMI,
            f"ожидается ';' после объявления поля '{name_tok.val}'"
        )
        return MemberNode(
            modifier=modifier,
            type_=type_str,
            name=name_tok.val,
            line=name_tok.line,
        )

    def _p_mod(self) -> str:
        tok = self._peek()
        if tok.kind in _MOD_TOKENS:
            self._consume()
            return tok.val
        return ""

    def _p_type(self) -> str:
        tok = self._peek()
        if tok.kind in _TYPE_TOKENS:
            self._consume()
            return tok.val
        raise ParseError(
            f"ожидается тип (int, float, str или имя класса), получено '{tok.val}'",
            tok
        )
