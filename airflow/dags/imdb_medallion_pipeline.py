import os
import sys
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)
# ruff: noqa: E402
# isort: skip_file

from airflow.models import DAG
from airflow.providers.standard.operators.python import PythonOperator

from src.extract.download_dataset import download_dataset
from src.transform.bronze import create_bronze_layer
from src.transform.silver import create_silver_layer
from src.transform.gold import create_gold_layer
from src.transform.analytics import create_analytics_layer

with DAG(
    dag_id="imdb_medallion_pipeline",
    start_date=datetime(2026, 6, 18),
    schedule="@daily",
    catchup=False,
    tags=["imdb", "etl", "medallion"],
):

    extract = PythonOperator(
        task_id="extract_dataset",
        python_callable=download_dataset,
    )

    bronze = PythonOperator(
        task_id="create_bronze_layer",
        python_callable=create_bronze_layer,
    )

    silver = PythonOperator(
        task_id="create_silver_layer",
        python_callable=create_silver_layer,
    )

    gold = PythonOperator(
        task_id="create_gold_layer",
        python_callable=create_gold_layer,
    )

    analytics = PythonOperator(
        task_id="create_analytics_layer",
        python_callable=create_analytics_layer,
    )

    # Definindo a dependência de fluxo
    extract >> bronze >> silver >> gold >> analytics
