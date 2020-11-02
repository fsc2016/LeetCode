'''

验证二叉搜索树
给定一个二叉树，判断其是否是一个有效的二叉搜索树。
假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
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
        def helper(node:TreeNode,lower=float('-inf'),upper=float('inf'))->bool:
            if node is None:
                return True

            val = node.val
            if val <= lower or val >= upper:
                return False

            if not helper(node.left,lower,val):
                return False

            if not helper(node.right,val,upper):
                return False

            return True

        return helper(root)

    def isValidBST2(self, root: TreeNode) -> bool:
        '''
        中序遍历
        使用栈来进行存储中序遍历节点，每次判断与前一节点大小
        :param root:
        :return:
        '''
        stack ,preNodeVal= [],float('-inf')
        while stack or root:
            while root:
                stack.append(root)
                root = root.left

            root = stack.pop()
            if root.val <= preNodeVal:
                return False
            preNodeVal = root.val
            root = root.right
        return True




