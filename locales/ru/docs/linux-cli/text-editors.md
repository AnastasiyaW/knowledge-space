---
title: "Текстовые редакторы в терминале"
category: reference
tags: [linux-cli, vim, nano, editors]
level: 3
source_sha256: b0cd44fa78212fbecfecd1af8cce49095b7e1616ac2eefa2cd8b9b696b6e5c30
translation: machine
translated_at: '2026-10-24'
---
# Текстовые редакторы в терминале {#terminal-text-editors}

nano удобен для начинающих; vim — стандартный инструмент опытных пользователей, который есть практически в каждой Linux-системе. Эта статья описывает основные горячие клавиши и команды обоих редакторов.

## Nano {#nano}

Запуск: `nano filename` или `nano -B filename` (создать резервную копию при сохранении).

### Операции с файлами {#file-operations}

| Клавиша | Действие |
|----------|--------|
| Ctrl+S | Сохранить |
| Ctrl+O | Сохранить как |
| Ctrl+X | Выйти |
| Ctrl+R | Вставить файл |

### Редактирование {#editing}

| Клавиша | Действие |
|----------|--------|
| Ctrl+K | Вырезать строку |
| Alt+6 | Копировать строку |
| Ctrl+U | Вставить |
| Alt+U | Отменить |
| Alt+E | Повторить |
| Alt+3 | Закомментировать/раскомментировать |

### Поиск {#search}

| Клавиша | Действие |
|----------|--------|
| Ctrl+W | Поиск вперёд |
| Ctrl+Q | Поиск назад |
| Alt+R | Поиск и замена |
| Alt+W | Найти следующее |

### Навигация {#navigation}

| Клавиша | Действие |
|----------|--------|
| Ctrl+A / Ctrl+E | Начало / конец строки |
| Ctrl+Y / Ctrl+V | Страница вверх / страница вниз |
| Alt+\ / Alt+/ | Начало / конец файла |
| Alt+G | Переход к номеру строки |
| Alt+N | Переключить нумерацию строк |

## Vim {#vim}

Модальный редактор с тремя основными режимами: **Normal**, **Insert**, **Visual**.

### Переключение режимов {#mode-switching}

```sql
i           Insert at cursor
a           Insert after cursor
I / A       Insert at line start / end
o / O       New line below / above, enter insert
Esc         Return to Normal mode
v           Visual mode (character)
V           Visual mode (line)
Ctrl+v      Visual block mode
```

### Перемещение курсора (Normal) {#cursor-movement-normal}

```text
h j k l     Left, down, up, right
w / b       Next / previous word
0 / $       Start / end of line
^           First non-blank character
gg          Top of file
G           Bottom of file
:[num]      Go to line
Ctrl+d/u    Half page down / up
{ / }       Previous / next paragraph
```

### Редактирование (Normal) {#editing-normal}

```sql
dd          Delete (cut) line
d$          Delete to end of line
dw          Delete word
cc          Change (delete + insert) line
J           Join line below
r[char]     Replace single character
.           Repeat last command
x           Delete character under cursor
```

### Текстовые объекты {#text-objects}

```sql
di(         Delete inside parentheses
ci"         Change inside quotes
da{         Delete around braces (including braces)
yi[         Yank inside brackets
```

### Буфер обмена {#clipboard}

```text
yy          Yank (copy) line
p / P       Paste after / before cursor
```

### Сохранение и выход {#save-and-exit}

```bash
:w          Save
:wq         Save and quit
:q          Quit (fails if unsaved)
:q!         Force quit without saving
```

### Поиск и замена {#search-and-replace}

```text
/pattern    Search forward
?pattern    Search backward
n / N       Next / previous match
:%s/old/new/g    Replace all in file
:%s/old/new/gc   Replace with confirmation
```

### Отмена и повтор {#undo-redo}

```text
u           Undo
Ctrl+r      Redo
```

### Окна и вкладки {#windows-and-tabs}

```text
:e file     Open file
:tabe       New tab
gt / gT     Next / previous tab
:vsp        Vertical split
Ctrl+ww     Switch between windows
Ctrl+wq     Close window
```

### Метки {#marks}

```text
m{a-z}      Set local mark
'{a-z}      Jump to mark
''          Return to previous position
```

## Подводные камни {#gotchas}

- Vim запускается в режиме Normal: нажатие букв выполняет команды, а не печатает текст
- `:q!` отбрасывает все изменения без подтверждения
- nano показывает горячие клавиши внизу экрана (`^` означает Ctrl)
- Vim предустановлен почти во всех Linux-системах, nano может потребоваться установить
- На многих системах `vi` — это на самом деле `vim` (Vi IMproved)
- В vim `u` отменяет одно изменение за раз, а `U` отменяет все изменения в текущей строке

## См. также {#see-also}

- [[terminal-basics|Оболочка и горячие клавиши]] - Оболочка и горячие клавиши
- [[file-operations|Создание и просмотр файлов]] - Создание и просмотр файлов
