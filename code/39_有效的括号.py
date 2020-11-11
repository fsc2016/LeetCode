'''
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。
示例：
输入：n = 3
输出：[
       "((()))",
       "(()())",
       "(())()",
       "()(())",
       "()()()"
     ]
链接：https://leetcode-cn.com/problems/generate-parentheses
'''
from typing import List
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        self.list = []
        result = ''
        self._gen(0,0,n,result)
        return self.list

    def _gen(self, left, right, n, result):
        if left == n and right == n:
            self.list.append(result)

        if left < n:
            self._gen(left+1,right,n,result+'(')

        if right < left:
            self._gen(left,right+1,n ,result+')')
