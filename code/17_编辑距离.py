'''
给你两个单词 word1 和 word2，请你计算出将 word1 转换成 word2 所使用的最少操作数 。
你可以对一个单词进行如下三种操作：
插入一个字符
删除一个字符
替换一个字符

示例 1：
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')

链接：https://leetcode-cn.com/problems/edit-distance
'''
def oneEditAway(first: str, second: str) -> int:
    '''
    动态规划，从后往前进行。动态转移表需要设置哨兵，进行初始化
    状态定义：dp[i][j] 表示的是word1 前i个字符与word2 前j个字符的 编辑距离
    :param first:
    :param second:
    :return:
    '''
    alen = len(first)
    blen = len(second)
    # 如果为0
    if alen * blen == 0:
        return alen+blen

    dp= [[0]*(blen+1) for _ in range(alen+1)]
    # 初始化状态转移表
    for i in range(alen+1):
        dp[i][0] = i
    for j in range(blen+1):
        dp[0][j] = j

    for i in range(1,alen+1):
        for j in range(1,blen+1):
            # 状态转移方程分成俩方面，一个是最后一个字符相同。另外是不同有三种情况推导出来
            if first[i-1] == second[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                left = dp[i-1][j]
                down = dp[i][j-1]
                left_down = dp[i-1][j-1]
                dp[i][j] = 1 + min(left,down,left_down)
    return dp[alen][blen]

def oneEditAway_rv1(first: str, second: str) -> int:
    alen = len(first)
    blen = len(second)
    # 二维动态数据
    dp=[[0]*(blen+1) for _ in range(alen+1)]

#     初始化二维动态数据，哨兵
    for i in range(alen+1):
        dp[i][0] = i
    for j in range(blen+1):
        dp[0][j] = j

    for i in range(1,alen+1):
        for j in range(1,blen+1):
            if first[i-1] == second[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                left = dp[i][j-1]
                up = dp[i-1][j]
                left_up = dp[i-1][j-1]
                dp[i][j] = 1 + min(left,up,left_up)
    for i in dp:
        print(i)
    return dp[alen][blen]


if __name__ == '__main__':
    word1 = "horse"
    word2 = "ros"
    print(oneEditAway(word1,word2))
    print(oneEditAway_rv1(word1, word2))
