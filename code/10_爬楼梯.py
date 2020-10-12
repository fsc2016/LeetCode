'''
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
注意：给定 n 是一个正整数。
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/climbing-stairs
'''
def climbStairs(n :int) ->int:
    '''
    递推加备忘录
    :param n:
    :return:
    '''
    count =0
    tables= [0]*n
    def getCount(remain):
        global count
        if remain == 1:return 1
        if remain == 2:return 2

        if tables[remain-1]:
            return tables[remain-1]

        count = getCount(remain-1) + getCount(remain-2)
        tables[remain-1] = count
        print(remain,count)
        return count

    return getCount(n)

def climbStairs2(n :int) ->int:
    tables=[0] * n
    tables[0] = 1
    tables[1] = 2
    for i in range(2,n):
        tables[i] = tables[i-1]+ tables[i-2]
    print(tables)
    return tables[n-1]

def climbStairs3(n :int) ->int:
    '''
    空间复杂度为O（1）
    :param n:
    :return:
    '''
    if n == 1: return 1
    if n==2 :return 2
    first  = 1
    second = 2
    for i in range(2,n):
        three= first + second
        first,second = second,three
    return three


if __name__ == '__main__':
    # print(climbStairs(5))
    print(climbStairs3(5))