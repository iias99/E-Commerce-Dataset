```
#projectSpark
from pyspark.sql import SparkSession 
from pyspark.sql import functions  as f
from pyspark.sql.functions import *
from pyspark.sql.window import Window 
from pyspark.sql.functions import col , date_format ,substring 
from pyspark.sql.functions import struct 
from pyspark.sql.functions import udf
from pyspark.sql.functions import avg, max, min
from pyspark.sql.types import StructType, StructField, StringType, FloatType ,IntegerType
#Optimization Stage
spark=SparkSession.builder \
     .appName("NovData") \
     .master("local[*]") \
     .config("spark.executor.memory","8g") \
     .config("spark.driver.memory","8g") \
     .config("spark.sql.shuffle.partitions","100")\
     .config("spark.serializer","org.apache.spark.serializer.KryoSerializer") \
     .config("spark.sql.adaptive.enabled","True") \
     .config("spark.sql.adaptive.coalescePartitions.enabled","true") \
     .config("spark.sql.adaptive.skewJoin.enabled","true") \
     .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df= spark.read.csv("hdfs://localhost:9a000//Asrar/2019-Nov.csv",header=True,inferSchema= True)
df.printSchema()
df.limit(10).show() 
#cleaning Stage 
df= df.withColumn("event_date",to_date(col("event_time"))) \
     .withColumn("event_timen",date_format(col("event_time"),"HH:mm:ss"))\
     .drop("event_time") 
df=df.select("event_date","event_timen",* [c for c in df.columns if c not in ("event_date","event_timen")])
df.show(5,truncate=False)  
df=df.withColumn("category_id",substring(col("category_id").cast("string"),1,4))\
     .fillna({"category_code":0,"brand":0})
df.show()
df=df.withColumn("price",col("price").cast("int"))
df.show(10)
#anlaysis Stage
windowSpec=Window.partitionBy("user_id").orderBy(f.desc("price"))
df.withColumn("row_number",f.row_number().over(windowSpec)).show()
df.groupBy("user_id").agg(count("user_session").alias("sessions_count")).show(10)
df.createOrReplaceTempView("dataset")
spark.sql(""" select user_session , Sum(price) as Total_price
     from dataset 
     group By user_session
     order by Total_price DESC""").show()
spark.sql(""" select user_id , brand , price 
          from dataset
          where price <= 200
          order by price DESC
          """).show()
subquery1=(""" select brand , total_brand
          from ( select brand, count (*) as total_brand
          from dataset
          group by brand
          ) As top_brand 
          where total_brand > 1000
          order by total_brand Desc
    
""")
spark.sql(subquery1).show()

subquery2= (''' select category_code ,total_category
            from ( select category_code  ,count(*) as total_category
            from dataset
            group by category_code
            ) As top_category
            order by total_category Desc
''')
spark.sql(subquery2).show()

```
