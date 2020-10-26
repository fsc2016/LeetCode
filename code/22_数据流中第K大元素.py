'''
设计一个找到数据流中第K大元素的类（class）。注意是排序后的第K大元素，不是第K个不同的元素。
你的 KthLargest 类需要一个同时接收整数 k 和整数数组nums 的构造器，它包含数据流中的初始元素。每次调用 KthLargest.add，返回当前数据流中第K大的元素。

示例:
int k = 3;
int[] arr = [4,5,8,2];
KthLargest kthLargest = new KthLargest(3, arr);
kthLargest.add(3);   // returns 4
kthLargest.add(5);   // returns 5
kthLargest.add(10);  // returns 5
kthLargest.add(9);   // returns 8
kthLargest.add(4);   // returns 8

链接：https://leetcode-cn.com/problems/kth-largest-element-in-a-stream
'''
from typing import *
from heapq import *
import heapq
class KthLargest:
    '''
    数组法
    # '''
    # def __init__(self, k: int, nums: List[int]):
    #     self._nums = nums
    #     self._k = k
    #
    # def add(self, val: int) -> int:
    #     self._nums.append(val)
    #     self._nums.sort()
    #     return self._nums[-self._k]

    '''
    堆
    '''
    def __init__(self, k: int, nums: List[int]):
        self._nums = nums
        heapq.heapify(self._nums)
        self._k = k
        while len(self._nums) > k:
            heapq.heappop(self._nums)

    def add(self, val: int) -> int:
        heapq.heappush(self._nums,val)
        if len(self._nums) > self._k:
            heapq.heappop(self._nums)
        return self._nums[0]


    # def __init__(self, k, nums):
    #     """
    #     :type k: int
    #     :type nums: List[int]
    #     """
    #     self.k = k
    #     self.nums = nums
    #     heapify(self.nums)
    #     while len(self.nums) > self.k:  # cut heap to size:k
    #         heappop(self.nums)
    #
    # def add(self, val):
    #     """
    #     :type val: int
    #     :rtype: int
    #     """
    #     if len(self.nums) < self.k:
    #         heappush(self.nums, val)
    #         heapify(self.nums)  # cation
    #     else:
    #         top = float('-inf')
    #         if len(self.nums) > 0:
    #             top = self.nums[0]
    #         if top < val:
    #             heapreplace(self.nums, val)
    #     return self.nums[0]


if __name__ == '__main__':
    arr=[4,5,8,2]
    kth = KthLargest(3,arr)
    print(kth.add(3))
    print(kth.add(5))
    print(kth.add(10))