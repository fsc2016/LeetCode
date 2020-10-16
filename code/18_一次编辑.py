'''
字符串有三种编辑操作:插入一个字符、删除一个字符或者替换一个字符。 给定两个字符串，编写一个函数判定它们是否只需要一次(或者零次)编辑。
示例 1:
输入:
first = "pale"
second = "ple"
输出: True

示例 2:
输入:
first = "pales"
second = "pal"
输出: False
链接：https://leetcode-cn.com/problems/one-away-lcci
'''
from typing import *
def oneEditAway(first: str, second: str) -> bool:
    '''
    不属于动态规划了
    双指针法，对于字符串长度差为1，使用从前往后 和从后往前各扫描一遍。
    :param first:
    :param second:
    :return:
    '''

    alen = len(first)
    blen = len(second)
    if abs(alen - blen) > 1:
        return False
    i =0
    j = alen - 1
    k = blen - 1
    while (i<= j and i <=k and first[i] == second[i]):
        i+=1
    while (j >=0 and k >=0 and first[j] == second[k]):
        j-=1
        k -=1

    # print(i, j, k)
    return j-i < 1 and  k-i<1


if __name__ == '__main__':
    first = "pale"
    second = "palec"
    print(oneEditAway(first,second))







