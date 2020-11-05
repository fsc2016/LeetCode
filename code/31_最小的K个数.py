'''
输入整数数组 arr ，找出其中最小的 k 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。
示例 1：
输入：arr = [3,2,1], k = 2
输出：[1,2] 或者 [2,1]

链接：https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof
'''
'''
分析
本题最简单的做法是排序。时间复杂度nlogn
其次是堆 时间复杂度是nlogk
最后是快速选择，时间复杂度是n
现在实现后面俩种
'''
from typing import List
import heapq
def getLeastNumbers( arr: List[int], k: int) -> List[int]:
    '''
    堆排序
    :param arr:
    :param k:
    :return:
    '''
    if k == 0:
        return []
    hp=[]
    for i in arr[:k]:
        # 建立小顶堆，使用相反数得到大顶堆
        hp.append(-i)
    heapq.heapify(hp)
    for i in arr[k:]:
        # 现在是大顶推
        if -i > hp[0]:
            heapq.heappop(hp)
            heapq.heappush(hp,-i)
    ans =[-i for i in hp]
    return ans

import random
def getLeastNumbers2( arr: List[int], k: int) -> List[int]:
    '''
    快速选择法
    :param arr:
    :param k:
    :return:
    '''
    if k == 0:return []
    randomized_selected(arr,0,len(arr)-1,k)
    return arr[:k]

def randomized_selected(arr:List,l,r,k):
    '''
    我们定义函数 randomized_selected(arr, l, r, k) 表示划分数组 arr 的 [l,r] 部分，使前 k 小的数在数组的左侧，在函数里我们调用快排的划分函数，假设划分函数返回的下标是 pos（表示分界值 pivot 最终在数组中的位置），即 pivot 是数组中第 pos - l + 1 小的数，
    那么一共会有三种情况：
    如果 pos - l + 1 == k，表示 pivot 就是第 kk 小的数，直接返回即可；
    如果 pos - l + 1 < k，表示第 kk 小的数在 pivot 的右侧，因此递归调用 randomized_selected(arr, pos + 1, r, k - (pos - l + 1))；
    如果 pos - l + 1 > k，表示第 kk 小的数在 pivot 的左侧，递归调用 randomized_selected(arr, l, pos - 1, k)。
    :return:
    '''
    pos = randomized_partition(arr,l,r)
    num = pos - l + 1
    if num < k:
        randomized_selected(arr ,pos +1,r,k-num)
    if num > k:
        randomized_selected(arr,l,pos-1,k)

# 下面利用快排的过程
def randomized_partition(arr,l,r):
    pidx = random.randint(l,r)
    arr[l],arr[pidx] = arr[pidx],arr[l]
    m = partition(arr,l,r)
    return m

def partition(arr,l,r):
    pivot ,j = arr[l],l
    for i in range(l+1,r+1):
        if arr[i] <= pivot:
            j+=1
            arr[i],arr[j] = arr[j],arr[i]
    arr[l],arr[j] = arr[j] ,arr[l]
    return j


if __name__ == '__main__':
    arr = [3, 2, 1]
    k = 2
    print(getLeastNumbers2(arr,k))
