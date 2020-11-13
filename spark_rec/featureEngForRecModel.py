from typing import *
import findspark
findspark.init()
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType
from pyspark.ml.feature import OneHotEncoder,StringIndexer,QuantileDiscretizer,MinMaxScaler
from pyspark.ml import Pipeline
# from pyspark.sql.functions import explode,split
from pyspark.sql.functions import *
import pyspark.sql.functions as F
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
    ratingSamples.groupBy('rating').count().orderBy('rating').withColumn('percentage',F.col('count')/sampleCount).show(10,truncate=False)
    #将过滤3.5评分的数据
    ratingSamples=ratingSamples.withColumn('label',F.when(ratingSamples['rating']>=3.5,1).otherwise(0))
    return ratingSamples

def extractReleaseYear():

    pass
def addMovieFeatures(movieSamples:DataFrame,ratingSamples:DataFrame):
    samplesWithMovies1 = ratingSamples.join(movieSamples,on='movieId',how='left')
    samplesWithMovies1.show(10,truncate=True)










if __name__ == '__main__':
    spark = SparkSession.builder.appName("featureEng").master('local[*]').getOrCreate()
    ratedf = spark.read.format('csv').option('header','true').load('./data/ratings.csv')
    moviedf = spark.read.format('csv').option('header','true').load('./data/movies.csv')
    ratingSamplesWithLabel =  addSampleLabel(ratedf)
    ratingSamplesWithLabel.show(10,truncate=60)

    addMovieFeatures(moviedf,ratingSamplesWithLabel)


