# Домашнее задание 4
## 1. Поднимаем в докере кликхаус и подключаемся:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/imgs/Screenshot_1.png)
## 2. Создаем супер пользователя:
Выполняем скрипт [task_2.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/task_2.sql)
## 3. Создаем базы данных и таблицы:
Выполняем скрипт [task_2.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/task_3.sql)<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/imgs/Screenshot_6.png)
## 4. Создаем роли readonly_role и stg_role и соответствующих пользователей:
Выполняем скрипт [task_4.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/task_4.sql)
## 5. Заполним stg слой посредством буферки:
Для этого выполним скрипт [main.py](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/py_script/main.py), который заливает данные в буфферную таблицу<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/imgs/Screenshot_7.png)
## 6. Создаем буферные представления для пролива данных в слои history и current:
Выполняем скрипт [task_6.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/task_6.sql)<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/imgs/Screenshot_8.png)
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_4/imgs/Screenshot_9.png)
