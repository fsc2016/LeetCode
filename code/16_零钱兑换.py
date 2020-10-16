'''
给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。
你可以认为每种硬币的数量是无限的。
示例 1：
输入：coins = [1, 2, 5], amount = 11
输出：3
解释：11 = 5 + 5 + 1

示例 2：
输入：coins = [2], amount = 3
输出：-1
链接：https://leetcode-cn.com/problems/coin-change
'''
from typing import *
def coinChange(coins:List[int], amount: int) -> int:
    if amount == 0:
        return -1
    dp = [0] * amount
    def dp_recu(remain):
        if remain in coins:
            return 1
        if remain < 0:
            return float('inf')
        if dp[remain-1]:
            return dp[remain-1]

        count = 1+ min([dp_recu(remain-i) for i in coins])
        dp[remain-1] = count
        return count

    value=dp_recu(amount)
    if value == float('inf'):
        value=-1
    return value

def coinChange_rv1( coins: List[int], amount: int) -> int:
    if amount == 0:
        return -1
    dp = [0] * amount
    def recu_coin(remain):
        if remain in coins:
            return 1
        if remain < 0:
            return float('inf')
        if dp[remain-1]:
            return dp[remain-1]

        count = 1+ min([recu_coin(remain-i) for i in coins])
        dp[remain-1] = count
        return count
    result = recu_coin(amount)
    return result

# 法2
def coinChange2( coins: List[int], amount: int) -> int:
    '''
    自下而上的动态规划
    :param coins:
    :param amount:
    :return:
    '''
    dp =[float('inf')] * (amount+1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin,amount+1):
            dp[x] = min(dp[x],dp[x-coin]+1)

    return dp[amount] if dp[amount] != float('inf') else -1

def coinChange2_rv1( coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount+1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin,amount+1):
            dp[i] = min(dp[i],dp[i-coin]+1)
    return dp[amount]

'''
给定不同面额的硬币和一个总金额。写出函数来计算可以凑成总金额的硬币组合数。假设每一种面额的硬币有无限个。 
示例 1:
输入: amount = 5, coins = [1, 2, 5]
输出: 4
解释: 有四种方式可以凑成总金额:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
链接：https://leetcode-cn.com/problems/coin-change-2
'''
def change( coins: List[int], amount: int) -> int:
    dp = [0] * (amount+1)
    dp[0] = 1
    for coin in coins:
        for x in range(coin,amount+1):
            dp[x] =dp[x] + dp[x - coin] #先从只有一种硬币考虑，总是等于前一差额+上当前值（默认当前值为0）
    return dp[amount]


if __name__ == '__main__':
    coins = [1,2,5]
    amount = 11
    # print(coinChange2(coins,amount))

    print(coinChange(coins,amount))
    print(coinChange_rv1(coins,amount))
    print(coinChange2_rv1(coins,amount))