'''
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1:
输入: s = "anagram", t = "nagaram"
输出: true
示例 2:
输入: s = "rat", t = "car"
输出: false

链接：https://leetcode-cn.com/problems/valid-anagram
'''
from collections import defaultdict
def isAnagram(s: str, t: str) -> bool:
    s1n = len(s)
    s2n = len(t)
    if s1n != s2n : return False
    s1dict,s2dict = defaultdict(int),defaultdict(int)
    for i in range(s1n):
        s1dict[s[i]] += 1
        s2dict[t[i]] += 1
    for key in s1dict.keys():
        if s1dict[key] != s2dict[key]:
            return False
    return True

if __name__ == '__main__':
    s = "anagram"
    t = "nagaram"
    print(isAnagram(s,t))