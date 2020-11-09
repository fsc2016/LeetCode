'''
给定一个二叉树，找出其最小深度。
最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
说明：叶子节点是指没有子节点的节点。
111. 二叉树的最小深度
'''
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def minDepth(self,root: TreeNode) -> int:
        '''
        dfs
        :return:
        '''
        def recu(root):
            if not root:
                return 0
            if not root.left and not root.right:
                return 1
            mindepth=float('inf')
            if root.left:
                mindepth = min(mindepth,self.minDepth(root.left))
            if root.right:
                mindepth = min(mindepth, self.minDepth(root.right))
            return mindepth+1
        return recu(root)

    def minDepth2(self, root: TreeNode) -> int:
        '''
        bfs
        '''

        if not root:
            return 0
        dq = deque()
        dq.append([root, 1])
        while dq:
            tmp, depth = dq.popleft()
            if not tmp.left and not tmp.right:
                return depth
            if tmp.left:
                dq.append([tmp.left, depth + 1])
            if tmp.right:
                dq.append([tmp.right, depth + 1])
        return 0



    '''
    输入一棵二叉树的根节点，求该树的深度。从根节点到叶节点依次经过的节点（含根、叶节点）形成树的一条路径，最长路径的长度为树的深度。
    剑指 Offer 55 - I. 二叉树的深度
    '''
    def maxDepth2(self, root: TreeNode) -> int:
        if not root:
            return 0
        dq = deque()
        dq.append([root,1])
        maxdepth = float('-inf')
        while dq:
            node,depth =dq.popleft()
            maxdepth = max(maxdepth,depth)
            if node.left:
                dq.append([node.left,depth+1])
            if node.right:
                dq.append([node.right, depth + 1])

        return maxdepth

