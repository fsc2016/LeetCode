'''
给你一个整数数组 nums ，请你找出数组中乘积最大的连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。
示例 1:
输入: [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
链接：https://leetcode-cn.com/problems/maximum-product-subarray
'''
from typing import *
def maxProduct(nums:List)-> int:
    '''
    动态规划法
    遍历数组时计算当前最大值，不断更新
    令imax为当前最大值，则当前最大值为 imax = max(imax * nums[i], nums[i])
    由于存在负数，那么会导致最大的变最小的，最小的变最大的。因此还需要维护当前最小值imin，imin = min(imin * nums[i], nums[i])
    :param nums:
    :return:
    '''
    n = len(nums)
    maxnum ,minnum,ans,ans_min= nums[0],nums[0],nums[0],nums[0]
    for i in range(1,n):
        tmp_max,tmp_min = maxnum,minnum
        maxnum = max(tmp_max*nums[i],tmp_min*nums[i],nums[i])
        minnum = min(tmp_max * nums[i], tmp_min * nums[i], nums[i])
        ans = max(ans,maxnum)
        ans_min = min(ans_min,minnum)
    return ans,ans_min

def maxProduct_rv1(nums:List)-> int:
    n = len(nums)
    tmp_min,tmp_max,best = nums[0],nums[0],nums[0]
    for i in range(1,n):
        tmp_max = max(nums[i],tmp_max*nums[i],tmp_min*nums[i])
        tmp_min = min(nums[i],tmp_min*nums[i],tmp_max*nums[i])
        best = max(tmp_max,best)
    return best

def maxProduct2(self, nums: List[int]) -> int:
    '''
    穷举法
    :param self:
    :param nums:
    :return:
    '''
    n = len(nums)
    maxnum = nums[0]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                maxnum = max(nums[i], maxnum)
                num = nums[i]
            else:
                num *= nums[j]
                maxnum = max(num, maxnum)
    return maxnum

if __name__ == '__main__':
    l=[2,3,-2,4]
    # l= [-2,0,-1]
    print(maxProduct_rv1(l))