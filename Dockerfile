FROM apache/airflow:2.7.0

ENV AIRFLOW_HOME=/opt/airflow

# Install FastAPI and Uvicorn
RUN pip install --no-cache-dir \
    mysql-connector-python \
    apache-airflow \
    tensorflow \
    numpy \
    matplotlib \
    imutils \
    scipy \
    beautifulsoup4 \
    requests \
    uvicorn

RUN pip install --no-cache fastapi

RUN pip install python-multipart
