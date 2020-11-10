'''
给定一个二叉树，检查它是否是镜像对称的。
例如，二叉树 [1,2,2,3,4,4,3] 是对称的
'''
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import deque
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        '''
        迭代法
        :param root:
        :return:
        '''
        if not root or not (root.left or root.right):
            return True
        dq = deque()
        dq.append(root.left)
        dq.append(root.right)
        while dq:
            node_left = dq.popleft()
            node_right= dq.popleft()
            # 左右子节点都有空
            if not node_left and not node_right:
                continue

            # 有一个节点为空一个为True，就不对称
            if not node_left or not node_right:
                return False

            # 俩个都有的节点比较值
            if node_left.val != node_right.val:
                return False

            # 一次对称加入优先级队列
            dq.append(node_left.left)
            dq.append(node_right.right)
            dq.append(node_left.right)
            dq.append(node_right.left)
        return True

    def isSymmetric2(self, root: TreeNode) -> bool:
        '''
        递归法
        :param root:
        :return:
        '''
        if not root: return True
        def dfs(left:TreeNode,right:TreeNode):
            #递归结束条件
            if not left and not right:
                return True
            if not left or not right:
                return False
            if left.val != right.val:
                return False
            return dfs(left.left,right.right) and dfs(left.right,right.left)
        return dfs(root.left,root.right)
