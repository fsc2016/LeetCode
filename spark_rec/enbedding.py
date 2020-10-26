import findspark
findspark.init()
from typing import *
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType,StringType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Word2Vec,Word2VecModel
from pyspark.sql.functions import *
import os

def sortByTime(movieid_time_list:List):
    '''
    按照时间戳排序，返回movieids
    :param movieid_time_list:
    :return:
    '''
    movieid_time_list.sort(key=lambda x:x[1])
    mids = [i[0] for i in movieid_time_list]
    return mids

def processItemSequence(spark:SparkSession):
    '''
    处理评分数据，筛选评分大于3.5的，按照用户id分组获取评分电影序列
    :param spark:
    :return:
    '''

    df = spark.read.format('csv').option('header', 'true').load('./data/ratings.csv')
    df.printSchema()

    sortUdf = udf(f=sortByTime,returnType=ArrayType(StringType()))
    userSeq=df.where(df['rating'] >= 3.5).groupby('userId').agg(sortUdf(collect_list(struct('movieId','timestamp'))).alias('movieIds'))\
        .withColumn('movieIdStr',array_join('movieIds',' '))
    userSeq.show(10)

    #不使用udf，速度慢一点
    # userSeq=df.where(df['rating'] >= 3.5).sort('timestamp').groupby('userId').agg(collect_list('movieId').alias('movieIds')).withColumn('movieIdStr',array_join('movieIds',' ')).show(10)

    userSeq.printSchema()
    dataset = userSeq.select('movieIds')
    return dataset

def trainItem2vec(dataset):
    '''
    训练产生embedding,inputCol需要是 array（string）类型
    训练好后写入 item2vecEmb.txt
    :param dataset:
    :return:
    '''
    word2vec = Word2Vec(vectorSize=10,windowSize=5,maxIter=10,inputCol='movieIds')
    model = word2vec.fit(dataset)
    print('model fitted')
    synonyms = model.findSynonymsArray('158',20)
    for moveid,similarity in synonyms:
        print('{}:{}'.format(moveid,similarity))

    with open('./modeldata/item2vecEmb.txt','w') as f:
        for row in model.getVectors().collect():
            f.write('{}:{}\n'.format(row['word'],row['vector']))


if __name__ == '__main__':
    spark = SparkSession.builder.appName('enbbeding').master('local[*]').getOrCreate()
    dataset=processItemSequence(spark)
    trainItem2vec(dataset)
