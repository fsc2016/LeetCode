'''
给定一个无序的整数数组，找到其中最长上升子序列的长度。
示例:
输入: [10,9,2,5,3,7,101,18]
输出: 4
解释: 最长的上升子序列是 [2,3,7,101]，它的长度是 4。
链接：https://leetcode-cn.com/problems/longest-increasing-subsequence
'''
from typing import *
def lengthOfLIS(nums: List[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(1,n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i],dp[j]+1)
    # print(dp)
    return max(dp)

if __name__ == '__main__':
    l=[10, 9, 2, 5, 3, 7, 101, 18]
    print(lengthOfLIS(l))