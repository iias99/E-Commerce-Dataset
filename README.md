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
# Progect Workflow

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
```
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


## Data Processing & Analysis
### 1.Data Transformation
  -Extracted **date** and **time** from the original timestamp column using PySpark SQL functions.

  -Created to separate column :
   -`event_date` : containing only the date (format: YYY-MM-DD)
   -`event_timen`: containing only the time (format: HH:mm:ss)
 
 Droped the original `event_time` column after transformation to simplify the structure.

<img width="1220" height="503" alt="7" src="https://github.com/user-attachments/assets/9fa892e7-3773-4f56-aa6f-a10ac81b2df0" />

**Separated the date and time** from the event timestamp into two independent columns (`event_date` and `event_timen`) to make time-based analysis easier.

from
### 2.Data Cleaning

