from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from clickhouse_driver import Client

import os
import pandas as pd
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Нужно указать, чтобы spark подгрузил lib для kafka.
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 --packages org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 pyspark-shell'

# Загружаем конекты. Не выкладываем в гит файл с конектами.
with open('/opt/spark/Streams/credentials.json') as json_file:
    сonnect_settings = json.load(json_file)

ch_local_db_name = "default"
ch_local_dst_table = "ShkOnPlaceState_log"
ch_kafka_db_name = "default"
ch_kafka_dst_table = "kafka"

client = Client(сonnect_settings['ch_local'][0]['host'],
                user=сonnect_settings['ch_local'][0]['user'],
                password=сonnect_settings['ch_local'][0]['password'],
                port=сonnect_settings['ch_local'][0]['port'],
                verify=False,
                database=ch_local_db_name,
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)

client_kafka = Client(сonnect_settings['ch_kafka'][0]['host'],
                user=сonnect_settings['ch_kafka'][0]['user'],
                password=сonnect_settings['ch_kafka'][0]['password'],
                port=сonnect_settings['ch_kafka'][0]['port'],
                verify=False,
                database=ch_kafka_db_name,
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)

# Разные переменные, задаются в params.json
spark_app_name = "ShkOnPlaceState_log_pipeline"
spark_ui_port = "8081"

kafka_host = сonnect_settings['kafka'][0]['host']
kafka_port = сonnect_settings['kafka'][0]['port']
kafka_topic = "My_topic"
kafka_batch_size = 50
processing_time = "5 second"

checkpoint_path = f'/opt/kafka_checkpoint_dir/{spark_app_name}/{kafka_topic}/v1'

# Подключаемся к ClickHouse и получаем последний оффсет
def get_last_offset():
    # Запрос для получения последнего оффсета из таблицы offset'ов
    sql_offset_query = """
        SELECT max(offset) 
        FROM default.kafkaOffsets 
        WHERE table_id = 1 
        AND dt_load = (SELECT max(dt_load) FROM default.kafkaOffsets)
    """

    result = client_kafka.execute(sql_offset_query)
    return result[0][0]

# Если папка с чекпоинтами пустая, то берем отступ из бд
if any(os.listdir(checkpoint_path)):
    offset = 'earliest'
    print('Чекпоинт обнаружен. Восстанавливаем сессию с помощью него.')
else:
    off = get_last_offset()
    if off != 0:
        offset = '{"My_topic":{"0":' + f'{get_last_offset()+1}' + '}}'
        print(f'Чекпоинт не обнаружен. Восстанавливаем сессию с помощью бд. Задаем offset равный {off+1}')
    else:
        offset = '{"My_topic":{"0":' + f'{get_last_offset()}' + '}}'
        print(f'Чекпоинт не обнаружен. В базе данных пусто. Начинаем считывать топик сначала, задаем offset равный 0')

# Создание сессии спарк.
spark = SparkSession \
    .builder \
    .appName(spark_app_name) \
    .config('spark.ui.port', spark_ui_port)\
    .config("spark.dynamicAllocation.enabled", "false") \
    .config("spark.executor.cores", "1") \
    .config("spark.task.cpus", "1") \
    .config("spark.num.executors", "1") \
    .config("spark.executor.instances", "1") \
    .config("spark.default.parallelism", "1") \
    .config("spark.cores.max", "1") \
    .config('spark.ui.port', spark_ui_port)\
    .getOrCreate()

# убираем разные Warning.
spark.sparkContext.setLogLevel("WARN")
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.debug.maxToStringFields", 500)

# Описание как создается процесс spark structured streaming.
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{kafka_host}:{kafka_port}") \
    .option("subscribe", kafka_topic) \
    .option("maxOffsetsPerTrigger", kafka_batch_size) \
    .option("startingOffsets", offset) \
    .option("failOnDataLoss", "false") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .load()

