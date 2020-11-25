from typing import *
import findspark
findspark.init()
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType,StringType
from pyspark.ml.feature import OneHotEncoder,StringIndexer,QuantileDiscretizer,MinMaxScaler
import redis
from pyspark.sql.functions import udf,col,when,split,format_number,stddev,count,lit,avg,collect_list,reverse,row_number
from pyspark.sql import Window
from collections import defaultdict
from pyspark.ml.linalg import VectorUDT,Vectors

HOST = 'localhost'
PORT = '6379'
def addSampleLabel(ratingSamples:DataFrame) -> DataFrame:
    '''
    增加label列
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

    # samplesWithUserFeatures.printSchema()
    # samplesWithUserFeatures.show(100,truncate=True)
    return  samplesWithUserFeatures

def extractAndSaveMovieFeaturesToRedis(df:DataFrame):
    # 获取每部电影最新的评论那一行，最为该电影的特征
    movieLatestSamples = df.withColumn('movieRowNum',row_number().over(Window.partitionBy('movieId').orderBy(col('timestamp').desc())))\
        .filter(col('movieRowNum')==1) \
        .select("movieId","releaseYear", "movieGenre1","movieGenre2","movieGenre3","movieRatingCount","movieAvgRating", "movieRatingStddev").na.fill('')

    movieLatestSamples.printSchema()
    movieLatestSamples.show(10,truncate=True)

    movieFeaturePrefix = "mf:"
    totalMovies=movieLatestSamples.count()

    pool = redis.ConnectionPool(host=HOST,port=PORT)
    # key的存活时间 秒
    ex = 60 * 60
    r = redis.Redis(connection_pool=pool)
    for n,row in enumerate(movieLatestSamples.collect()):
        movie={}
        movie['releaseYear'] = row['releaseYear']
        movie['movieGenre1'] = row['movieGenre1']
        movie['movieGenre2'] = row['movieGenre2']
        movie['movieGenre3'] = row['movieGenre3']
        movie['movieRatingCount'] = row['movieRatingCount']
        movie['movieAvgRating'] = row['movieAvgRating']
        movieKey = '{}{}'.format(movieFeaturePrefix,row['movieId'])
        r.hmset(movieKey,movie)
        r.expire(movieKey,ex)

        if n % 100 == 0:
            print(str(n) + "/" + str(totalMovies) + "...")


def extractAndSaveUserFeaturesToRedis(df:DataFrame):
    userLatestSamples = df.withColumn('userRowNum',row_number().over(Window.partitionBy('userId').orderBy(col('timestamp').desc()))) \
            .filter(col('userRowNum') == 1) \
            .select("userId","userRatedMovie1", "userRatedMovie2","userRatedMovie3","userRatedMovie4","userRatedMovie5","userRatingCount", "userAvgReleaseYear", "userReleaseYearStddev", "userAvgRating", "userRatingStddev","userGenre1", "userGenre2","userGenre3","userGenre4","userGenre5").na.fill('')

    userLatestSamples.printSchema()
    userLatestSamples.show(5, truncate=True)

    userLatestSamples.repartition(1).write.option('header', 'true').csv('./data/modelSamplesRow')



    # userFeaturePrefix = "uf:"
    # totalUsers = userLatestSamples.count()
    # pool = redis.ConnectionPool(host=HOST, port=PORT)
    # # key的存活时间 秒
    # ex = 60 * 60
    # r = redis.Redis(connection_pool=pool)
    # for n, row in enumerate(userLatestSamples.collect()):
    #     user = {}
    #     user['userRatedMovie1'] = row['userRatedMovie1']
    #     user['userRatedMovie2'] = row['userRatedMovie2']
    #     user['userRatedMovie3'] = row['userRatedMovie3']
    #     user['userRatedMovie4'] = row['userRatedMovie4']
    #     user['userRatedMovie5'] = row['userRatedMovie5']
    #     user['userRatingCount'] = row['userRatingCount']
    #     user['userAvgReleaseYear'] = row['userAvgReleaseYear']
    #     user['userReleaseYearStddev'] = row['userReleaseYearStddev']
    #     user['userAvgRating'] = row['userAvgRating']
    #     user['userRatingStddev'] = row['userRatingStddev']
    #     user['userGenre1'] = row['userGenre1']
    #     user['userGenre2'] = row['userGenre2']
    #     user['userGenre3'] = row['userGenre3']
    #     user['userGenre4'] = row['userGenre4']
    #     user['userGenre5'] = row['userGenre5']
    #     userKey = '{}{}'.format(userFeaturePrefix, row['userId'])
    #     r.hmset(userKey, user)
    #     r.expire(userKey, ex)
    #
    #     if n % 1000 == 0:
    #         print(str(n) + "/" + str(totalUsers) + "...")

if __name__ == '__main__':
    spark = SparkSession.builder.appName("featureEng").master('local[*]').getOrCreate()
    ratedf = spark.read.format('csv').option('header','true').load('./data/ratings.csv')
    moviedf = spark.read.format('csv').option('header','true').load('./data/movies.csv')
    ratingSamplesWithLabel =  addSampleLabel(ratedf)
    ratingSamplesWithLabel.show(10,truncate=60)

    samplesWithMovieFeatures=addMovieFeatures(moviedf,ratingSamplesWithLabel)
    samplesWithUserFeatures=addUserFeatures(samplesWithMovieFeatures)


    # samplesWithMovieFeatures.show(10,truncate=60)
    # extractAndSaveMovieFeaturesToRedis(samplesWithMovieFeatures)

    # pandaDF=samplesWithUserFeatures.toPandas()
    # pandaDF.to_csv('./data/samplesWithMovieFeatures.csv')


    samplesWithMovieFeatures.repartition(1).write.option('header','true').csv('./data/modelsamples')
    extractAndSaveUserFeaturesToRedis(samplesWithUserFeatures)



