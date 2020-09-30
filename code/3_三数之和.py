'''
给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/3sum
'''
from typing import *
def threeSum(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    res = []
    if not nums or n<3:
        return []
    # 进行排序
    nums.sort()

    for i in range(n):
        if nums[i] > 0:
            return res
        # 过滤重复元素
        # if i > 0  and nums[i] == nums[i-1]:
        #     continue
        left = i+1
        right = n-1
        while left < right:
            if (nums[i] + nums[left] + nums[right]) == 0:
                res.append((nums[i],nums[left],nums[right]))
                # 过滤重复元素
                # while left < right and nums[left] == nums[left+1]:
                #     left +=1
                # while left < right and nums[right] == nums[right-1]:
                #     right-=1
                left +=1
                right -=1
            elif (nums[i] + nums[left] + nums[right])>0:
                right -=1
            else:
                left+=1
    return res

if __name__ == '__main__':

    print(set(threeSum([-1,0,1,2,-1,-4])))
    print(threeSum([0,0,0]))




