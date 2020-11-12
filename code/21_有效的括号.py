'''
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
有效字符串需满足：
左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
注意空字符串可被认为是有效字符串。
示例 1:
输入: "()"
输出: true

示例 2:
输入: "()[]{}"
输出: true

示例 3:
输入: "(]"
输出: false

示例 4:
输入: "([)]"
输出: false

示例 5:
输入: "{[]}"
输出: true
链接：https://leetcode-cn.com/problems/valid-parentheses
'''
from typing import *
def isValid(s: str) -> bool:
    kv = {")": "(", "]": "[", "}": "{", }
    n = len(s)
    if n == 0:
        return True
    if n % 2 != 0:
        return False
    stack = []
    for i in s:
        # if i in kv.keys() and not stack:
        #     return False
        # if i in kv.values():
        #     stack.append(i)
        # else:
        #     if stack.pop() != kv.get(i):
        #         return False
        if i in kv.keys():
            if not stack or stack.pop() !=  kv.get(i):
                return False
        else:
            stack.append(i)
    return not stack


if __name__ == '__main__':
    s = "{[]}"
    s='()[]{}'
    s="()"
    print(isValid(s))


