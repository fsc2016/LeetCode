class Node:
    def __init__(self,data,next=None):
        self.data=data
        self._next = next

class LinkedQueue:
    '''
    链表实现队列
    '''
    def __init__(self):
        self.head=None
        self.tail=None

    def enqueue(self,value):
        '''
        入队
        :param value:
        :return:
        '''
        new_node = Node(value)
        # 如果不是第一个入队元素
        if self.tail:
            self.tail._next=new_node
        else:
            self.head = new_node
        self.tail = new_node

    def dequeue(self):
        '''
        出队
        :return:
        '''
        if self.head:
            value = self.head.data
            self.head = self.head._next
            # 如果队列只有一个元素
            if not self.head:
                self.tail=None
            return value

    def __repr__(self):
        values=[]
        current = self.head
        while current:
            values.append(str(current.data))
            current = current._next
        return '->'.join(values)

if __name__ == '__main__':
    d = LinkedQueue()
    for i in range(10):
        d.enqueue(i)
    print(d)
    print(d.dequeue())
    print(d.dequeue())
    print(d)






