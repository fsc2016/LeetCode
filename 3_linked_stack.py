class Node:
    def __init__(self, data: int, next=None):
        self.data = data
        self._next = next

class LinkedStack:
    '''
    链表实现链式栈
    '''
    def __init__(self):
        self._top=None

    def push(self,value):
        node = Node(value)
        node._next = self._top
        self._top = node

    def pop(self):
        if self._top:
            value = self._top.data
            self._top=self._top._next
            return value

    def __repr__(self):
        if self._top:
            head=self._top
            values=[]
            while head :
                values.append(str(head.data))
                head=head._next
            return '->'.join(values)

if __name__ == "__main__":
    stack = LinkedStack()
    for i in range(9):
        stack.push(i)
    print(stack)
    for _ in range(3):
        stack.pop()
    print(stack)