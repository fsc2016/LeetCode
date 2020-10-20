'''
给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

示例:
给定 nums = [2, 7, 11, 15], target = 9
因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]

链接：https://leetcode-cn.com/problems/two-sum
'''
from typing import *

def twoSum(nums: List[int], target: int) -> List[int]:
    '''
    暴力枚举
    :param nums:
    :param target:
    :return:
    '''
    n = len(nums)
    for i in range(n):
        for j in range(i+1,n):
            if nums[i] + nums[j] == target:
                return [i,j]

def twoSum2(nums: List[int], target: int) -> List[int]:
    '''
    哈希表法
    :param nums:
    :param target:
    :return:
    '''
    hash_kv = {}
    for i,num in enumerate(nums):
        tmp = target - num
        if tmp in hash_kv.keys():
            return [i,hash_kv.get(tmp)]
        hash_kv[num] = i


if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    nums = [3,2,4]
    target = 6
    print(twoSum(nums,target))
    print(twoSum2(nums,target))
