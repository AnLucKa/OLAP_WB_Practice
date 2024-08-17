-- Роль с правами на чтение
create role readonly_role;
grant show tables, select on *.* to readonly_role;

-- Соответствующий пользователь
create user READONLY_USER identified with sha256_password by 'READONLY_PASS' default role readonly_role;

-- Роль с правами создавать и заполнять данные в БД стейджинга(stg)
create role stg_role;
grant create table, insert on stg.* to stg_role;

-- Соответствующий пользователь
create user STG_USER identified with sha256_password by 'STG_PASS' default role stg_role;
