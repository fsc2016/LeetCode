'''
定义栈的数据结构，请在该类型中实现一个能够得到栈的最小元素的 min 函数在该栈中，调用 min、push 及 pop 的时间复杂度都是 O(1)。
示例:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.min();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.min();   --> 返回 -2.

链接：https://leetcode-cn.com/problems/bao-han-minhan-shu-de-zhan-lcof
'''
class MinStack:
    '''
    辅助栈是严格有序的
    '''

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.l = []
        self.deque=[]

    def push(self, x: int) -> None:
        self.l.append(x)
        if self.deque:
            for i in range(len(self.deque)):
                if self.deque[i] < x:
                    self.deque.insert(i,x)
                    return
        self.deque.append(x)

    def pop(self) -> None:
        popnum=self.l.pop()
        self.deque.remove(popnum)


    def top(self) -> int:
        return self.l[-1]


    def min(self) -> int:
        return self.deque[-1]


class MinStack1:
    '''
    非严格有序
    '''

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.l = []
        self.deque=[]

    def push(self, x: int) -> None:
        self.l.append(x)
        if not self.deque or self.deque[-1] > x:
            self.deque.append(x)


    def pop(self) -> None:
        if self.l.pop() == self.deque[-1]:
            self.deque.pop()

    def top(self) -> int:
        return self.l[-1]

    def min(self) -> int:
        return self.deque[-1]


if __name__ == '__main__':
    minStack = MinStack1()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-1)
    print(minStack.deque)
    print(minStack.min())
    print(minStack.top())
    minStack.pop()

    print(minStack.min())
