'''
这里是 4 道相关题目：
144.二叉树的前序遍历
94. 二叉树的中序遍历
145. 二叉树的后序遍历
102. 二叉树的层序遍历
'''
from typing import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        '''
        前序遍历-递归
        :param root:
        :return:
        '''
        res=[]
        def dfs(root:TreeNode):
            if not root:
                return
            nonlocal res
            res.append(root.val)
            dfs(root.left)
            dfs(root.right)
        dfs(root)
        return res

    def preorderTraversal_2(self, root: TreeNode) -> List[int]:
        '''
        前序遍历-栈迭代法,先进后出
        :param root:
        :return:
        '''
        if not root : return []
        stack,res=[],[]
        cur = root
        while stack or cur:
            while cur:
                res.append(cur.val)
                stack.append(cur)
                cur = cur.left
            tmp = stack.pop()
            cur = tmp.right
        return res



    def inorderTraversal(self, root: TreeNode) -> List[int]:
        '''
        中序遍历-递归
        :param root:
        :return:
        '''
        res = []
        def dfs(root: TreeNode):
            if not root:
                return
            nonlocal res
            dfs(root.left)
            res.append(root.val)
            dfs(root.right)

        dfs(root)
        return res

    def inorderTraversal_2(self, root: TreeNode) -> List[int]:
        '''
        中序遍历-迭代
        :param root:
        :return:
        '''
        if not root : return []
        stack ,res =[],[]
        cur = root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            tmp = stack.pop()
            res.append(tmp.val)
            cur = tmp.right
        return res

    def postorderTraversal(self, root: TreeNode) -> List[int]:
        '''
        后序遍历-递归
        :param root:
        :return:
        '''
        res = []

        def dfs(root: TreeNode):
            if not root:
                return
            nonlocal res
            dfs(root.left)
            dfs(root.right)
            res.append(root.val)

        dfs(root)
        return res

    def postorderTraversal_2(self, root: TreeNode) -> List[int]:
        '''
        后序遍历-迭代
        :param root:
        :return:
        '''
        if not root : return []
        cur ,res,stack = root,[],[]
        while stack or cur:
            while cur:
                res.append(cur.val)
                stack.append(cur)
                cur = cur.right
            tmp = stack.pop()
            cur = tmp.left

        return res[::-1]
