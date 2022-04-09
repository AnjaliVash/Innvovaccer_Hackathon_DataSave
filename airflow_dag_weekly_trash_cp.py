from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 
from airflow.contrib.sensors.file_sensor import FileSensor

from bin.int_medications import int_meds_auto_updt, storage, insert, del_stag, int_med_stag_clean


DAG_DEFAULT_ARGS = {
'owner':'airflow',
'depends_on_past':False,
'retires':1,
'schedule_interval':'@weekly'
}


dagToRun = DAG(dag_id = 'int_meds_dag_v1', 
           start_date=datetime(2022, 10, 10), 
           default_args = DAG_DEFAULT_ARGS,
           catchup = False)


cmd_command = "cp <filename> /path/written/where/all/files/willaccumulte/to/Trash"
#and these files after accoumulating to trash will be delted in 7 days time.
data_loading = BashOperator(
         task_id = "int_meds",
         bash_command = cmd_command,
         dag=dagToRun)


Sleeprun= BashOperator(
    task_id="sleep",
    bash_command ="sleep 10",
    dag=dagToRun
)

data_loading >> Sleeprun