def bsarch(l,value):
    '''
    二分查找循环形式
    l中没有重复元素
    :param l:
    :return:
    '''
    low = 0
    high = len(l) - 1
    while low <= high:
        # 更新mid
        mid = low + (high-low)//2
        if l[mid] == value:
            return mid
        # 更新high与low
        elif l[mid] < value:
            low = mid + 1
        else:
            high = mid - 1
    # 没有找到
    return -1

def bseach_rec(l,low,high,value):
    '''
    递归实现二分查找
    :param l:
    :param low:
    :param high:
    :param value:
    :return:
    '''
    # 递归结束标记
    if low > high:
        return -1

    mid = low + (high - low) // 2
    if l[mid] == value:
        return  mid
    elif l[mid] < value:
        bseach_rec(l,mid+1,high,value)
    else:
        bseach_rec(l,low,mid-1,value)

if __name__ == '__main__':
    l =[1,2,5,7,8,9,11,13,14,18,23,34,56,57,59,60,78,89]
    print(bsarch(l,14))
    print(l[bsarch(l,14)])
    print(bseach_rec(l,0,len(l)-1,14))