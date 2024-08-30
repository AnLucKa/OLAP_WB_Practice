create database dq;

create table dq.tareArrival engine = ReplacingMergeTree order by dt_load_hour as
select toStartOfHour(dt_load) dt_load_hour
     , count() cnt
     , uniq(tare_id) uniq_tare_id
     , countIf(tare_id, tare_id < 1) cnt_0_tare_id
     , countIf(dt_arrived, dt_arrived < '2024-01-01') cnt_invalid_dt_arrived
     , countIf(dt_reported, dt_reported < '2024-01-01') cnt_invalid_dt_reported
     , uniq(tare_sticker) uniq_tare_sticker
     , countIf(tare_sticker, tare_sticker = '') cnt_0_tare_sticker
     , uniq(tare_type) uniq_tare_type
     , countIf(tare_type, tare_type = '') cnt_0_tare_type
     , uniq(office_id) uniq_office_id
     , countIf(office_id, office_id < 1) cnt_0_office_id
     , uniq(employee_id) uniq_employee_id
     , countIf(employee_id, employee_id < 1) cnt_0_employee_id
     , uniq(wh_id) uniq_wh_id
     , countIf(wh_id, wh_id < 1) cnt_0_wh_id
     , uniq(place_cod) uniq_place_cod
     , countIf(place_cod, place_cod < 1) cnt_0_place_cod
     , uniq(wh_tare_entry) uniq_wh_tare_entry
     , countIf(wh_tare_entry, wh_tare_entry = '') cnt_0_wh_tare_entry
     , countIf((dt_load - dt_arrived) > 1800) cnt_late_data
from default.tareArrival
group by dt_load_hour
order by dt_load_hour;
