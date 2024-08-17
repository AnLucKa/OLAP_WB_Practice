-- Создаем БД
create database stg;
create database history;
create database current;
create database direct_log;

-- Создаем таблицы
create table if not exists stg.ShkOnPlace_narrow
(
    shk_id      UInt64,
    state_id    LowCardinality(String),
    place_cod   UInt64,
    dt          DateTime,
    dt_load     MATERIALIZED now()
)
engine MergeTree()
order by (shk_id)
TTL dt_load + interval 1 week
COMMENT 'Узкая ШКнаМХ. stg слой';


create table if not exists history.ShkOnPlace_narrow
(
    shk_id      UInt64,
    state_id    LowCardinality(String),
    place_cod   UInt64,
    dt          DateTime,
    dt_load     MATERIALIZED now()
)
engine MergeTree
order by (shk_id)
partition by toStartOfWeek(dt_load, 1)
TTL dt_load + interval 1 year
COMMENT 'Узкая ШКнаМХ. History слой';


create table if not exists current.ShkOnPlace_narrow
(
    shk_id      UInt64,
    state_id    LowCardinality(String),
    place_cod   UInt64,
    dt          DateTime,
    dt_load     MATERIALIZED now()
)
engine ReplacingMergeTree(dt)
order by (shk_id)
COMMENT 'Узкая ШКнаМХ. Сurrent слой';


create table if not exists direct_log.ShkOnPlace_narrow_buf
(
    shk_id      UInt64,
    state_id    LowCardinality(String),
    place_cod   UInt64,
    dt          DateTime,
    dt_load     MATERIALIZED now()
)
engine = Buffer('stg', 'ShkOnPlace_narrow', 16, 10, 100, 10000, 1000000, 10000000, 100000000)
COMMENT 'Буферная таблица для узкой ШКнаМХ';
