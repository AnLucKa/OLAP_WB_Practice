import json
import random
import time
from datetime import datetime
from clickhouse_driver import Client


with open('./secrets/ch.json') as json_file:
    data = json.load(json_file)

client = Client(data['server'][0]['host'],
                user=data['server'][0]['user'],
                password=data['server'][0]['password'],
                port=data['server'][0]['port'],
                verify=False,
                database='',
                compression=True)


if __name__ == '__main__':
    # Генерация shk_id
    shks = [random.randint(10000000, 10000000000) for _ in range(100)]

    # Генерация статуса
    states = ['WLT', 'WLR', 'WLI', 'AIP', 'WIJ', 'PEP', 'WPU', 'WPI', 'IPM', 'PTS', 'SPM', 'WIW', 'MDV', 'MCM', 'ASI',
                'PBI', 'WSR', 'WSC', 'IPS', 'SGP', 'LPR', 'LWA']

    # Генерация place_cod
    place_cods = [random.randint(10000000, 10000000000) for _ in range(100)]

    # Генерация dt
    today = datetime.now()
    dts = []
    for _ in range(10):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        random_date = datetime(today.year, today.month, today.day, hour, minute, second)
        #date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')
        dts.append(random_date)


    while True:
        data = []
        for i in range(20):
            shk_id = random.choice(shks)
            state_id = random.choice(states)
            place_cod = random.choice(place_cods)
            dt = random.choice(dts)

            data.append((shk_id, state_id, place_cod, dt))

        rows = client.execute(
            'INSERT INTO direct_log.ShkOnPlace_narrow_buf (*) VALUES',
            data
        )

        time.sleep(10)
