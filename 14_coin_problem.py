from typing import *
import sys
sys.setrecursionlimit(100000)
'''
有3个硬币，1,3,5 。问给定的总额，最低需要多少个硬币数凑齐总额
'''
def coin_solu(money:int)->int:
    '''
    回溯解决
    :param money:
    :return:
    '''
    count = 0
    tables =[0] * money
    def min_coin(remain):
        global count
        if remain == 1 :return 1
        if remain == 2 :return 2
        if remain == 3 :return 1
        if remain == 4 :return 2
        if remain == 5 :return 1
        # if remain <= 0 :return
        count = 1 + min(min_coin(remain-5),min_coin(remain-3),min_coin(remain-1))
        # 打印重复的子问题
        # print(remain,count)
        return count
    return min_coin(money)


def coin_solu2(money:int)->int:
    '''
    递归加备忘录
    :param money:
    :return:
    '''
    count = 0
    tables =[0] * money
    def min_coin(remain):
        global count
        if remain == 1 :return 1
        if remain == 2 :return 2
        if remain == 3 :return 1
        if remain == 4 :return 2
        if remain == 5 :return 1
        # 加入备忘录
        if tables[remain-1]:
            return tables[remain-1]
        # if remain <= 0 :return
        # 动态转移方程
        count = 1 + min(min_coin(remain-5),min_coin(remain-3),min_coin(remain-1))
        # print(remain,count)
        # 从备忘录中提取
        tables[remain-1] = count
        return count
    return min_coin(money)

if __name__ == '__main__':
    # print(coin_solu(10))
    import time
    st=time.time()
    print(coin_solu(42))
    print(time.time()-st)