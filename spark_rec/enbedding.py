import findspark
findspark.init()
from typing import *
from pyspark.sql import *
from pyspark.sql.types import  IntegerType,ArrayType,StringType
from pyspark.ml.feature import Word2Vec,Word2VecModel
from pyspark.sql.functions import *
import os,random
from pyspark.ml.linalg import Vectors
from collections import defaultdict
import redis
from pyspark.ml.recommendation import ALS,ALSModel

from pyspark.ml.feature import BucketedRandomProjectionLSH

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
    moviesCount = dataset.select(explode(col('movieIds'))).alias('tmp').distinct().count()
    print('unique high rating movies:{}'.format(moviesCount))
    # print(dataset.count())
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
        r = redis.Redis(connection_pool=pool)
        for i,row in enumerate(model.getVectors().collect()):
            tmp = ','.join([str(vector) for vector in row['vector']])
            if i == 1:
                print(type(row['vector']))
            r.set('{}:{}'.format(redisKeyPrefix,row['word']),tmp,ex)
    return  model

def embeddingLSH(moviesEmb:DataFrame):
    '''
    局部敏感哈希
    :param spark:
    :param moviesEmb:
    :return:
    '''
    brp = BucketedRandomProjectionLSH(inputCol='vector',outputCol='bucketId',numHashTables=3,bucketLength=0.1)
    model = brp.fit(moviesEmb)
    moviesEmbResult = model.transform(moviesEmb)
    moviesEmbResult.printSchema()
    moviesEmbResult.show(5)
    print("Approximately searching for 5 nearest neighbors of the sample embedding:")
    sampleEmb = Vectors.dense([0.795,0.583,1.120,0.850,0.174,-0.839,-0.0633,0.249,0.673,-0.237])
    model.approxNearestNeighbors(moviesEmb,sampleEmb,5).show(5)



def dealPairMovie(movies:Row)->List:
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
        randomProb = random.random()
        for k, prob in transitionMatrix[curItem].items():
            if randomProb >= prob:
                curItem = k
                break

        sample.append(curItem)
    return sample

def randomWalk(transitionMatrix,itemDistribution,sampleCount,sampleLength):
    '''
    随机游走
    :param transitionMatrix:
    :param itemDistribution:
    :param sampleCount:
    :param sampleLength:
    :return:
    '''
    samples = []
    for i in range(sampleCount):
        samples.append(oneRandomWalk(transitionMatrix, itemDistribution, sampleLength))
    return samples

def oneNode2vec(transitionMatrix, itemDistribution, sampleLength):

    p , q  = 0.1, 0.2
    sample = []
    randomValue = random.random()
    firstItem = ''
    accumulateProb = 0

    # 按照电影分布，取第一部电影
    for k, v in itemDistribution.items():
        accumulateProb += v
        if accumulateProb >= randomValue:
            firstItem = k
            break

    sample.append(firstItem)
    curItem = firstItem
    #nodeT始终是curElement的前一个值
    nodeT = curItem
    # 按照状态转移，取后面9部电影
    for i in range(1, sampleLength):
        if not transitionMatrix[curItem] or not itemDistribution[curItem]:
            break
        randomProb = random.random()
        # 第一步时，curItem和nodeT是同一个点，所以要保持nodeT不动，curIte前进一步
        if i == 1:
            for item, prob in transitionMatrix[curItem].items():
                if randomProb >= prob:
                    curItem = item
                    break
        else:
            for item, prob in transitionMatrix[curItem].items():
                # 跳回前一节点
                if item == nodeT:
                    prob = prob * 1 / p
                #distince =1
                elif item in transitionMatrix[nodeT]:
                    prob = prob
                #distince =2
                else:
                    prob = prob * 1/q

                if randomProb >= prob:
                    nodeT = curItem
                    curItem = item
                    break
        sample.append(curItem)

    return sample


def node2vec(transitionMatrix,itemDistribution,sampleCount,sampleLength):
    samples = []
    for i in range(sampleCount):
        samples.append(oneNode2vec(transitionMatrix, itemDistribution, sampleLength))
    return samples

