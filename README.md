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


