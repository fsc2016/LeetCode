'''
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof
'''
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    '''
    迭代法。p，q只有3种可能，
    1，要么都在root左子树
    2，要么都在root右子树
    3，一边在左子树，一边在右子树
    :param p:
    :param q:
    :return:
    '''
    if p.val > q.val:
        #始终保持 p < q
        p,q = q,p
    while root:
        if root.val < p.val:  #都在右子树,遍历右子树
            root = root.right
        elif root.val > q.val: #都在左子树
            root = root.left
        else:
            break
        return root


def lowestCommonAncestor2(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    '''
    递归法
    '''
    if p.val > q.val:
        #始终保持 p < q
        p,q = q,p
    def recu(root:TreeNode):
        if root.val < p.val:  #都在右子树,遍历右子树
             return recu(root.right)
        elif root.val > q.val: #都在左子树
             return recu(root.left)
        return root
    return recu(root)
