'''
给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。
'''
class Solution:
    def reverseWords(self, s: str) -> str:
        s = s.split(' ')
        s = ' '.join([i[::-1] for i in s if i])
        return s