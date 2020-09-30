'''
在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

示例 1:
输入: [3,2,1,5,6,4] 和 k = 2
输出: 5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/kth-largest-element-in-an-array
'''
#方法一，直接调用类库方法进行排序
from typing import *
def findKthLargest(nums: List[int], k: int) -> int:
    nums.sort(reverse=True)
    return nums[k-1]

#方法二 使用归并排序进行排序
def _merge_sort_first(l):
    high = len(l)-1
    _merge_sort(l,0,high)

def _merge_sort(l,low,high):
    if low < high:
        mid = low + (high-low)//2
        # 递归
        _merge_sort(l,low,mid)
        _merge_sort(l,mid+1,high)

        merge(l,low,mid,high)

def merge(l,low,mid,high):
    tmp = []
    i = low
    j = mid+1
    while i <= mid and j <= high:
        if l[i] >= l[j]:
            tmp.append(l[i])
            i+=1
        else:
            tmp.append(l[j])
            j+=1

    start = i if i<= mid else j
    end = mid if i<=mid  else high
    tmp.extend(l[start:end+1])
    l[low:high+1] = tmp

# 方法3 使用快速排序
def _quick_sort_first(l):
    high= len(l)-1
    _quick_sort(l,0,high)

import random
def _quick_sort(l,low,high):
    if low < high:
        pivot = random.randint(low,high-1)
        l[low] ,l[pivot] = l[pivot],l[low]

        m = parttion(l,low,high)

        _quick_sort(l,low,m-1)
        _quick_sort(l,m+1,high)

def parttion(l,low,high):
    pivot ,j= low,low
    for i in range(low+1,high+1):
        if l[i] <= l[pivot]:
            j+=1
            l[i],l[j]=l[j],l[i]
    l[pivot],l[j] = l[j],l[pivot]
    return j

# 堆排序
import heapq
def get_top_K(l,k):
    n = len(l)
    heapq.heapify(l)
    l=[heapq.heappop(l) for i in range(n)]
    return l[-k]



if __name__ == '__main__':
    l=[3,2,1,5,6,4]
    # print(findKthLargest( l,2))
    # _merge_sort_first(l)
    # _quick_sort_first(l)
    # print(l)
    print(get_top_K(l,2))