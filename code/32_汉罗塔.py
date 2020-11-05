'''
在经典汉诺塔问题中，有 3 根柱子及 N 个不同大小的穿孔圆盘，盘子可以滑入任意一根柱子。一开始，所有盘子自上而下按升序依次套在第一根柱子上(即每一个盘子只能放在更大的盘子上面)。移动圆盘时受到以下限制:
(1) 每次只能移动一个盘子;
(2) 盘子只能从柱子顶端滑出移到下一根柱子;
(3) 盘子只能叠在比它大的盘子上。
请编写程序，用栈将所有盘子从第一根柱子移到最后一根柱子。
你需要原地修改栈。
示例1:
 输入：A = [2, 1, 0], B = [], C = []
 输出：C = [2, 1, 0]

链接：https://leetcode-cn.com/problems/hanota-lcci
'''
from typing import List
def hanota(A: List[int], B: List[int], C: List[int]) -> None:
    '''
    递归法
    :param A:
    :param B:
    :param C:
    :return:
    '''

    def move(A,B,C,n):
        if n == 1:
            C.append(A.pop())
            return

        move(A,C,B,n-1) #通过 C 把 A中n-1移动到B中
        # print('1_move:{}:{}:{}'.format(A,B,C))
        C.append(A.pop()) #把A中最后一个盘移动到C
        # print('2_move:{}:{}:{}'.format(A, B, C))
        move(B,A,C,n-1) #通过A柱 ，把B柱n-1个盘移动到C

    n = len(A)
    move(A,B,C,n)
    print(C)

if __name__ == '__main__':
    A = [4,3,2, 1, 0]
    B = []
    C = []
    hanota(A,B,C)




