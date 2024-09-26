# kafka Offset
## 1. Поднимаем нужные контейнеры:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_18.png)
ch_kafka - кликхаус, в котором будут храниться Offset'ы.
## 2. Данные в кафке:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_1.png)
## 3. Создаем на локальном клике нужные таблицы:
Выполняем скрипт [script.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/script.sql)<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_2.png)<br>Также выполняем [script_2.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/script_2.sql), чтобы создать нужные таблицы на ch_kafka. оффсеты будут храниться у нас в таблице default.kafkaOffsets, также добавляем словарь с соответствием table_id и table_name, чтобы не делать первичный ключ по столбцу String. <br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_3.png)
## 4. Spark-таска:
Для предотвращения сброса offset'а мы будем комбинировать встроенную checkpoint систему с записью последнего для каждого батча offset'а в кликхаус:
* если файл с чекпоинтом присутствует в директории, spark руководствуется им в начале работы
* если он отсутсвует, выставляется offset в соответствии с данными бд
* если иотсутствует любая информация, начинаем считывать топик сначала.
## 4. Старт Spark-таски (3-й вариант):
Запускаем таску:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_4.png)<br>И после нескольких батчей прерываем ее:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_5.png)<br>Заполнение таблицы default.shkOnPlaceState_log на этом этапе:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_7.png)<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_8.png)
## 5. Удаляем чекпоинт и запускаем заново (2-й вариант):
Удаляем чекпонит<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_6.png)
<br>Запускаем таску:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_9.png)<br>И после нескольких батчей прерываем ее:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_10.png)<br>Заполнение таблицы default.shkOnPlaceState_log на этом этапе:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_12.png)<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_13.png)
<br>Содержимое таблицы с оффсетами:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_11.png)
## 6. Запускаем в третий раз (1-й вариант):
Запускаем таску:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_14.png)<br>И после нескольких батчей прерываем ее:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_15.png)<br>Заполнение таблицы default.shkOnPlaceState_log на этом этапе:<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_16.png)<br>![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Diplom/imgs/Screenshot_17.png)
