# E-Commerce-Dataset
# About the Project
 ### This project focuses on analyzing and cleaning a massive E-Commerce dataset containing over 287 million records.
 ### The goal is to improve data quality, remove duplicates, and extract key insights about customer behavior and product performance . 
---
# Technologies Used 
- Hadoop Hdfs & Yarn
- Apache Spark
- PySpark
- VS Code
- Kaggle (Data Source)
---

# Project Workflow

## Project Setup
### Before running the project, make sure the following components are installed:
- Hadoop 3.x
- Apache Spark 4.x
- Python & Pyspark 3.x

  ---
   # How to Run the Project
  To start the Hadoop and Spark services, run the following commands in the terminal:

``` 
# Start HDFS and YARN
start-all.sh
start-yarn.sh
```
![1](https://github.com/user-attachments/assets/4632fe58-d9e4-476d-b6d5-91f5106e9c4e)

----
### Upload Data to HDFS

  -Create a directory in HDFS and upload the dataset from the local system 
 ```
# Create a new directory in HDFS
hdfs dfs -mkdir /Asrar1

# Copy the dataset from local machine to HDFS
hdfs dfs -CopyFromLocal /home/asrar/2019-Nov.csv /Asrar1
``` 
![3](https://github.com/user-attachments/assets/73d06332-9e1e-462a-9c8f-b19657553cf3)

![4](https://github.com/user-attachments/assets/20a275c4-93bf-428e-baf5-eefd94e79f69)

![5](https://github.com/user-attachments/assets/9c727c7b-eb40-4ea6-b651-d012c0b66104)

---

## Spark Optimization :
Spark optimization settings were configured to improve performance and memory management.

The configuration included:
- Increasing **executor and driver memory** to 8 GB.
- Setting the **number of shuffle partitions** to 100 for balanced data distribution.
- Enabling **adaptive query execution** for automatic optimization.
- Enabling **Kryo serialization** for faster data serialization.
```python
from pyspark.sql import SparkSession
# Initialize Spark session with optimized configurations
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
```
<img width="1184" height="399" alt="6" src="https://github.com/user-attachments/assets/81a8a255-62e1-4bfc-ab53-c7a3643ddf0a" />


---


## Data Processing & Analysis
### Loding Data From HDFS
   ```python
      df=spark.csv.read("hdfs://localhost:9000//Asrar/2019-Nov.csv",header=True,inferSchema= True)
df.printSchema()
df.show() 
   ```
### 1.Data Transformation
 - Extracted **date** and **time** from the original timestamp column using PySpark SQL functions.
 - Created two separate columns :
   - `event_date` : containing only the date (format: YYYY-MM-DD)
   - `event_timen`: containing only the time (format: HH:mm:ss)
 
- Dropped the original `event_time` column after transformation to simplify the structure.
 ```python
from pyspark.sql.functions import to_date, date_format, col
df.withColumn("event_date" , to_date(col("event_time"))) \
  .withColumn( " event_timen" , date_format(col("event_time"),"HH:mm:ss")) \
  .drop("event_time")

# Used a list comprehension inside select() to loop through all columns and keep the original order without overlapping.
df.select("event_date", "event_timen", *[c for c in df.columns if c not in ("event_date", "event_timen")])

df.show(5, truncate=False)

 ```

<img width="1220" height="503" alt="7" src="https://github.com/user-attachments/assets/9fa892e7-3773-4f56-aa6f-a10ac81b2df0" />

---

### 2.Data Cleaning
- Filled missing values (`NULL`) in `category_code` and `brand` columns with default value `0` to prevent null-related issues.
  
- Trimmed long IDs in the `category_id` column to display only the first four digits for better readability using the `substring()` function.
  
- Converted the `price` column from string to integer type for consistent numerical analysis.

  ```python
  from pyspark.sql.functions import col, substring
   df = df.withColumn("category_id", substring(col("category_id").cast("string"), 1, 4)) \
          .fillna({"category_code": "0", "brand": "0"}) \
          .withColumn("price", col("price").cast("int"))

  df.show(5)
 
    ```

<img width="1164" height="590" alt="9" src="https://github.com/user-attachments/assets/700d6fd8-e070-4b7e-9710-70d09fc49fc6" />

---
### 3.Data Analysis
 - Created a window partitioned by `user_id` to analyze user behavior patterns and rank each user's viewed products based on price.
  
  
 ```python
from pyspark.sql.window import Window
from pyspark.sql import functions as f

# Create window specification
windowSpec = Window.partitionBy("user_id").orderBy(f.desc("price"))

# Apply row_number to rank products per user
df = df.withColumn("row_number", f.row_number().over(windowSpec))

df.show(20, truncate=False)

 ```
 -
 <img width="1178" height="473" alt="10" src="https://github.com/user-attachments/assets/b5575807-1a43-4905-ab52-9148d5c7eb65" />
 ---
 
  - Grouped the dataset by `user_id` and counted the number of `user_session` to analyze how many sessions each user had.

   ```python
from pyspark.sql.functions import count
 df.groupBy("user_id") \
   .agg(count("user_session").alias("sessions_count")) \
df.show(10)


 ```
<img width="864" height="391" alt="11" src="https://github.com/user-attachments/assets/78ec9fbc-0a22-4080-bc3c-8b50e33823fe" />

---

#### Using Spark SQL for Data Analysis
- Created a temporary view named `eCommerce` to run SQL queries directly on the DataFrame.  
- Calculated **total revenue per user session** using the `SUM(price)` function.

   ```python
  df.createOrReplaceTempView("eCommerce")
   spark.sql( """
   Select user_session, SUM(price) as total_price
   From eCommerce
   Group By user_session
   Order By  total_price DESC """ ).show()


  ```

<img width="715" height="608" alt="12" src="https://github.com/user-attachments/assets/8e81c071-7366-4747-8fc3-d8d7c7aa38cc" /> 

---
- Filtered data to show products below a certain price threshold (`price <= 20000`).

  
   ```python
  spark.sql( """
  Select user_id, brand, price
   From eCommerce
   Where price <= 20000
   Order By price DESC
   """ ).show()


   ```

<img width="707" height="569" alt="13" src="https://github.com/user-attachments/assets/845919aa-0b99-4090-be83-82a2b1c2ff7f" /> 

- Aggregated results to determine the **most popular brands** and **top-selling categories**

 ```python
  
 subquery1=( """ 
  Select brand , total_brand 
  from ( Select brand , Count(*) As total_brand 
         from eCommerce 
         Group By brand ) As top_brand
         Where total_brand > 10000
         Order By total_brand DESC

""" )
spark.sql(subquery1).show()
 ```


 <img width="739" height="651" alt="14" src="https://github.com/user-attachments/assets/12f5a07c-661a-46d6-911b-bc552a2014a5" />


 ---


- Analyzed **top product categories** by counting how many records belong to each `category_code`.  

 ```python
 subquery2=( """ 
  Select category_code , total_category 
  from ( select category_code , Count(*) As total_category 
         from eCommerce 
         Group By category_code ) As top_category
         Order By total_category DESC

""" )
spark.sql(subquery2).show()
 ```

<img width="770" height="608" alt="15" src="https://github.com/user-attachments/assets/d1e8c549-40d5-4c83-a058-a3aea70dc607" />
