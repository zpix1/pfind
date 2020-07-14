# pfind - поиск совершенных раскрасок циркулянтных графов

## Как запустить и использовать?

### Windows
Поставьте `python3`, например [отсюда](https://www.python.org/downloads/release/python-384/).

### Linux / Mac OS
Пакет `python3` обычно уже установлен, если нет - используйте ваш пакетный менеджер.

`sudo apt-get install python3`

Далее:

Скачайте файл `pfind.py` (или весь репозиторий).

Перейдите в папку с загруженным файлом, запустите его `python3 pfind.py`. Вы получите 2-раскраски 124-графа (настройки по умолчанию):
```
ncolors=2
connections=[1, 2, 4]
p=2
(2, 2) (0, 1)
p=3
(3, 6) (0, 0, 1)
p=4
(3, 3) (0, 0, 1, 1)
p=7
(1, 6) (0, 0, 0, 0, 0, 0, 1)
(2, 5) (0, 0, 0, 0, 0, 1, 1)
(2, 5) (0, 0, 0, 0, 1, 0, 1)
(3, 4) (0, 0, 0, 0, 1, 1, 1)
(2, 5) (0, 0, 0, 1, 0, 0, 1)
(3, 4) (0, 0, 0, 1, 0, 1, 1)
(3, 4) (0, 0, 1, 0, 0, 1, 1)
(3, 4) (0, 0, 1, 0, 1, 0, 1)
p=9
(2, 4) (0, 0, 0, 0, 0, 0, 1, 1, 1)
(2, 4) (0, 0, 0, 0, 1, 0, 1, 0, 1)
(2, 4) (0, 0, 0, 1, 0, 0, 0, 1, 1)
B/C Table
*  1  2  3  4  5  6
1  -  -  -  -  -  -
2  -  1  -  -  -  -
3  -  -  1  -  -  -
4  -  3  4  -  -  -
5  -  3  -  -  -  -
6  1  -  1  -  -  -
total=14
```

В этих обозначениях:

* `ncolors` - число цветов (от 2 до 3 на данный момент).
* `connections` - дистанции в графе.
* `p=<период>` - период раскраски, после этой строки идут раскраски с указанным периодом
* Каждая раскраска задается:
    1. При `ncolors=2` строкой вида (b, c) и самой раскраской (одним периодом, где одинаковые числа означают одинаковые цвета). Также в конце будет выведена b\c таблица.
    2. При `ncolors=3` раскраской и ее матрицей параметров на следующей строке.
* `total=<всего>` - число найденных раскрасок

### Настройка

Программу можно запускать с различными параметрами, указывая дистанции флагом `-c` и число цветов флагом `-n`.

Например:

`python3 pfind.py -c 1 2 3 -n 2` - получить 2-раскраски 123-графа.