'''
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
示例:
输入: [-2,1,-3,4,-1,2,1,-5,4]
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
'''
from typing import *
def maxSubArray(nums: List[int]) -> int:
    '''
    动态规划
    :param nums:
    :return:
    '''
    # n = len(nums)
    # dp = [float('-inf')] * n
    # dp[0] = nums[0]
    # for i in range(1,n):
    #     dp[i] = max(dp[i-1]+nums[i],nums[i])
    # return max(dp)

    # 优化空间复杂度
    n = len(nums)
    pre_num = nums[0]
    best_num = nums[0]
    for i in range(1, n):
        pre_num = max(pre_num + nums[i], nums[i])
        best_num = max(best_num,pre_num)

    return best_num

if __name__ == '__main__':
    l =[-2,1,-3,4,-1,2,1,-5,4]
    print(maxSubArray(l))