def graphEmb(dataset:DataFrame,spark:SparkSession,embOutputFilename,saveToRedis=False,redisKeyPrefix=None):
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

    # newSamples=randomWalk(transitionMatrix, itemDistribution, sampleCount, sampleLength)
    newSamples = node2vec(transitionMatrix, itemDistribution, sampleCount, sampleLength)

    # 转为rdd
    rddSamples=spark.sparkContext.parallelize([Row(movieIds=i) for i in newSamples])
    print(newSamples[:10])
    print(rddSamples.take(10))

    # 转为DataFrame
    dataFrameSamples = spark.createDataFrame(rddSamples)
    print(type(dataFrameSamples))
    print(dataFrameSamples.take(10))
    # trainItem2vec(dataFrameSamples,embOutputFilename,saveToRedis,redisKeyPrefix)

def dealUserEmb(movieids:List):
    useremb=[0] * 10
    for movieid in movieids:
        movEmb = movdict.get(movieid)
        if movEmb:
            useremb=[useremb[i]+movEmb[i] for i in range(10)]
    return ','.join([str(ue) for ue in useremb])

def generateUserEmb(spark:SparkSession,model:Word2VecModel,embOutputFilename,saveToRedis=False,redisKeyPrefix=None):
    '''
    用户embbing
    :param spark:
    :param model:
    :param embOutputFilename:
    :param saveToRedis:
    :param redisKeyPrefix:
    :return:
    '''
    df = spark.read.format('csv').option('header', 'true').load('./data/ratings.csv')

    due = udf(f=dealUserEmb, returnType=StringType())
    um = df.groupBy('userId').agg(collect_list(col('movieId')).alias('movieIds')).withColumn('userEmb', due(col('movieIds')))
    ueEmb = um.select('userId','userEmb').collect()

    if saveToRedis:
        pool = redis.ConnectionPool(host=HOST,port=PORT)
        # key的存活时间 秒
        ex = 60 * 10
        r = redis.Redis(connection_pool=pool)
        for row in ueEmb:
            r.set('{}:{}'.format(redisKeyPrefix,row['userId']),row['userEmb'],ex)


def testALS(spark:SparkSession,saveToRedis = False,redisUserPrefix= "uEmb",redisItemPrefix='i2vEmb'):
    df = spark.read.format('csv').option('header','true').load('./data/ratings.csv')
    newdf = df.select(['userId','movieId','rating'])
    newdf.printSchema()
    newdf=newdf.withColumn('userId',newdf.userId.astype('int')).withColumn('movieId',newdf.movieId.astype('int')).withColumn('rating',newdf.rating.astype('float'))
    newdf.printSchema()
    als = ALS(maxIter=10,regParam=0.1,userCol='userId',itemCol='movieId',ratingCol='rating')
    model = als.fit(newdf)
    print(model.itemFactors.take(2))
    if saveToRedis:
        pool = redis.ConnectionPool(host=HOST,port=PORT)
        # key的存活时间 秒
        ex = 60 * 60
        r = redis.Redis(connection_pool=pool)
        for row in model.itemFactors.collect():
            tmp =[str(i) for i in row['features']]
            r.set('{}:{}'.format(redisItemPrefix, row['id']), ' '.join(tmp), ex)





    # test code
    # users = newdf.select('userId').distinct().count()
    # movers = newdf.select('movieId').distinct().count()
    # print('length user:{} length movie:{}'.format(users,movers))
    # print(model.userFactors.count())
    # print(model.itemFactors.count())
    # print(model.recommendForUserSubset(newdf.where(newdf.userId==10),2).collect())
    # print(model.recommendForItemSubset(newdf.where(newdf.movieId == 2), 2).collect())


if __name__ == '__main__':
    spark = SparkSession.builder.appName('enbbeding').master('local[*]').getOrCreate()
    # dataset=processItemSequence(spark)
    # print(type(dataset))
    # model = trainItem2vec(dataset,'item2vecEmb1.txt',saveToRedis=False,redisKeyPrefix='i2vEmb')
    # embeddingLSH(model.getVectors())
    # graphEmb(dataset,spark,'item2graphVecEmb.txt',saveToRedis=True,redisKeyPrefix='graphEmb')
    # 构造itememb dict
    # rows = model.getVectors().collect()
    # movdict = {}
    # for row in rows:
    #     movdict[row['word']] = list(row['vector'])
    # generateUserEmb(spark,model,'userEmb.csv',saveToRedis = True,redisKeyPrefix= "uEmb")

    testALS(spark,saveToRedis = True,redisUserPrefix= "uEmb",redisItemPrefix='i2vEmb')

