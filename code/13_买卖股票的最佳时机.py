'''
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
如果你最多只允许完成一笔交易（即买入和卖出一支股票一次），设计一个算法来计算你所能获取的最大利润。
注意：你不能在买入股票前卖出股票。
示例 1:
输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。

示例 2:
输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock
'''
from typing import *
def maxProfit(prices: List[int]) -> int:
    # max_income = 0
    # n = len(prices)
    # for i in range(1,n):
    #     tmp = prices[i]-min(prices[:i])
    #     max_income = max(tmp,max_income)
    # return max_income

    # 改进版,执行时间提升了100倍
    max_income = 0
    min_price = float('inf')
    n = len(prices)
    for i in range(1, n):
        min_price = min(min_price, prices[i - 1])
        tmp = prices[i] - min_price
        max_income = max(tmp, max_income)
    return max_income

'''
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

示例 1:
输入: [7,1,5,3,6,4]
输出: 7
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
     随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6-3 = 3 。
链接：https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii
'''
def maxProfit2(prices: List[int]) -> int:
    '''
    有收益全部加起来
    :param prices:
    :return:
    '''
    # max_income = 0
    # n = len(prices)
    # for i in range(1,n):
    #     if prices[i] > prices[i-1]:
    #         max_income+=prices[i] - prices[i-1]
    # return max_income

    '''
    峰谷法,优先找到每一次谷到峰的段，累加起来。
    '''
    max_income = 0
    n = len(prices)
    i =0
    while(i < n-1):
        # 找波谷
        while i < n-1 and prices[i] >= prices[i+1]:
            i+=1
        valley = prices[i]
        #波峰
        while i < n-1 and prices[i] < prices[i+1] :
            i+=1
        peak = prices[i]
        max_income += peak - valley
    return max_income

def maxProfit3(prices: List[int]) -> int:
    '''
    动态规划法。主要是采用动态转移表。分成俩个状态
    :param prices:
    // 0：持有现金
    // 1：持有股票
    // 状态转移：0 → 1 → 0 → 1 → 0 → 1 → 0
    '''

    n = len(prices)
    dp = [[0] *2 for i in range(n)]
    dp[0][0] = 0
    dp[0][1] = -prices[0] #买入股票为负值。
    for i in range(1,n):
        dp[i][0] = max(dp[i-1][0],dp[i-1][1] + prices[i]) #当前阶段是否卖出股票
        dp[i][1] = max(dp[i-1][1],dp[i-1][0] - prices[i]) #当前阶段是否买入最低值股票
    return dp[n-1][0]

if __name__ == '__main__':
    prices=[7,1,5,3,6,4]
    # prices=[7,6,4,3,1]
    print(maxProfit3(prices))
