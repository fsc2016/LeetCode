# 1) Insertion, deletion and random access of array
# 2) Assumes int for element type
#

class MyArray:
    """A simple wrapper around List.
      You cannot have -1 in the array.
      """
    def __init__(self,cap:int):
        self._data=[]
        self._cap=cap

    def __setitem__(self, key, value):
        self._data[key]=value

    def __getitem__(self, item):
        return  self._data[item]

    def __len__(self):
        return len(self._data)

    def find(self,index):
        try:
            return self._data[index]
        except IndexError:
            return None


    def delete(self, index):
        try:
            self._data.pop(index)
            return True
        except:
            return False

    def insert(self,key,value):
        try:
            self._data.insert(key,value)
            return True
        except:
            return False

    def printall(self):
        for i in self:
            print(i)



if __name__ == '__main__':
    array=MyArray(5)
    array.insert(3,4)
    array.insert(0, 4)
    array.insert(1, 5)
    array.insert(3, 9)
    array.insert(3, 10)
    # assert array.insert(0, 100) is False
    # assert array.delete(4) is True
    array.printall()
    # assert len(array) == 5
    assert array.find(1) == 5
