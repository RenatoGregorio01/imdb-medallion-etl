FROM apache/airflow:3.2.2

USER root

COPY requirements-airflow.txt /requirements-airflow.txt

USER airflow

RUN pip install --no-cache-dir -r /requirements-airflow.txt
