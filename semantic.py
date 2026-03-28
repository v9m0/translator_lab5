from ast_nodes import ClassNode, MemberNode


class SemanticError(Exception):
    def __init__(self, message: str, line: int = 0):
        loc = f" (строка {line})" if line else ""
        super().__init__(f"[Семантика]{loc}: {message}")


SymbolInfo  = dict[str, str]
SymbolTable = dict[str, SymbolInfo]
ClassTable  = dict[str, SymbolTable]


class SemanticAnalyzer:
    def analyze(self, node: ClassNode) -> ClassTable:
        table: SymbolTable = {}

        for member in node.members:
            self._check_member(member, node.name, table)
            table[member.name] = {
                "type":     member.type_,
                "modifier": member.modifier if member.modifier else "(нет)",
            }

        return {node.name: table}

    def _check_member(
        self,
        member: MemberNode,
        class_name: str,
        existing: SymbolTable,
    ) -> None:
        if member.name in existing:
            raise SemanticError(
                f"поле '{member.name}' объявлено повторно в классе '{class_name}'",
                line=member.line,
            )

        if member.name == class_name:
            raise SemanticError(
                f"имя поля '{member.name}' совпадает с именем класса",
                line=member.line,
            )


def format_table(class_table: ClassTable) -> str:
    lines = []

    for class_name, fields in class_table.items():
        lines.append(f"Класс: {class_name}")

        if not fields:
            lines.append("  (нет полей)")
            continue

        col_name = max(len("Поле"),     max(len(n) for n in fields))
        col_type = max(len("Тип"),      max(len(v["type"]) for v in fields.values()))
        col_mod  = max(len("Модификатор"), max(len(v["modifier"]) for v in fields.values()))

        sep_top = f"┌{'─' * (col_name + 2)}┬{'─' * (col_type + 2)}┬{'─' * (col_mod + 2)}┐"
        sep_mid = f"├{'─' * (col_name + 2)}┼{'─' * (col_type + 2)}┼{'─' * (col_mod + 2)}┤"
        sep_bot = f"└{'─' * (col_name + 2)}┴{'─' * (col_type + 2)}┴{'─' * (col_mod + 2)}┘"

        header = (
            f"│ {'Поле':<{col_name}} │ {'Тип':<{col_type}} │ {'Модификатор':<{col_mod}} │"
        )

        lines.append(sep_top)
        lines.append(header)
        lines.append(sep_mid)

        for field_name, info in fields.items():
            row = (
                f"│ {field_name:<{col_name}} "
                f"│ {info['type']:<{col_type}} "
                f"│ {info['modifier']:<{col_mod}} │"
            )
            lines.append(row)

        lines.append(sep_bot)

    return "\n".join(lines)
