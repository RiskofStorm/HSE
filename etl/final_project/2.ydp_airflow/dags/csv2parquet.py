from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import IntegerType, StringType, BooleanType
from pyspark.sql.utils import AnalysisException


spark = SparkSession.builder.appName("csv2parquet").getOrCreate()


source_path = "s3a://hseetl/transactions_v2.csv"
target_path = "s3a://hseetl/etl_parquet/transactions_v2.parquet"

try:
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(source_path)
    df = df.withColumn("actual_amount_paid", col("actual_amount_paid").cast(IntegerType())) \
           .withColumn("is_auto_renew", col("is_auto_renew").cast(BooleanType())) \
           .withColumn("is_cancel", col("is_cancel").cast(BooleanType())) \
           .withColumn("membership_expire_date", to_date(col("membership_expire_date").cast("string"), "yyyyMMdd")) \
           .withColumn("msno", col("msno").cast(StringType())) \
           .withColumn("payment_method_id", col("payment_method_id").cast(IntegerType())) \
           .withColumn("payment_plan_days", col("payment_plan_days").cast(IntegerType())) \
           .withColumn("plan_list_price", col("plan_list_price").cast(IntegerType())) \
           .withColumn("transaction_date", to_date(col("transaction_date").cast("string"),  "yyyyMMdd"))
    df = df.na.drop()
    df.write.mode("overwrite").parquet(target_path)
except Exception as e:
    print(e)
finally:
    spark.stop()