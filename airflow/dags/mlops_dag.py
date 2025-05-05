from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    'mlops_drift_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    description='Pipeline de detección de drift y reentrenamiento automático',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 1),
    catchup=False,
) as dag:

    check_drift = BashOperator(
        task_id='check_drift',
        bash_command='python /opt/airflow/dags/scripts/auto_monitor.py'
    )

    check_drift