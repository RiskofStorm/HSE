import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_json, struct, rand
import logging
logger = logging.getLogger(__name__)

def main():
    spark = SparkSession.builder \
        .appName("kafka_write_parquet") \
        .getOrCreate()

    df = spark.read.parquet("s3a://hseetl/etl_parquet/transactions_v2_clean.parquet").cache()
    rows_loaded = df.count()
    logger.info(f" LOEADED {rows_loaded} ROWS")

    while True:
        batch_df = df.limit(100)
        kafka_df = batch_df.select(to_json(struct([col(c) for c in batch_df.columns])).alias("value"))
        kafka_df.write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "rc1a-sp0t812fps48sn74.mdb.yandexcloud.net:9091") \
            .option("topic", "dataproc-kafka-topic") \
            .option("kafka.security.protocol", "SASL_SSL") \
            .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
            .option("kafka.sasl.jaas.config",
                    "org.apache.kafka.common.security.scram.ScramLoginModule required "
                    "username=\"user1\" "
                    "password=\"password1\";") \
            .save()

        logger.info("SEND 100 messages")
        logger.info("LAST ONE WAS")
        logger.info(kafka_df.tail(1,False))
        time.sleep(2)

    spark.stop()

if __name__ == "__main__":
    main()