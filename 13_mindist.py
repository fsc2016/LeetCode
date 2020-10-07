from  typing import List
def min_dist(weights:List[List[int]]) -> int:
    '''
    动态转移表法
    :param weights:
    :return:
    '''
    m,n = len(weights),len(weights[0])
    tables=[[0]*n for _ in range(m)]
    # 初始化第一行
    sum=0
    for i in range(n):
        sum += weights[0][i]
        tables[0][i] = sum

    # 初始化第一列
    sum = 0
    for j in range(m):
        sum += weights[j][0]
        tables[j][0] = sum

    for j in range(1, m):
        for i in range(1,n):
            tables[j][i] = weights[j][i] + min(tables[j-1][i],tables[j][i-1])

    return tables[m-1][n-1]

def min_dist_recur(weights:List[List[int]]) -> int:
    '''
    动态转移方程法。递归+备忘录
    :param weights:
    :return:
    '''
    m , n  = len(weights),len(weights[0])
    tables = [[0]*n for _ in range(m)]
    def min_dist_to(i:int,j:int)->int:
        if i == 0 and j == 0:
            return weights[0][0]
        if tables[i][j]:
            return  tables[i][j]

        min_left,min_up =float('inf'),float('inf')
        if j >= 0 :
            min_left = min_dist_to(i,j-1)

        if i >= 0 :
            min_up = min_dist_to(i-1,j)

        min_current = weights[i][j] + min(min_left,min_up)
        tables[i][j] = min_current
        return min_current

    return min_dist_to(m - 1, n - 1)

def min_dist_recur2(weights: List[List[int]]) -> int:
    m, n = len(weights), len(weights[0])
    table = [[0] * n for _ in range(m)]
    def min_dist_to(i: int, j: int) -> int:
        if i == j == 0: return weights[0][0]
        if table[i][j]: return table[i][j]
        min_left = float("inf") if j - 1 < 0 else min_dist_to(i, j - 1)
        min_up = float("inf") if i - 1 < 0 else min_dist_to(i - 1, j)
        return weights[i][j] + min(min_left, min_up)
    return min_dist_to(m - 1, n - 1)



if __name__ == "__main__":
    weights = [[1, 3, 5, 9], [2, 1, 3, 4], [5, 2, 6, 7], [6, 8, 4, 3]]
    print(min_dist_recur2(weights))
    print(min_dist_recur(weights))
