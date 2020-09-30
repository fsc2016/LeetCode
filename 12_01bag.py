from typing import *
def bag(items:List[int],w:int):
    '''
    :param items: 物品列表
    :param w: 总重量
    :return:
    '''
    n = len(items)
    states=[[-1]*(w+1) for i in range(n)] #二维数组
    states[0][0]=1
    if items[0]<=w:
        states[0][items[0]] = 1

    for i in range(1,n):
        for j in range(0,w+1):
            if states[i-1][j] == 1:
                states[i][j] = 1  #不加

        for j in range(0,(w - items[i])+1): # 遍历除了背包减去第i个商品的重量，相当于筛选条件
            if states[i-1][j] ==1:
                states[i][j+items[i]] = 1  #加入

    for j in range(0,w+1)[::-1]:
        if states[n-1][j] == 1:
            return j


def bag_with_max_value(weights:List[int],values:List[int],w,n):
    '''
    :param weights: 商品重量集合
    :param values: 商品价值集合
    :param w: 背包总重量
    :param n: 商品总数量
    :return:
    '''
    states = [[-1]*(w+1) for i in range(n)]
    # 特殊处理第一行
    states[0][0] =0
    if weights[0] <= w:
        states[0][weights[0]]=values[0]

    for i in range(1,n):
        for j in range(w+1):
            if states[i-1][j]>=0:
                states[i][j] = states[i-1][j]

        for j in range(w - weights[i]+1):
            if states[i-1][j] >= 0:
                maxv = states[i-1][j] + values[i]
                if maxv > states[i][j+weights[i]]: #保留每个状态下最大的那个价值
                    states[i][j + weights[i]] = maxv

    tmpMax=0
    for j in range(w+1):
        if states[n-1][j] > tmpMax:
            tmpMax = states[n-1][j]
    return tmpMax


if __name__ == '__main__':
    items_info = [2, 2, 4, 6, 3]
    values_info=[3,4,8,9,6]
    capacity = 9
    print(bag(items_info, capacity))

    print(bag_with_max_value(items_info,values_info,capacity,5))


