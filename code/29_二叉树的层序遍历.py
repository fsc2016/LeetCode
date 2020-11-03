'''
给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。
二叉树：[3,9,20,null,null,15,7],
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal

107. 二叉树的层次遍历 II
给定一个二叉树，返回其节点值自底向上的层次遍历。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）

俩题解题思路类似，只是返回值不同
'''
from typing import *
from collections import deque
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        '''
        BFS，使用优先级队列来保存节点
        :param root:
        :return:
        '''
        queue = deque()
        queue.append(root)
        res=[]
        while queue:
            size = len(queue)
            level = []
            # 遍历当前层
            for _ in range(size):
                cur = queue.popleft()
                # 如果当前节点为空，continue
                if not cur:
                    continue
                level.append(cur.val)
                queue.append(cur.left)
                queue.append(cur.right)
            if level:
                res.append(level)
        return res
