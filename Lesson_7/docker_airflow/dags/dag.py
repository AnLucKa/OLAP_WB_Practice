from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from clickhouse_driver import Client
from sqlalchemy import create_engine
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 29)
}

dag = DAG(
    dag_id='rep_SOP',
    default_args=default_args,
    schedule_interval='5-55/15 * * * *',
    description='Test DAG',
    catchup=False,
    max_active_runs=1
)


def main():

    client = Client('192.168.1.2',
                        user='default',
                        password='default',
                        port=9000,
                        verify=False,
                        database='default',
                        settings={"numpy_columns": False, 'use_numpy': True},
                        compression=False)

    client.execute("""INSERT INTO report.ShkOnPlaceState_log_agg 
                      select toDate(dt)    dt_date
                           , state_id
                           , count(shk_id) qty_shk
                      from ShkOnPlaceState_log
                      group by dt_date, state_id""")

    to_import = """select dt_date 
                         , state_id 
                         , qty_shk
                    from report.ShkOnPlaceState_log_agg"""

    df = client.query_dataframe(to_import)
    df['dt_date'] = pd.to_datetime(df['dt_date']).dt.date
    engine = create_engine('postgresql://default:default@192.168.1.2:5432/postgres')
    df.to_sql('ShkOnPlaceState_log_agg', engine, if_exists="append")
    print('ready')


task1 = PythonOperator(
    task_id='rep_SOP', python_callable=main, dag=dag)
