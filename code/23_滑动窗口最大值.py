'''
给定一个数组 nums 和滑动窗口的大小 k，请找出所有滑动窗口里的最大值。
示例:
输入: nums = [1,3,-1,-3,5,3,6,7], 和 k = 3
输出: [3,3,5,5,6,7]

链接：https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof
'''
from typing import *
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    '''
    法1
    :param nums:
    :param k:
    :return:
    '''
    n = len(nums)
    if k > n  or n == 0:
        return []
    max_list=[]
    new_n=n + 1 - k
    for i in range(new_n):
        max_list.append(max(nums[i:i+k]))
    return max_list

def maxSlidingWindow2(nums: List[int], k: int) -> List[int]:
    '''
    法二
    :param nums:
    :param k:
    :return:
    '''
    n = len(nums)
    if k > n or n == 0:
        return []
    if k == 1:
        return nums
    max_list = []
    tmp_best=max(nums[:k])
    max_list.append(tmp_best)
    for i in range(k,n):
        if nums[i] > tmp_best :
            tmp_best = nums[i]
            max_list.append(tmp_best)
        else:
            if tmp_best == nums[i-k]:
                tmp_best=max(nums[i-k+1:i+1])
            max_list.append(tmp_best)
    return max_list

def maxSlidingWindow3(nums: List[int], k: int) -> List[int]:
    '''
    法三
    :param nums:
    :param k:
    :return:
    '''
    from collections import deque
    # deque 是一个单调递减的队列，队首元素始终是当前窗口的最大值
    if not nums or k == 0: return []
    deque = deque()
    res = []
    n = len(nums)
    # 窗口未形成前
    for i in range(k):
        while deque and nums[i] >= deque[-1]:
            deque.pop()
        deque.append(nums[i])
    res.append(deque[0])

    # 窗口形成后
    for i in range(k,n):
        if deque[0] == nums[i-k]:
            deque.popleft()
        while deque and nums[i] >= deque[-1]:
            deque.pop()
        deque.append(nums[i])
        res.append(deque[0])
    return res






if __name__ == '__main__':
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(maxSlidingWindow(nums,k))
    print(maxSlidingWindow2(nums, k))
    print(maxSlidingWindow3(nums,k))





