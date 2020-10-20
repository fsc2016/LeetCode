from typing import *
import findspark
findspark.init()
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType
from pyspark.ml.feature import OneHotEncoder,StringIndexer
from pyspark.ml import Pipeline
# from pyspark.sql.functions import explode,split
from pyspark.sql.functions import *
from pyspark.ml.linalg.Vectors import sparse




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
    多变量编码
    :param df:
    :return:
    '''

def myudf(indexes:List,size):
    return sparse(size,indexes.sort(),len(indexes)*[1.0])





if __name__ == '__main__':

    spark = SparkSession.builder.appName('learn_ml').master('local[*]').getOrCreate()
    df=spark.read.format('csv').option("header", "true").load('./data/movies.csv')
    df = spark.read.csv( path='./data/movies.csv',inferSchema=True,header=True)
    df.printSchema()
    df.show(5)
    df.head()
    # df2 = spark.createDataFrame([(2,), (5,), (5,)], ('age',))
    # print(df2.agg(collect_list('age')).collect())


    # # 独热编码
    # df = df.withColumn('movieIdNumber', df.movieId.cast(IntegerType()))
    # oneHotEncoderExample(df)

    # multiHotEncoderExample
    # multiHotEncoderExample(df)
    dfWithGenre = df.select('movieId', 'title', explode(split(df.genres, '\\|')).alias('genre'))
    # dfWithGenre.show(10)
    stringIndex = StringIndexer(inputCol='genre',outputCol='genreIndex')
    stringIndexerModel=stringIndex.fit(dfWithGenre)
    genreIndexSamples=stringIndexerModel.transform(dfWithGenre)
    # genreIndexSamples.show(10)
    genreIndexSamples=genreIndexSamples.withColumn('genreIndexInt',genreIndexSamples.genreIndex.cast(IntegerType()))
    genreIndexSamples.show(10)
    # genreIndexSamples.printSchema()
    # 一共有多少类型
    indexSize = genreIndexSamples.agg({'genreIndexInt':'max'}).collect()[0][0]+1
    # indexSize = genreIndexSamples.select('genreIndexInt').rdd.max()[0]+1
    # print(indexSize)
    processedSamples = genreIndexSamples.groupBy('movieId').agg(collect_list('genreIndexInt').alias('genreIndexes')).withColumn("indexSize", lit(indexSize))
    processedSamples.show(10)

    array2vec=udf(f=myudf,returnType=ArrayType)
    finalSample=processedSamples.withColumn('vector',array2vec(processedSamples['genreIndexes'],processedSamples['indexSize']))
    finalSample.show(10)











