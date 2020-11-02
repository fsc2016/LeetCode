'''
给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
链接：https://leetcode-cn.com/problems/validate-binary-search-tree
'''

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        '''
        递归法
        :param root:
        :return:
        '''
        def helper(root:TreeNode,lower=float('-inf'),uppder=float('inf')):
            if not root:
                return True

            val = root.val
            if val <= lower or val >=uppder:
                return False

            if not helper(root.left,lower,val):
                return False
            if not  helper(root.right,val,uppder):
                return False
            return True
        return helper(root)



