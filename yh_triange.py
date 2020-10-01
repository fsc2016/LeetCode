def yh_triange(yh_nums):
    '''
    计算永辉三角的最佳路线
    :param yh_nums: 永辉三角 [[3], [2, 6], [5, 4, 2], [6, 0, 3, 2]]
    :return:
    '''
    n = len(yh_nums)
    states=[[0]*i for i in range(1,n+1)]
    print(states)
    states[0][0] = yh_nums[0][0]
    for i in range(1,n):
        for j in range(i+1):
            if j == 0:
                states[i][j] = states[i-1][j] + yh_nums[i][j]
            elif j == i:
                states[i][j] = states[i-1][j-1] + yh_nums[i][j]
            else:
                states[i][j] = min(states[i-1][j-1]+yh_nums[i][j],states[i-1][j]+yh_nums[i][j])

    for i in states:
        print(i)

    print ('fsc')
    return min(states[n-1])
    

def get_road(states,yh_nums):
    n = len(states)
    tmp = []

    idx=states[n-1].index(min(states[n-1]))
    tmp.append(yh_nums[n-1][idx])
    for i in range(n-1)[::-1]:
        for j in range(i+1):
            pass
            # min()
    print('fsc')


if __name__ == '__main__':
    nums = [[3], [2, 6], [5, 4, 2], [6, 0, 3, 2]]
    print(yh_triange(nums))