# .option("kafka.sasl.jaas.config", f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{kafka_user}" password="{kafka_password}";') \
# .option("kafka.sasl.mechanism", "PLAIN") \
# .option("kafka.security.protocol", "SASL_PLAINTEXT") \

# Колонки, которые писать в ClickHouse. В kafka много колонок, не все нужны. Этот tuple нужен перед записью в ClickHouse.
columns_to_ch = ("shk_id", "dt", "state_id", "place_cod")


# Схема сообщений в топике kafka. Используется при формировании batch.
schema = StructType([
    StructField("shk_id", LongType(), False),
    StructField("dt", StringType(), True),
    StructField("state_id", StringType(), False),
    StructField("place_cod", LongType(), False)
])

sql_tmp_create = """create table tmp.tmp_ShkOnPlaceState_log
    (
        shk_id      UInt64,
        dt          DateTime,
        state_id    LowCardinality(String),
        place_cod   UInt64
    )
        engine = Memory
"""

sql_insert = f"""insert into {ch_local_db_name}.{ch_local_dst_table}
    select shk_id
        , dt
        , state_id
        , place_cod
        , t2.place_name
        , t2.wh_id
        , t2.office_id
        , 'shkOnPlaceState_log_kafka' entry
    from tmp.tmp_ShkOnPlaceState_log t1
    left any join
    (
        select place_cod, place_name, wh_id, office_id
        from default.StoragePlace
        where place_cod in (select place_cod from tmp.tmp_ShkOnPlaceState_log)
    ) t2
    on t1.place_cod = t2.place_cod
"""

client.execute("drop table if exists tmp.tmp_ShkOnPlaceState_log")

def column_filter(df):
    # select только нужные колонки.
    col_tuple = []
    for col in columns_to_ch:
        col_tuple.append(f"value.{col}")
    return df.selectExpr(col_tuple)


def load_to_ch(df):
    # Преобразуем в dataframe pandas и записываем в ClickHouse.
    df_pd = df.toPandas()
    client.insert_dataframe('INSERT INTO tmp.tmp_ShkOnPlaceState_log VALUES', df_pd)

# Функция обработки batch. На вход получает dataframe-spark.
def foreach_batch_function(df2, epoch_id):

    df_rows = df2.count()
    # Если dataframe не пустой, тогда продолжаем.

    if df_rows > 0:
        # df2.printSchema()
        # df2.show(5)

        # Убираем не нужные колонки.
        df2_filtered = column_filter(df2)

        client.execute(sql_tmp_create)

        # Записываем dataframe в ch.
        load_to_ch(df2_filtered)

        # Добавляем объем и записываем в конечную таблицу.
        client.execute(sql_insert)
        client.execute("drop table if exists tmp.tmp_ShkOnPlaceState_log")

        # Получаем запись с максимальным оффсетом и временем
        last_record = df2.orderBy(col("offset").desc()).first()

        # Запись offset и timestamp в отдельную таблицу
        last_offset = last_record.offset
        last_timestamp = last_record.timestamp
        last_timestamp_formatted = last_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # SQL запрос для записи информации о последнем оффсете и времени
        insert_offset_sql = f"""
            INSERT INTO default.kafkaOffsets (table_id, offset, timestamp)
            VALUES (1, {last_offset}, '{last_timestamp_formatted}')
        """
        client_kafka.execute(insert_offset_sql)
        print(f"Строка (1, {last_offset}, '{last_timestamp_formatted}') вставлена в default.kafkaOffsets")

# Описание как создаются микробатчи. processing_time - задается вначале скрипта
query = df.select(
        from_json(col("value").cast("string"), schema).alias("value"),
        "offset",
        "timestamp",
        "topic") \
    .writeStream \
    .trigger(processingTime=processing_time) \
    .option("checkpointLocation", checkpoint_path) \
    .foreachBatch(foreach_batch_function) \
    .start()

query.awaitTermination()