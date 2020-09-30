class Node:
    def __init__(self,data,next_node=None):
        self.data=data
        self._next = next_node

class SingleLinkedList:
    def __init__(self):
        self._head=None

    # 通过value找节点
    def find_by_value(self,value):
        p = self._head
        while p and p.data != value:
            p=p._next
        return p

    #给定偏移量找节点
    def find_by_index(self,index):
        p=self._head
        position=0
        while p and position != index:
            p = p._next
            position+=1
        return p


    def insert_value_to_head(self,value):
        new_node = Node(value)
        self.insert_node_to_head(new_node)

    # 插入新节点到头节点
    def insert_node_to_head(self,newnode):
        if newnode:
            newnode._next = self._head
            self._head = newnode

    def insert_value_after(self,node,value):
        new_node = Node(value)
        self.insert_node_to_head(node,new_node)

    # 在某一节点后面插入新节点
    def insert_node_after(self,node,newnode):
        if not node or not newnode:
            return
        newnode._next=node._next
        node._next = newnode


    def insert_value_before(self,node,value):
        new_node = Node(value)
        self.insert_node_before(node,new_node)

    # 在某一节点前面插入一个节点
    def insert_node_before(self,node,new_node):
        if not node or not new_node or not self._head:
            return
        # 如果是目标节点时头结点
        if self._head== node:
            self.insert_node_to_head(new_node)
            return

        # 查找出在目标节点的前一个节点
        current = self._head
        while current and current._next !=node:
            current = current._next
        # 目标节点不在当前链表中
        if not current:
            return
        # 插入操作
        current._next = new_node
        new_node._next=node


    def delete_by_node(self,node):
        if not self._head or not node:
            return
        #把下一个节点赋值当前节点
        if node._next:
            node.data = node._next.data
            node._next = node._next._next

#        如果待删除节点不在链表中或者是尾节点
        current = self._head
        while current and current._next != node:
            current = current._next
        if not current:
            return
        current._next = node._next

    def __repr__(self):
        nums = []
        current = self._head
        while current:
            nums.append(current.data)
            current = current._next
        return "->".join(str(num) for num in nums)

    # 重写__iter__方法，方便for关键字调用打印值
    def __iter__(self):
        node = self._head
        while node:
            yield node.data
            node = node._next




    def print_all(self):
        current = self._head
        if current:
            print(f"{current.data}", end="")
            current = current._next
        while current:
            print(f"->{current.data}", end="")
            current = current._next
        print("\n", flush=True)

def reverse(head):
    '''
    反转单链表
    :param head:
    :return:
    '''
    reverse_head=None
    current=head
    while current:
        reverse_head,reverse_head._next,current = current,reverse_head,current._next
    return  reverse_head


def has_cycle(node):
    '''检测环

    :param node:
    :return:
    '''
    fast,low = node,node
    while fast and fast._next:
        fast=fast._next._next
        low = low._next
        if fast == low:return True
    return False

def merge_sorted_list(l1,l2):
    '''
    有序链表合并
    :param l1:
    :param l2:
    :return:
    '''
    if l1 and l2:
        p1,p2= l1,l2
        # 合并链表后的新链表
        fake_node = Node(None)
        current = fake_node
        # 循环判断链表大小，有序合并到一起
        while p1 and p2:
            if p1.data <= p2.data:
                current._next = p1
                p1 = p1._next
            else:
                current._next = p2
                p2 = p2._next
            current = current._next
        #最先遍历完的是哪一个链表
        current._next =p1 if p1 else p2
        return fake_node




def find_middle_ndoe(head):
    '''
    查找链表中间节点
    :param head:
    :return:
    '''
    slow,fast = head,head
    fast = fast._next if fast else None
    while fast and fast._next:
        fast = fast._next._next
        slow = slow._next
    return slow


# 打印输出
def printall(node:Node):
    l=[]
    while node:
        l.append(str(node.data))
        node = node._next
    print('->'.join(l))


if __name__ == "__main__":
    l = SingleLinkedList()
    for i in range(15):
        l.insert_value_to_head(i)
    # node9 = l.find_by_value(9)
    # l.insert_value_before(node9, 20)
    # l.insert_value_before(node9, 16)
    # l.insert_value_before(node9, 16)
    # # l.delete_by_value(16)
    # node11 = l.find_by_index(3)
    # l.delete_by_node(node11)
    # l.delete_by_node(l._head)
    # l.delete_by_value(13)
    print(l)
    # print(l.find_by_index(0).data)
    # printall(reverse(l.find_by_index(0)))
    # print(has_cycle(l.find_by_index(0)))

#     测试有序链表合并
    l2 = SingleLinkedList()
    for i in range(6,10):
        l2.insert_node_to_head(Node(i))

    # print(l2)
    # printall(reverse(l.find_by_index(0)))
    # printall(reverse(l.find_by_index(0)))
    # printall(l2.find_by_index(0))
    l1_node =reverse(l.find_by_index(0))
    l2_node =reverse(l2.find_by_index(0))
    # print(l2)
    printall(l2_node)
    # printall(reverse(l2.find_by_index(0)))
    printall(l1_node)
    # merge_headnode = merge_sorted_list(l1_node,l2_node)
    # printall(merge_headnode)
    printall(find_middle_ndoe(l2_node))

















