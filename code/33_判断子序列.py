'''
给定字符串 s 和 t ，判断 s 是否为 t 的子序列。
你可以认为 s 和 t 中仅包含英文小写字母。字符串 t 可能会很长（长度 ~= 500,000），而 s 是个短字符串（长度 <=100）。
字符串的一个子序列是原始字符串删除一些（也可以不删除）字符而不改变剩余字符相对位置形成的新字符串。（例如，"ace"是"abcde"的一个子序列，而"aec"不是）。

示例 1:
s = "abc", t = "ahbgdc"
返回 true.

示例 2:
s = "axc", t = "ahbgdc"
返回 false.

链接：https://leetcode-cn.com/problems/is-subsequence
'''
def isSubsequence(s: str, t: str) -> bool:
    '''
    双指针法
    :param s:
    :param t:
    :return:
    '''
    slen,tlen = len(s),len(t)
    i,j = 0,0
    while i < slen and j < tlen:
        if s[i] == t[j]:
            i+=1
            j+=1
        else:
            j+=1
    return True if i ==slen else False

if __name__ == '__main__':
    s = "abc"
    t = "ahbgdc"

    print(isSubsequence(s,t))