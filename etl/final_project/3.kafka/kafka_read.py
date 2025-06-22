from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_date
from pyspark.sql.types import StructType, StringType, IntegerType, BooleanType

def main():
    spark = SparkSession.builder.appName("read_kafka_steam").getOrCreate()

    schema = StructType() \
        .add("msno", StringType()) \
        .add("payment_method_id", IntegerType()) \
        .add("payment_plan_days", IntegerType()) \
        .add("plan_list_price", IntegerType()) \
        .add("actual_amount_paid", IntegerType()) \
        .add("is_auto_renew", BooleanType()) \
        .add("transaction_date", StringType()) \
        .add("membership_expire_date", StringType()) \
        .add("is_cancel", BooleanType())

    df = spark.readStream.format("kafka") \
                        .option("kafka.bootstrap.servers", "rc1a-sp0t812fps48sn74.mdb.yandexcloud.net:9091") \
                        .option("subscribe", "dataproc-kafka-topic") \
                        .option("kafka.security.protocol", "SASL_SSL") \
                        .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
                        .option("kafka.sasl.jaas.config",
                                "org.apache.kafka.common.security.scram.ScramLoginModule required "
                                "username=\"user1\" "
                                "password=\"password1\";") \
                        .option("startingOffsets", "latest") \
                        .load()

    df = df.selectExpr("CAST(value AS STRING) as json_str") \
            .select(from_json(col("json_str"), schema).alias("data")) \
            .select("data.*") \
            .withColumn("transaction_date", to_date(col("transaction_date"), "yyyy-MM-dd")) \
            .withColumn("membership_expire_date", to_date(col("membership_expire_date"), "yyyy-MM-dd"))


    print(f'READ DataFrame ROWS {df.count()}')
    print(df.tail(100, False))



if __name__ == "__main__":
    main()