# Домашнее задание 5
## 1. Поднимаем нужные контейнеры:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_5.png)
## 2. Данные в кафке:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_1.png)
## 3. Создаем на локальном клике нужные таблицы:
Выполняем скрипт [task_2.sql](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/script.sql)<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_6.png)
## 4. Запускаем Spark-таску:
Выполняем код:<br>
`pip install clickhouse_driver clickhouse_cityhash lz4 pandas`<br><br>
`spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 --executor-cores 1 --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" /opt/spark/Streams/shkOnPlaceState_log_sync.py`<br>Результат:<br>
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_2.png)
## 5. Результирующая таблица в клике:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_3.png)
## 6. Скриншот веб-интефейса спарк:
![Image alt](https://github.com/AnLucKa/OLAP_WB_Practice/blob/main/Lesson_5/imgs/Screenshot_4.png)
