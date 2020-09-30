'''
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

示例 1:
输入: "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
链接：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters
'''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 暴力法
        # tmp=[]
        # n=len(s)
        # if n<2 :return n
        # for i in range(n):
        #     ss=set()
        #     ss.add(s[i])
        #     for j in s[i+1:]:
        #         if j not in ss:
        #             ss.add(j)
        #         else:
        #             break
        #     tmp.append(len(ss))
        # return max(tmp)

        # 移动窗口法
        occ = set()
        rk, ans = -1, 0
        n = len(s)
        for i in range(n):
            if i != 0:
                occ.remove(s[i - 1]) #从窗口左边依次删除，直到删除已经出现在set中的字符
            # 加入set
            while rk + 1 < n and s[rk + 1] not in occ:
                occ.add(s[rk + 1])
                rk += 1

            if ans < len(occ):
                ans = len(occ)
        return ans
