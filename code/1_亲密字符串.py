'''
给定两个由小写字母构成的字符串 A 和 B ，只要我们可以通过交换 A 中的两个字母得到与 B 相等的结果，就返回 true ；否则返回 false 。
'''
'''
思路：
1，俩个字符串长度不相等，false
2，俩个字符串相等。且有重复元素，True
3，俩个字符串长度相等，有俩处字符不相等，查看不相等的处，调换位置看看
'''
class Solution:
    def buddyString(self,A,B) -> bool:
        if len(A) != len(B):
            return False

        if A == B and len(set(A)) < len(A):
            return True

        dif = [(a,b) for a,b in zip(A,B) if a!=b]
        if len(dif) == 2 and dif[0] == dif[1][::-1]:
            return True

        return False


if __name__ == '__main__':
    solu = Solution()
    print(solu.buddyString('ab','ba'))
