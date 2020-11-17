'''
实现 int sqrt(int x) 函数。

计算并返回 x 的平方根，其中 x 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

示例 1:

输入: 4
输出: 2
'''

def mySqrt(x: int) -> int:
    '''
    二分查找解决
    :param x:
    :return:
    '''
    l,r,ans = 0,x,-1
    while l <= r:
        mid = ( l + r ) // 2
        if mid*mid <= x:
            ans = mid
            l = mid + 1
        else:
            r = mid  - 1
    return ans