'''
给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

说明：不允许修改给定的链表。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/linked-list-cycle-ii
'''
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # 暴力枚举法
    def detectCycle(self, head: ListNode) -> ListNode:
        hashset=set()
        cur = head
        while cur:
            if cur in hashset:
                return cur
            hashset.add(cur)
            cur = cur.next
        return None

    # 双指针法
    def detectCycle2(self, head: ListNode) -> ListNode:
        fast,slow = head,head
        while fast and fast.next:
            fast,slow=fast.next.next, slow.next
            # 有环
            if fast == slow:
                meetcode = slow
                start = head
                while start != meetcode:
                    start, meetcode = start.next, meetcode.next
                return start
        return None


