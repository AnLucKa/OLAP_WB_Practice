drop table if exists default.kafkaOffsets;
create table if not exists default.kafkaOffsets
(
    table_id        UInt64,
    offset          UInt64,
    timestamp       DateTime,
    dt_load         MATERIALIZED now()
)
engine MergeTree()
order by (table_id)
TTL dt_load + interval 1 day;


drop table if exists default.tableNames;
create table if not exists default.tableNames
(
    table_id        UInt64,
    table_name      String
)
engine MergeTree()
order by (table_id);

insert into default.tableNames values
(1, 'ShkOnPlaceState_log');
