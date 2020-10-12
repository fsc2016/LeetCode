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
def coinChange( coins: List[int], amount: int) -> int:
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

if __name__ == '__main__':
    coins = [1,3,5]
    amount = 0
    print(coinChange(coins,amount))
