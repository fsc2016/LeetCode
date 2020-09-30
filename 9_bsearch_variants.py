def bsearch_left(l,value):
    '''
    二分查找查找第一个值等于给定值的元素
    :param l:
    :param value:
    :return:
    '''
    low = 0
    high = len(l) - 1
    while low <= high:
        mid = low + (high-low)//2
        if l[mid] > value:
            high = mid - 1
        elif l[mid] < value:
            low = mid + 1
        else:
            if mid == 0 or l[mid - 1] != value:
                return mid
            else:
                high = mid - 1
    return -1

def bsearch_right(l,value):
    '''
    查找最后一个值等于给定值的元素
    :param l:
    :param value:
    :return:
    '''
    low = 0
    high = len(l) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if l[mid] > value:
            high = mid - 1
        elif l[mid] < value:
            low = mid + 1
        else:
            if (mid == len(l) - 1) or l[mid + 1] != value:
                return mid
            else:
                low = mid + 1
    return -1

def bsearch_left_not_less(l,value):
    '''
    查找第一个大于等于给定值的元素
    :param l:
    :param value:
    :return:
    '''
    low = 0
    high = len(l) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if l[mid] >= value:
            if mid ==0 or l[mid-1] < value:
                return mid
            else:
                high = mid - 1
        elif l[mid] < value:
            low = mid + 1
    return -1


def bsearch_right_not_greater(l,value):
    '''
    查找最后一个小于等于给定值的元素
    :param l:
    :param value:
    :return:
    '''
    low = 0
    high = len(l) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if l[mid] > value:
            high = mid - 1
        elif l[mid] <= value:
            if mid == len(l)-1 or l[mid+1] > value:
                return  mid
            else:
                low = mid + 1
    return -1


if __name__ == '__main__':
    a = [1, 1, 2, 3, 4, 6, 7, 7, 7, 7, 10, 22]
    print(bsearch_left(a, 0) == -1)
    print(bsearch_left(a, 7) == 6)
    print(bsearch_left(a, 30) == -1)

    print(bsearch_right(a, 0) == -1)
    print(bsearch_right(a, 7) == 9)
    print(bsearch_right(a, 30) == -1)

    print(bsearch_left_not_less(a, 0) == 0)
    print(bsearch_left_not_less(a, 5) == 5)
    print(bsearch_left_not_less(a, 30) == -1)

    print(bsearch_right_not_greater(a, 0) == -1)
    print(bsearch_right_not_greater(a, 6) == 5)
    print(bsearch_right_not_greater(a, 30) == 11)
