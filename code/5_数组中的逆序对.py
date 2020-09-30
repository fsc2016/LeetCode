'''
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。输入一个数组，求出这个数组中的逆序对的总数。
示例 1:
输入: [7,5,6,4]
输出: 5
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof
'''
from typing import *
class Solution:
    # 使用暴力枚举。不好
    def reversePairs(self, nums: List[int]) -> int:
        tmp=0
        for n,i in enumerate(nums):
            for j in nums[n+1:]:
                if i > j:
                    tmp+=1
        return tmp

    # 使用归并排序算法 来解决
    times=0
    def reversePairs2( self,nums: List[int]) -> int:
        high=len(nums)-1
        self._merge_sort(nums,0,high)
        return self.times


    def _merge_sort(self,nums,low,high):
        if low < high:
            mid = low + (high - low)//2
            self._merge_sort(nums,low,mid)
            self._merge_sort(nums,mid+1,high)
            self.merge(nums,low,mid,high)

    def merge(self,nums,low,mid,high):
        tmp =[]
        i ,j = low,mid+1
        while i<=mid and j <=high:
            if nums[i] <= nums[j]:
                tmp.append(nums[i])
                i+=1
            else:
                tmp.append(nums[j])
                j+=1
                self.times=self.times+(mid-i+1)
        start =i if i <= mid else j
        end = mid if i<= mid else high
        tmp.extend(nums[start:end+1])
        nums[low:high+1] = tmp

        # 下面这种写法 超出时间限制。挨个添加不如一次性extend
        # while i<=mid:tmp.append(nums[i])
        # while j <= high: tmp.append(nums[j])
        # nums[low:high + 1] = tmp

if __name__ == '__main__':
    solu = Solution()
    nums=[7,5,6,4]
    # print(solu.reversePairs(nums))
    print(solu.reversePairs2(nums))

