import  random
'''
快速排序
'''
def quick_sort(l):
    length = len(l)
    _quick_sort_bet(l,0,length-1)

def _quick_sort_bet(l,low,high):
    if low < high:
        j = random.randint(low,high)
        # 把随机的元素交换到第一个位置
        l[low],l[j] = l[j],l[low]
        # 先分区
        m = parttion(l,low,high)

        _quick_sort_bet(l,low,m-1)
        _quick_sort_bet(l,m+1,high)

def parttion(l,low,high):
    # 比较元素为队首，先固定不动，遍历队首后面的元素，比他小的和队首后第一个元素互换位置，依次类推。最后把队首和最后一个比较元素互换位置
    pivot,j = l[low],low
    for i in range(low+1,high+1):
        if l[i] <= pivot:
            j += 1
            # 交换位置
            l[i],l[j] = l[j],l[i]
    l[low],l[j]=l[j],l[low]
    return j


if __name__ == "__main__":
    a1 = [3, 5, 6, 7, 8]
    a2 = [2, 2, 2, 2]
    a3 = [4, 3, 2, 1]
    a4 = [5, -1, 9, 3, 7, 8, 3, -2, 9]
    quick_sort(a1)
    print(a1)
    quick_sort(a2)
    print(a2)
    quick_sort(a3)
    print(a3)
    quick_sort(a4)
    print(a4)

