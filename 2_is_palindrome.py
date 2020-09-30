import re
class Solution1:
    '''
    使用re
    '''
    pat =re.compile('[a-zA-Z\d]+')
    def isPalindrome(self, s: str):
        raw=''.join(self.pat.findall(s)).lower()
        reserve_raw = raw[::-1]
        return reserve_raw == raw


class Solution2:
    '''
    使用双指针,从头到尾挨个移动
    '''

    def isPalindrome(self, s: str):
        raw  = "".join(ch.lower() for ch in s if ch.isalnum())
        n = len(raw)
        left,right = 0,n-1
        while left <right:
            if raw[left] != raw[right]:
                return False
            left, right = left + 1, right + 1
        return True





if __name__ == '__main__':
    solu=Solution1()
    print(solu.isPalindrome("A man, a plan, a canal: Panama"))
    print(solu.isPalindrome("race a car"))