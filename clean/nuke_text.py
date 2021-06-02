# -*- coding: utf-8 -*-
# Language Analysis ABSA v4.0
#
# Nuke Text (still in development)
# DO NOT USE THIS FILE
#
# Copyright (C) 2019-2021 Guide Analytics
# Author: Michael Brock Li <michael.brock.li@gmail.com>
#
# URL: <https://guideanalytics.ca>



from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import regexp_replace, udf, collect_list, col
from pyspark.sql.types import StringType
from punctuation import PunctuationRemoval
from pyspark import SparkContext, SparkConf
import random
import time

# Initiate Spark Context (for result output)
sc = SparkContext(appName="Nuke Review Text", master="local[2]",
                  conf=SparkConf().set('spark.ui.port',
                                       random.randrange(4000, 5000)))

# Initiate Spark Session
spark = SparkSession.builder.appName('Nuke Review Text')\
    .master("local[2]")\
    .config('spark.ui.port', random.randrange(4000, 5000)).getOrCreate()

data_path = 'gs://gide_analytics/output/comp/*.parquet'
output_path = 'gs://gide_analytics/output/text_output_comp/'


# load_dataset_and_set_views:
# Purpose: reading the company_reviews from csv through SPARK
# Input; [String] pathR, pathA
# Output: [Spark DataFrame] rev_data, auth_data
def load_dataset_and_set_views(pathR="GOOGLE_REVIEWS.csv"):#, pathA="REVIEWS_AUTHORS.csv"):

    """
    :param pathR: default csv file: GOOGLE_REVIEWS.csv
    :param pathA: default csv file: REVIEWS_AUTHORS.csv
    :return: spark, reviews DataFrame, authors DataFrame
    """

    # Try not to touch these commands.
    # These are normal Spark functions and it is the quickest way to handle Spark company_reviews
    while True:
        """
        try:
            rev_data_raw = spark.read.csv(pathR, mode="PERMISSIVE", header='true', sep=',', inferSchema=True,
                                          multiLine=True, quote='"', escape='"')

            auth_data_raw = spark.read.csv(pathA, mode="PERMISSIVE", header='true', sep=',', inferSchema=True,
                                           multiLine=True, quote='"', escape='"')
            break
        except:
        
        """
        try:
            rev_data_raw = spark.read.parquet(pathR)
            #auth_data_raw = spark.read.parquet(pathA)
            break
        except:
            print('Trying again in 10 seconds')
            time.sleep(10)

    """
    rev_data_raw = rev_data_raw.withColumn('compReview Text', regexp_replace('Review Text', '"', ''))
    auth_data_raw = auth_data_raw.withColumn('Review Text', regexp_replace('Review Text', '"', ''))
    auth_data_raw = auth_data_raw.withColumn("Business Name", regexp_replace("Business Name", '"', ''))
    auth_data_raw = auth_data_raw.withColumn("Business Adddress", regexp_replace("Business Adddress", '"', ''))
    
  
    # Setting up Database/DataFrame header names
    rev_data = rev_data_raw.toDF("rev_id", "Business Rating", "Business Reviews", "Source URL",
                                 "Business Name", "Author Name", "Local Guide", "review_text", "Review Rating",
                                 "Review Date", "Author URL", "Like", "Review Photo", "Scraped Time")

    auth_data = auth_data_raw.toDF("auth_id", "Note", "Level", "Reviews Count", "Ratings Count",
                                   "Source URL", "Source Business Name", "Business Name", "Business Address",
                                   "review_text", "Author", "Review Rating",
                                   "Review Date", "Reviewer URL", "Scraped Time", "Like", "Review Photo")
    """
    # Creating Temp views (for extracting and testing purposes)
    rev_data_raw.createOrReplaceTempView("rev_data")
    #auth_data_raw.createOrReplaceTempView("auth_data")

    return spark, rev_data_raw #, auth_data_raw


def nuke_text(prod_data, col_name = 'companyReviewText'):

    print(prod_data.count())
    prod_data = prod_data.select(col_name)
    try:
        filter_reviews = prod_data.where(col(col_name)).isNotNull()
    except:
        try:
            filter_reviews = prod_data.na.drop(subset=[col_name])
        except:
            filter_reviews = prod_data.filter(col_name + "is not NULL")
    #filter_reviews = prod_data.select(col).filter(prod_data[col].isNotNull())
    print(filter_reviews.count())

    data_size = int(filter_reviews.count() / 50)
    filter_reviews = filter_reviews.repartition(data_size)
    remove_punc = PunctuationRemoval()
    udf_punc = udf(remove_punc.remove_nuke, StringType())
    punc_remov_pd = filter_reviews.withColumn(col_name, udf_punc(col_name)).cache()


    # joined_data = punc_remov_pd.select(col).rdd

    # print(joined_data.take(10))
    punc_remov_pd.select(col_name).coalesce(1).write.mode('overwrite').text(output_path)


_, rev_data = load_dataset_and_set_views(pathR=data_path)
nuke_text(rev_data)
