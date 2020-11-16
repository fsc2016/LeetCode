from typing import *
import findspark
findspark.init()
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType,StringType
from pyspark.ml.feature import OneHotEncoder,StringIndexer,QuantileDiscretizer,MinMaxScaler
from pyspark.ml import Pipeline
# from pyspark.sql.functions import explode,split
from pyspark.sql.functions import udf,col,when,split,format_number,stddev,count,lit,avg,collect_list,reverse
from pyspark.sql import Window
from collections import defaultdict
from pyspark.ml.linalg import VectorUDT,Vectors

def addSampleLabel(ratingSamples:DataFrame) -> DataFrame:
    '''
    筛选大于3.5的评分评论
    :param ratingSamples:
    :return:
    '''
    # ratingSamples.show(5,truncate=60)
    sampleCount = ratingSamples.count()
    # 查看打分大致分布
    ratingSamples.groupBy('rating').count().orderBy('rating').withColumn('percentage',col('count')/sampleCount).show(10,truncate=False)
    #将过滤3.5评分的数据
    ratingSamples=ratingSamples.withColumn('label',when(ratingSamples['rating']>=3.5,1).otherwise(0))
    return ratingSamples

def extractReleaseYear(title:str):
    if not title or len(title) < 6 :
        return 1990
    else:
        return int(title.strip()[-5:-1])

def extractTitle(title:str):
    if title:
        return title.strip()[:len(title)-6]
    else:
        return title

def addMovieFeatures(movieSamples:DataFrame,ratingSamples:DataFrame):
    '''
    处理电影特征
    :param movieSamples:
    :param ratingSamples:
    :return:
    '''
    samplesWithMovies1 = ratingSamples.join(movieSamples,on='movieId',how='left')
    # samplesWithMovies1.show(10,truncate=True)
    extractReleaseYearUdf = udf(f=extractReleaseYear,returnType=IntegerType())
    extractTitleUdf = udf(f=extractTitle,returnType=StringType())

    #use udf
    samplesWithMovies2 = samplesWithMovies1.withColumn('releaseYear',extractReleaseYearUdf(col('title'))).withColumn('newTitle',extractTitleUdf(col('title'))).drop('title')

    # samplesWithMovies2.show(10,truncate=True)

    samplesWithMovies3=samplesWithMovies2.withColumn('movieGenre1',split(col('genres'),'\\|').getItem(0)).withColumn('movieGenre2',split(col('genres'),'\\|').getItem(1)).withColumn('movieGenre3',split(col('genres'),'\\|').getItem(2))

    # samplesWithMovies3.show(10,truncate=True)

    movieRatingFeatures = samplesWithMovies3.groupBy('movieId').agg(count(lit(1)).alias('movieRatingCount'),
            format_number(avg(col('rating')),2).alias('movieAvgRating'),
            format_number(stddev(col('rating')),2).alias('movieRatingStddev')).na.fill(0)

    # movieRatingFeatures.show(10, truncate=True)

    samplesWithMovies4 = samplesWithMovies3.join(movieRatingFeatures,on='movieId',how='left')
    # samplesWithMovies4.printSchema()
    # samplesWithMovies4.show(10,truncate=True)
    return samplesWithMovies4

def extractGenres(genres):
    genMap = defaultdict(int)
    for genre in genres:
        for i in genre.split('\\|'):
            genMap[i] +=1
    genList = sorted(genMap.items(),key=lambda a:a[1],reverse=True)
    genList = [i[0] for i in genList]
    return genList


def addUserFeatures(df:DataFrame):
    '''
    提取用户特征
    :param df:
    :return:
    '''
    extractGenresUdf = udf(extractGenres,returnType=ArrayType(IntegerType()))
    print('start user feature')
    samplesWithUserFeatures = df.withColumn('userPositiveHistory',collect_list(when(col('label')==1,col('movieId')).otherwise(lit(None))).over(Window.partitionBy('userId').orderBy(col('timestamp')).rowsBetween(-100,-1)))\
        .withColumn('userPositiveHistory',reverse(col('userPositiveHistory'))) \
        .withColumn("userRatedMovie1", col("userPositiveHistory").getItem(0))  \
        .withColumn("userRatedMovie2", col("userPositiveHistory").getItem(1)) \
        .withColumn("userRatedMovie3", col("userPositiveHistory").getItem(2)) \
        .withColumn("userRatedMovie4", col("userPositiveHistory").getItem(3)) \
        .withColumn("userRatedMovie5", col("userPositiveHistory").getItem(4)) \
        .withColumn('userRatingCount',count(lit(1)).over(Window.partitionBy('userId').orderBy(col('timestamp')).rowsBetween(-100,-1))) \
        .withColumn('userAvgReleaseYear',avg(col('releaseYear')).over(Window.partitionBy("userId").orderBy(col('timestamp')).rowsBetween(-100, -1)).cast('int')) \
        .withColumn('userReleaseYearStddev',stddev(col('releaseYear')).over(Window.partitionBy('userId').orderBy(col('timestamp')).rowsBetween(-100,-1))) \
        .withColumn('userAvgRating',format_number(avg(col('rating')).over(Window.partitionBy('userId').orderBy(col('timestamp')).rowsBetween(-100,-1)),2)) \
        .withColumn('userRatingStddev',    stddev(col("rating")).over(Window.partitionBy("userId").orderBy(col("timestamp")).rowsBetween(-100, -1))) \
        .withColumn('userGenres',extractGenresUdf(collect_list(when(col('label') == 1,col('genres')).otherwise(lit(None))).over(Window.partitionBy('userId').orderBy(col('timestamp')).rowsBetween(-100,-1)))).na.fill(0) \
        .withColumn("userRatingStddev", format_number(col("userRatingStddev"), 2)) \
        .withColumn("userReleaseYearStddev", format_number(col("userReleaseYearStddev"), 2)) \
        .withColumn("userGenre1", col("userGenres").getItem(0)) \
        .withColumn("userGenre2", col("userGenres").getItem(1)) \
        .withColumn("userGenre3", col("userGenres").getItem(2)) \
        .withColumn("userGenre4", col("userGenres").getItem(3)) \
        .withColumn("userGenre5", col("userGenres").getItem(4))\
        .drop("genres", "userGenres", "userPositiveHistory").filter(col('userRatingCount') > 1)

    samplesWithUserFeatures.printSchema()
    samplesWithUserFeatures.show(100,truncate=True)


if __name__ == '__main__':
    spark = SparkSession.builder.appName("featureEng").master('local[*]').getOrCreate()
    ratedf = spark.read.format('csv').option('header','true').load('./data/ratings.csv')
    moviedf = spark.read.format('csv').option('header','true').load('./data/movies.csv')
    ratingSamplesWithLabel =  addSampleLabel(ratedf)
    ratingSamplesWithLabel.show(10,truncate=60)

    samplesWithMovieFeatures=addMovieFeatures(moviedf,ratingSamplesWithLabel)
    addUserFeatures(samplesWithMovieFeatures)


