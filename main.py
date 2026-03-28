import sys
import os
from scanner  import Scanner,  ScanError
from mparser   import Parser,   ParseError
from semantic import SemanticAnalyzer, SemanticError, format_table


def run(source: str, out_path: str | None = None) -> None:
    output_lines: list[str] = []

    def emit(line: str = ""):
        print(line)
        output_lines.append(line)

    emit(source)

    try:
        scanner = Scanner(source)
        tokens  = scanner.scan_all()
    except ScanError as e:
        print(f"\n{e}", file=sys.stderr)
        return

    emit()
    emit("Tokens")
    for tok in tokens[:-1]:
        emit(str(tok))

    try:
        parser = Parser(tokens)
        class_node = parser.p_class()
    except ParseError as e:
        print(f"\n{e}", file=sys.stderr)
        return

    emit()
    emit("AST")
    emit(repr(class_node))

    try:
        analyzer    = SemanticAnalyzer()
        class_table = analyzer.analyze(class_node)
    except SemanticError as e:
        print(f"\n{e}", file=sys.stderr)
        return

    emit()
    emit("Symbol table")
    emit(format_table(class_table))
    emit()

    if out_path:
        filepath = out_path if out_path.endswith(".txt") else out_path + ".txt"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print(f"\nРезультат сохранён в: {filepath}")


def main():
    args     = sys.argv[1:]
    out_path = None

    if "-o" in args:
        i = args.index("-o")
        if i + 1 < len(args):
            out_path = args[i + 1]
            args = args[:i] + args[i + 2:]
        else:
            print("Ошибка: после -o должно быть имя файла", file=sys.stderr)
            sys.exit(1)

    if args:
        filepath = args[0]
        if not os.path.isfile(filepath):
            print(f"Ошибка: файл '{filepath}' не найден", file=sys.stderr)
            sys.exit(1)
        with open(filepath, encoding="utf-8") as f:
            source = f.read().strip()
        run(source, out_path)

    else:
        print("Транслятор языка описания классов")
        print("Введите объявление класса (пустая строка — конец ввода):")
        print("Пример: class Test { public int x; private str y; Test z; }")
        print()

        lines = []
        try:
            while True:
                line = input("> " if not lines else "  ")
                if line == "":
                    break
                lines.append(line)
        except EOFError:
            pass

        if not lines:
            print("Ввод пуст.")
            return

        source = " ".join(lines)
        run(source, out_path)


if __name__ == "__main__":
    main()
