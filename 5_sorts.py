
def bubble_sort(ll):
    '''
    冒泡
    :param ll:
    :return:
    '''
    length=len(ll)
    if length <=1:
        return
    for i in range(length):
        # swap= False
        for j in range(length-i-1):
            if ll[j]>ll[j+1]:
                ll[j],ll[j+1]=ll[j+1],ll[j]
                # swap = True
        # if not swap:
        #     break


def inset_sort(ll):
    '''
    插入
    :param ll:
    :return:
    '''
    length = len(ll)
    if length <= 1:
        return

    for i in range(1,length):
        value = ll[i]
        j = i -1
        # 在已排区间查找插入位置
        while j>=0 and (ll[j]>value):
            # 数据移动
            ll[j+1] = ll[j]
            j-=1
        #插入数据
        ll[j+1] = value

if __name__ == "__main__":
    array = [5, 6, -1, 4, 2, 8, 10, 7, 6]
    bubble_sort(array)
    print(array)

    array = [5, 6, -1, 4, 2, 8, 10, 7, 6]
    inset_sort(array)
    print(array)






