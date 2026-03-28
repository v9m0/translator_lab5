# Анализатор

Классический сканер и рекурсивный нисходящий предикативный распознаватель с семантикой.

---

## Грамматика:

```ebnf
<Class>   ::= class id { <members> }
<members> ::= <member> <members> | ε
<member>  ::= <mod> <type> id ;
<mod>     ::= private | public | protected | ε
<type>    ::= int | float | str | id
```
---



## Запуск

### Интерактивный режим:

```bash
python3 main.py
```

После запуска программа ждёт ввод объявления класса.
Текст можно ввести:
- в одну строку
- в несколько строк

Ввод заканчивается пустой строкой.

Пример ввода по строкам:

```txt
> class Test {
  public int x;
  private str y;
  Test z;
  }

```

Пример ввода в одну строку:

```txt
> class Test { public int x; private str y; Test z; }

```

---

### Чтение из файла:

```bash
python3 main.py path/to/input.txt
```

Сохранение результата в файл:

```bash
python3 main.py path/to/input.txt -o result
```

## Пример входных данных

```txt
class Test { public int x; private str y; Test z; }
```
---
#### Выполнил Витаев Абдул-Малик Ихванович
#### КМБО-05-23

