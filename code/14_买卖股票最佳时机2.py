'''
之前对交易次数限制是 1次和任意多次
这次是限制最多交易俩次，求出最大利润

示例 1:
输入: [3,3,5,0,0,3,1,4]
输出: 6
解释: 在第 4 天（股票价格 = 0）的时候买入，在第 6 天（股票价格 = 3）的时候卖出，这笔交易所能获得利润 = 3-0 = 3 。
     随后，在第 7 天（股票价格 = 1）的时候买入，在第 8 天 （股票价格 = 4）的时候卖出，这笔交易所能获得利润 = 4-1 = 3 。
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-iii

'''
from typing import *
def maxProfit(prices: List[int]) -> int:
    '''
    采用波峰波谷法，可以解决任意交易次数
    :param prices:
    :return:
    '''
    cost1 ,cost2= float('inf'),float('inf')
    profit1,profit2=0,0
    for p in prices:
        cost1 = min(cost1,p)
        profit1 = max(profit1,p - cost1)
        cost2 = min(cost2,p - profit1) #第二次的成本,叠加了第一次的收益，并不是第二次购买股票的价格
        profit2 = max(profit2,p - cost2)  #第二次收益就是总收益
    return profit2

def maxProfit2(prices: List[int]) -> int:
    n = len(prices)
    dp = [[0] * 5 for i in range(n)]
    #初始化第一轮
    dp[0][1] = -prices[0] #第一次购买成本
    dp[0][2] = 0   #第一次收益
    dp[0][3] =  -prices[0] #第二次成本，叠加了第一次收益
    dp[0][4] = 0 #第二次收益=总收益
    for i in range(1,n):
        dp[i][1] = max(dp[i-1][1],dp[i-1][0] - prices[i])
        dp[i][2] = max(dp[i-1][2],dp[i-1][1] + prices[i])
        dp[i][3] = max(dp[i-1][3],dp[i-1][2] - prices[i])
        dp[i][4] = max(dp[i-1][4],dp[i-1][3] + prices[i])
    for i in dp:
        print(i)
    # print(dp)
    return dp[n-1][4]


if __name__ == '__main__':
    l = [3,3,5,0,0,3,1,4]
    l=[1,2,4,2,5,7,2,4,9,0]
    print(maxProfit2(l))

