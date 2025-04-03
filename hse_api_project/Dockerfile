FROM apache/airflow:2.10.4

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
RUN airflow db init

USER root
RUN apt-get update && \
    apt-get install wget --yes && \
    mkdir --parents ~/.mongodb && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
         --output-document /tmp/root.crt && \
    chmod 0644 /tmp/root.crt

USER airflow
COPY root.crt /tmp/root.crt
COPY requirements.txt /tmp/requirements.txt
# RUN pip uninstall bson
RUN pip install --no-cache-dir -r /tmp/requirements.txt