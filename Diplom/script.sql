create table if not exists default.ShkOnPlaceState_log
(
    shk_id      UInt64,
    dt          DateTime,
    state_id    LowCardinality(String),
    place_cod   UInt64,
    place_name  String,
    wh_id       UInt64,
    office_id   UInt64,
    entry       String,
    dt_load     MATERIALIZED now()
)
engine MergeTree()
order by (shk_id)
partition by toStartOfWeek(dt_load, 1)
TTL dt_load + interval 1 year;


drop table if exists default.StoragePlace;
create table if not exists default.StoragePlace
(
    place_cod   UInt64,
    place_name  String,
    wh_id       UInt64,
    office_id   UInt64
)
engine = MergeTree()
order by (place_cod);
