'''
给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。
相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。
例如，给定三角形：
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。
链接：https://leetcode-cn.com/problems/triangle
'''
from typing import *
def minimumTotal(triangle:List[List[int]]) -> int:
    '''
    动态规划中动态转移表法
    :param triangle:
    :return:
    '''
    n = len(triangle)
    tables = [[0] * i for i in range(1,n+1)]
    tables[0][0]  =triangle[0][0]
    for i in range(1,n):
        for j in range(i+1):
            if j == 0:
                tables[i][j] = tables[i-1][j] + triangle[i][j]
            elif j == i:
                tables[i][j] = tables[i-1][j-1] + triangle[i][j]
            else:
                tables[i][j] = triangle[i][j] + min(tables[i-1][j-1],tables[i-1][j])
    # print(tables[n-1])
    return min(tables[n-1])

def minimumTotal2(triangle:List[List[int]]) -> int:
    pass


if __name__ == '__main__':
    triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
    print(minimumTotal(triangle))