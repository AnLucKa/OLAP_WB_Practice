# ДЗ 2
## Задание 2.2 ##
### Postgres
Запускаем контейнер
```
docker run -d --name pg -p 8080:8080 -e POSTGRES_USER=golovanov -e POSTGRES_PASSWORD=password -e PGDATA=/var/lib/postgresql/data/pgdata -v ./pg_data:/var/lib/postgresql/data --restart always --cpus 1 -m 256m postgres
```
где
- `-d` указываем не перехватывать управление
- `--name pg` задаем контейнеру имя pg 
- `-p 8080:8080` пробрасываем порт
- `-e POSTGRES_USER=golovanov` устанавливаем переменную окружения в соответствующее значение
- `-e POSTGRES_PASSWORD=password` устанавливаем переменную окружения в соответствующее значение
- `-e PGDATA=/var/lib/postgresql/data/pgdata` устанавливаем переменную окружения в соответствующее значение
- `-v ./pg_data:/var/lib/postgresql/data` пробрасываем тома
- `--restart=always` указываем перезапускать контейнер всегда, вне зависимости от причины его остановки
- `--cpus 1` указываем ограничение количества CPU, доступных контейнеру
- `-m 256m` указываем ограничение опреативной памяти, доступной контейнеру
Перезапуск контейнера
```
docker restart pg
```
Остановка контейнера
```
docker stop pg
```
Удаление контейнера
```
docker rm pg
```
### ClickHouse
Запускаем контейнер
```
docker run -d --name ch -p 8123:8123 -e CLICKHOUSE_USER=username -e CLICKHOUSE_PASSWORD=password -v ./ch_data:/var/lib/clickhouse/ --restart always --cpus 1 -m 256m clickhouse/clickhouse-server
```
где
- `-d` указываем не перехватывать управление
- `--name ch` задаем контейнеру имя ch 
- `-p 8123:8123` пробрасываем порт
- `-e CLICKHOUSE_USER=usernamev` устанавливаем переменную окружения в соответствующее значение
- `-e CLICKHOUSE_PASSWORD=password` устанавливаем переменную окружения в соответствующее значение
- `-v ./ch_data:/var/lib/clickhouse/` пробрасываем тома
- `--restart=always` указываем перезапускать контейнер всегда, вне зависимости от причины его остановки
- `--cpus 1` указываем ограничение количества CPU, доступных контейнеру
- `-m 256m` указываем ограничение опреативной памяти, доступной контейнеру
Перезапуск контейнера
```
docker restart ch
```
Остановка контейнера
```
docker stop ch
```
Удаление контейнера
```
docker rm ch
```
