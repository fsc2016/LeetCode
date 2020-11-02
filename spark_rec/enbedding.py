import findspark
findspark.init()
from typing import *
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType,StringType
from pyspark.ml.feature import Word2Vec
from pyspark.sql.functions import *
import os,random
from collections import defaultdict
import redis

HOST ='localhost'
PORT = 6379
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
    userSeq.show(5)

    #不使用udf，速度慢一点
    # userSeq=df.where(df['rating'] >= 3.5).sort('timestamp').groupby('userId').agg(collect_list('movieId').alias('movieIds')).withColumn('movieIdStr',array_join('movieIds',' ')).show(10)

    userSeq.printSchema()
    dataset = userSeq.select('movieIds')
    print(dataset.count())
    return dataset

def trainItem2vec(dataset,filename,saveToRedis=False,redisKeyPrefix=None):
    '''
    训练产生embedding,inputCol需要是 array（string）类型
    训练好后写入 filename
    :param dataset:
    :return:
    '''
    word2vec = Word2Vec(vectorSize=10,windowSize=5,maxIter=10,inputCol='movieIds')
    model = word2vec.fit(dataset)
    print('model fitted')
    # 打印相似电影，基于点积运算
    synonyms = model.findSynonymsArray('158',20)
    for moveid,similarity in synonyms:
        print('{}:{}'.format(moveid,similarity))

    with open('./modeldata/{}'.format(filename),'w') as f:
        for row in model.getVectors().collect():
            tmp=','.join([str(vector) for vector in row['vector']])
            f.write('{}:{}\n'.format(row['word'],tmp))

    # redis-cli eval "redis.call('del', unpack(redis.call('keys','*')))" 0 windows批量删除key
    if saveToRedis:
        pool = redis.ConnectionPool(host=HOST,port=PORT)
        # key的存活时间 秒
        ex = 60 * 10
        # r = redis.Redis(host=HOST,port=PORT)
        r = redis.Redis(connection_pool=pool)
        for i,row in enumerate(model.getVectors().collect()):
            tmp = ','.join([str(vector) for vector in row['vector']])
            if i == 1:
                print(type(row['vector']))
            r.set('{}:{}'.format(redisKeyPrefix,row['word']),tmp,ex)


def dealPairMovie(movies:Row)->List:
    '''
    udf
    :param movies:
    :return:
    '''
    newl=[]
    movies = movies['movieIds']
    for i in range(len(movies)-1):
        newl.append((movies[i],movies[i+1]))
    return newl


def generateTransitionMatrix(dataset:DataFrame):
    '''
    生成状态转移矩阵
    :param dataset:
    :return:
    '''
    pairSamples=dataset.rdd.flatMap(dealPairMovie)
    pairSamples.cache()
    print(pairSamples.take(10))
    print('pairSamples over')
    # {(mid,mid2):count,...}

    pairCountMap = pairSamples.countByValue()

    print('pairCountMap_{}'.format(len(pairCountMap)))
    # 计数状态矩阵
    transitionCountMatrix = defaultdict(dict)
    itemCountMap = defaultdict(int)
    all_count=0
    for k,count in pairCountMap.items():
        transitionCountMatrix[k[0]][k[1]] = count
        itemCountMap[k[0]] +=count
        all_count+=count
    print('transitionCountMatrix over')
    #概率状态矩阵
    transitionMatrix = defaultdict(dict)
    itemDistribution = defaultdict(int)
    for a,cmap in transitionCountMatrix.items():
        for b,count in cmap.items():
            transitionMatrix[a][b] = float(count /itemCountMap[a])

    for k,count in itemCountMap.items():
        itemDistribution[k] = float(count / all_count)

    print('transitionMatrix_{}'.format(len(transitionMatrix)))
    print(transitionMatrix['858'])
    print('itemDistribution_{}'.format(len(itemDistribution)))
    print(itemDistribution['858'])
    return transitionMatrix,itemDistribution

def oneRandomWalk(transitionMatrix, itemDistribution, sampleLength):
    '''
    单次随机游走
    :param transitionMatrix:
    :param itemDistribution:
    :param sampleLength:
    :return:
    '''
    sample = []
    randomValue = random.random()
    firstItem=''
    accumulateProb=0

    # 按照电影分布，取第一部电影
    for k,v in itemDistribution.items():
        accumulateProb+=v
        if accumulateProb >= randomValue:
            firstItem=k
            break
    sample.append(firstItem)
    curItem = firstItem

    # 按照状态转移，取后面9部电影
    for i in range(1,sampleLength):
        if not transitionMatrix[curItem] or not itemDistribution[curItem]:
            break
        # 随机游走的策略
        curProb = itemDistribution[curItem]
        prob = random.random()
        accumulateProb=0
        for k,v in transitionMatrix[curItem].items():
            accumulateProb += v
            if accumulateProb >= prob*curProb:
                curItem = k
                break

        sample.append(curItem)
    return sample



def randomWalk(transitionMatrix,itemDistribution,sampleCount,sampleLength):
    samples = []
    for i in range(sampleCount):
        samples.append(oneRandomWalk(transitionMatrix, itemDistribution, sampleLength))
    return samples

def graphEmb(dataset:DataFrame,spark:SparkSession,embOutputFilename):
    '''
    图enbding
    :param dataset:
    :param spark:
    :param embOutputFilename:
    :return:
    '''
    transitionMatrix, itemDistribution=generateTransitionMatrix(dataset)
    sampleCount = 20000
    sampleLength = 10

    newSamples=randomWalk(transitionMatrix, itemDistribution, sampleCount, sampleLength)
    # 转为rdd
    rddSamples=spark.sparkContext.parallelize([Row(movieIds=i) for i in newSamples])
    print(newSamples[:10])
    print(rddSamples.take(10))
    # 转为DataFrame
    dataFrameSamples = spark.createDataFrame(rddSamples)
    print(type(dataFrameSamples))
    print(dataFrameSamples.take(10))
    # trainItem2vec(dataFrameSamples,embOutputFilename)



if __name__ == '__main__':
    spark = SparkSession.builder.appName('enbbeding').master('local[*]').getOrCreate()
    dataset=processItemSequence(spark)
    print(type(dataset))
    trainItem2vec(dataset,'item2vecEmb1.txt',saveToRedis=True,redisKeyPrefix='i2vEmb')
    # graphEmb(dataset,spark,'item2graphVecEmb.txt')


