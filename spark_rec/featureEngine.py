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


def oneHotEncoderExample(df):
    # pipe版本
    stringIndexer = StringIndexer(inputCol='movieIdNumber',outputCol='movieIdIndex').setHandleInvalid("keep")
    # dropLast是否drop掉类别最少的那一类
    encoder = OneHotEncoder(inputCol='movieIdIndex',outputCol='movieIdVector',dropLast=False)
    pipeline = Pipeline(stages=[stringIndexer,encoder])
    model = pipeline.fit(df)
    encode_df = model.transform(df)
    encode_df.show(10)

def multiHotEncoderExample(df):
    '''
    对genres进行多热编码
    :param df:
    :return:
    '''
    dfWithGenre = df.select('movieId', 'title', explode(split(df.genres, '\\|')).alias('genre'))

    # StringIndexer对genre建立index
    stringIndex = StringIndexer(inputCol='genre', outputCol='genreIndex')
    stringIndexerModel = stringIndex.fit(dfWithGenre)
    genreIndexSamples = stringIndexerModel.transform(dfWithGenre) #genreIndex type=double
    genreIndexSamples = genreIndexSamples.withColumn('genreIndexInt', genreIndexSamples.genreIndex.cast(IntegerType()))
    genreIndexSamples.show(10)

    # genreIndexSamples.printSchema()
    # 一共有多少类型
    # indexSize = genreIndexSamples.agg({'genreIndexInt': 'max'}).collect()[0][0] + 1
    indexSize = genreIndexSamples.agg(F.max(col('genreIndexInt'))).collect()[0][0] + 1
    # indexSize = genreIndexSamples.select('genreIndexInt').rdd.max()[0]+1
    print(indexSize)

    processedSamples = genreIndexSamples.groupBy('movieId').agg(collect_list('genreIndexInt').alias('genreIndexes')).withColumn("indexSize", lit(indexSize))
    processedSamples.show(5)

    #用户自定义函数，注意返回值类型
    array2vec = udf(f=tmpArray2vec, returnType=VectorUDT())
    finalSample = processedSamples.withColumn('vector', array2vec(processedSamples['genreIndexes'],processedSamples['indexSize']))
    finalSample.show(10)

def ratingFeatures(rating_df):
    '''
    处理评论数据
    :param rating_df:
    :return:
    '''
    rating_df.printSchema()
    rating_df.show(10)

    # 用户自定义函数
    double2vec = udf(f=tmpDouble2vec, returnType=VectorUDT())
    movieFeatures = rating_df.groupBy(col('movieId')).agg(count(lit(1)).alias('ratingCount'),
                                                          avg(col('rating')).alias('avgRating'),
                                                          variance(col('rating')).alias('ratingVar')).withColumn(
        'avgRatingVec', double2vec(col('avgRating')))

    movieFeatures.show(10,truncate=True)

    userFeatures = rating_df.groupBy(col('userId')).agg(count(lit(1)).alias('ratingCount'),
                                                        avg(col('rating')).alias('avgRating'),
                                                        variance(col('rating')).alias('ratingVar'))
    userFeatures.show(10,truncate=True)

    movieFeatures.printSchema()

    # 分箱
    ratingCountDiscretizer = QuantileDiscretizer(inputCol='ratingCount', outputCol='ratingCountBucket',
                                                 numBuckets=100).setHandleInvalid('keep')
    # 归一化
    ratingScaler = MinMaxScaler(inputCol='avgRatingVec', outputCol='scaleAvgRating')

    pipe = Pipeline(stages=[ratingCountDiscretizer, ratingScaler])
    model = pipe.fit(movieFeatures)
    movieProcessedFeatures = model.transform(movieFeatures)
    movieProcessedFeatures.show(10,truncate=True)
    movieProcessedFeatures.printSchema()

def tmpArray2vec(indexes,size):
    indexes.sort()
    return Vectors.sparse(size,indexes,len(indexes)*[1.0])

def tmpDouble2vec(x):
    return Vectors.dense(x)


if __name__ == '__main__':

    spark = SparkSession.builder.appName('learn_ml').master('local[*]').getOrCreate()
    df=spark.read.format('csv').option("header", "true").load('./data/movies.csv')
    # df = spark.read.csv( path='./data/movies.csv',inferSchema=True,header=True)
    # df.printSchema()
    # df.show(5)
    # df2 = spark.createDataFrame([(2,), (5,), (5,)], ('age',))
    # print(df2.agg(collect_list('age')).collect())


    # # 独热编码
    # df = df.withColumn('movieIdNumber', df.movieId.cast(IntegerType()))
    # oneHotEncoderExample(df)

    # multiHotEncoderExample
    # multiHotEncoderExample(df)

    #ratingFeatures
    rating_df = spark.read.format('csv').option("header", "true").load(path='./data/ratings.csv')
    ratingFeatures(rating_df)




















