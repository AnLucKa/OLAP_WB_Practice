create materialized view stg.ShkOnPlace_narrow_history_view to history.ShkOnPlace_narrow as
select shk_id
     , state_id
     , place_cod
     , dt
from stg.ShkOnPlace_narrow;

create materialized view stg.ShkOnPlace_narrow_current_view to current.ShkOnPlace_narrow as
select shk_id
     , state_id
     , place_cod
     , dt
from stg.ShkOnPlace_narrow;