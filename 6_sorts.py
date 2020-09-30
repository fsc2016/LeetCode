def merge_sort(l):
    '''
    归并排序，采用分治思想和递归的编程技巧
    :param l:
    :return:
    '''
    _merge_sort_l(l,0,len(l)-1)

def _merge_sort_l(l,low,high):
    if low < high:
        mid = low + (high-low)//2
        # 递归调用
        _merge_sort_l(l,low,mid)
        _merge_sort_l(l,mid+1,high)
        # 递调用结束后，开始归调用，挨个合并数组
        merge(l,low,mid,high)

def merge(l,low,mid,high):
    # 合并俩个排序好的序列，通过新加一个tmp
    # l[low:mid], l[mid+1, high] are sorted.
    tmp = []
    i ,j = low,mid+1
    while i<=mid and j <=high:
        if l[i] <= l[j]:
            tmp.append(l[i])
            i+=1
        else:
            tmp.append(l[j])
            j+=1
    start = i if i <= mid else j
    end  = mid if i <=mid else high
    tmp.extend(l[start:end+1])
    l[low:high+1] = tmp

if __name__ == "__main__":
    a1 = [3, 5, 6, 7, 8]
    a2 = [2, 2, 2, 2]
    a3 = [4, 3, 2, 1]
    a4 = [5, -1, 9, 3, 7, 8, 3, -2, 9]
    merge_sort(a1)
    print(a1)
    merge_sort(a2)
    print(a2)
    merge_sort(a3)
    print(a3)
    merge_sort(a4)
    print(a4)





