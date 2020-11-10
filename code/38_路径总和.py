'''
112-路径总和
给定一个二叉树和一个目标和，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。
说明: 叶子节点是指没有子节点的节点。
'''
class TreeNode:
        def __init__(self, x):
            self.val = x
            self.left = None
            self.right = None

from collections import deque
class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:return False
        dq_node = deque()
        dq_value= deque()
        dq_node.append(root)
        dq_value.append(root.val)
        while dq_node:
            node=dq_node.popleft()
            value = dq_value.popleft()
            if value == sum and not node.left and not node.right:
                return True
            if node.left:
                dq_node.append(node.left)
                dq_value.append(value+node.val)
            if node.right:
                dq_node.append(node.right)
                dq_value.append(value+node.val)
        return False

