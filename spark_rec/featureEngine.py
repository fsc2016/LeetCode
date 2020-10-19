import pyspark
from pyspark.sql import *
from pyspark.sql.types import  IntegerType
from pyspark.ml.feature import OneHotEncoderEstimator,OneHotEncoder
from pyspark.ml import *


def oneHotEncoderExample(df):
    oneHotEncoder=OneHotEncoderEstimator().setInputCols('movieIdNumber').setOutputCols('movieIdVector').setDropLast(False)
    # oneHotEncoder = Pi
    # pip = Pipeline().setStages()
    tmp=oneHotEncoder.fit()



if __name__ == '__main__':


    spark = SparkSession.builder.appName('learn_ml').master('local[1]').getOrCreate()
    # df=spark.read.format('csv').option("header", "true").load('./data/movies.csv')
    df = spark.read.csv( path='./data/movies.csv',inferSchema=True,header=True)
    # df=df.withColumn('movieIdNumber',df.movieId.cast(IntegerType()))
    df.printSchema()
    df.show(5)