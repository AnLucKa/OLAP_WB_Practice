from confluent_kafka import Producer
import json
from clickhouse_driver import Client


dbname = 'default'

with open('./secrets/ch.json') as json_file:
    data = json.load(json_file)

client = Client(data['server'][0]['host'],
                user=data['server'][0]['user'],
                password=data['server'][0]['password'],
                port=data['server'][0]['port'],
                verify=False,
                database=dbname,
                settings={"wait_end_of_query": True,
                          "numpy_columns": False, 'use_numpy': False},
                compression=True)

config = {
    'bootstrap.servers': '192.168.1.2:29092',  # адрес Kafka сервера
    'client.id': 'simple-producer',
    # 'sasl.mechanism':'PLAIN',
    # 'security.protocol': 'PLAINTEXT',
}

producer = Producer(**config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_message(data):
    try:
        # Асинхронная отправка сообщения
        producer.produce('My_topic', data.encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Поллинг для обработки обратных вызовов
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

if __name__ == '__main__':
    query = 'select distinct shk_id, dt, state_id, place_cod from ShkOnPlaceState_log limit 10000'
    rows = client.execute(query)

    for row in rows:
        json_row = json.dumps(
            {
                'shk_id': row[0],
                'dt': row[1].strftime('%Y-%m-%dT%H:%M:%S'),
                'state_id': row[2],
                'place_cod': row[3]
            }
        )
        print(f'{json_row} sent to kafka.')
        send_message(json_row)
        producer.flush()