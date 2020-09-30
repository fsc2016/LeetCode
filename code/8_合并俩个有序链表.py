'''
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 
示例：
输入：1->2->4, 1->3->4
输出：1->1->2->3->4->4
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/merge-two-sorted-lists
'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        head=None
        while l1.next and l2.next:
            if l1.val <= l2.val:
                if not head:
                    head =l1
                else:
                    head.next =l1


