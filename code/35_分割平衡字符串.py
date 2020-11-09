''''
在一个「平衡字符串」中，'L' 和 'R' 字符的数量是相同的。
给出一个平衡字符串 s，请你将它分割成尽可能多的平衡字符串。
返回可以通过分割得到的平衡字符串的最大数量。

示例 1：
输入：s = "RLRRLLRLRL"
输出：4
解释：s 可以分割为 "RL", "RRLL", "RL", "RL", 每个子字符串中都包含相同数量的 'L' 和 'R'。

链接：https://leetcode-cn.com/problems/split-a-string-in-balanced-strings
'''
def balancedStringSplit(s: str) -> int:
    '''
    辅助栈的用法
    :param s:
    :return:
    '''
    l = []
    res=0
    for i in range(len(s)):
        if not l or l[-1] == s[i]:
            l.append(s[i])
        else:
            l.pop()
        if len(l) == 0:
            res+=1
    return res

if __name__ == '__main__':
    s = "RLRRLLRLRL"
    print(balancedStringSplit(s))
