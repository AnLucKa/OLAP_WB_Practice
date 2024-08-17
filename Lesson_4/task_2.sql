-- Создание супер юзера
create user SUPER_USER identified with sha256_password by 'SUPER_PASS';

-- Выдача всех прав
grant current grants on *.* to SUPER_USER with grant option;
