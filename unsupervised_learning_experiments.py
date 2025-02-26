# -*- coding: utf-8 -*-
"""Unsupervised Learning Experiments.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eilX1iQRoT7CcJMpUQWc28m3Y-MWdt0R
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

input_file=  "https://github.com/grindrllc/public-datasets/blob/aa1d3a2c1df6005b33c8900d1113660a4b77feb5/example_view_df.csv?raw=true"
df = pd.read_csv(input_file)
print(df.head())

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, to_date, weekofyear, count, lag
from pyspark.sql.window import Window

# Create a spark session to begin creating spark elements
spark = SparkSession.builder.appName("ViewAnalysis").getOrCreate()
input_file=  "https://github.com/grindrllc/public-datasets/blob/aa1d3a2c1df6005b33c8900d1113660a4b77feb5/example_view_df.csv?raw=true"
import requests

local_filename = "/tmp/df.csv"
# download file locally
response = requests.get(input_file)
# something we can write to
with open(local_filename, "wb") as f:
  f.write(response.content)
df = spark.read.csv(local_filename, header = True, inferSchema = True)

# Sort by timestamp
df_sorted = df.orderBy("timestamp")

# count unique viewer IDs
unique_viewers = df.select(countDistinct("viewer_id")).collect()[0][0]

# distribution of views per day
df_day = df.withColumn("date",to_date("timestamp"))
dist_day = df_day.groupby("date").agg(count("viewer_id").alias("viewcount"))
dist_day.show()

import pandas as pd
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import NMF
from sklearn.preprocessing import StandardScaler
from scipy.signal import find_peaks
from datetime import datetime

df = pd.read_csv(input_file, parse_dates=["timestamp"])

# feature engineering
df["date"] = df["timestamp"].dt.date # access date
df["week"] = df["timestamp"].dt.isocalendar().week
df["hour"] = df["timestamp"].dt.hour

# 1: Clustering users based on viewer behavior
user_stats = df.groupby("viewer_id").agg({"timestamp":["count","min","max"]}) # different ways to look into timestamp
user_stats.columns=["viewcount","firstview","lastview"]
# HW: subtract first view from last view to find activity span. Create a new feature called activity span inside of user_stats.
user_stats["activity_span"] = (user_stats["lastview"] - user_stats["firstview"]).dt.days #column called activity span

scaler = StandardScaler()
user_features = scaler.fit_transform(user_stats[["activity_span","viewcount"]])

# KMeans Clustering
kmeans = KMeans(n_clusters=4, random_state = 2025)
user_stats["cluster"] = kmeans.fit_predict(user_features)


# anomaly detection
isoforest = IsolationForest(contamination=0.05, random_state=2025)
user_stats["anomaly"] = isoforest.fit_predict(user_features)

# graph analysis to look at pagerank and community detection
G = nx.DiGraph()
for _,row in df.iterrows():
    G.add_edge(row["viewer_id"],row["viewed_id"])

page_rank_scores = nx.pagerank(G)
user_stats["page_rank_scores"] = user_stats.index.map(lambda x: page_rank_scores.get(x,0)) # queries for x keys, if doesn't exist, 0
