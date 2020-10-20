'''
定义一个函数，输入一个链表的头节点，反转该链表并输出反转后链表的头节点。
示例:
输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/fan-zhuan-lian-biao-lcof
'''

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Linklist:
    def __init__(self):
        pass


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        reverse_head = None
        cur = head
        reverse_head,reverse_head.next,cur = cur,reverse_head,cur.next

    def reverseList_rv1(self, head: ListNode) -> ListNode:
        reserve_head = None
        cur = head
        while cur:
            reserve_head,reserve_head.next,cur = cur,reserve_head,cur.next
        return reserve_head

if __name__ == '__main__':
    l=[1,2,3,4,5]
    for i in l:
        node = ListNode(i)
