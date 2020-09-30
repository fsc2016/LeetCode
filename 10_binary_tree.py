class TreeNode():
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None

def pre_order(rootnode):
    '''
    前序遍历
    :param rootnode:
    :return:
    '''
    if rootnode:
        yield rootnode.value
        yield from pre_order(rootnode.left)
        yield from pre_order(rootnode.right)


def in_order(rootnode):
    '''
    中序遍历
    :param rootnode:
    :return:
    '''
    if rootnode:
        yield from pre_order(rootnode.left)
        yield rootnode.value
        yield from pre_order(rootnode.right)

def post_order(rootnode):
    '''
    后序遍历
    :param rootnode:
    :return:
    '''
    if rootnode:
        yield from pre_order(rootnode.left)
        yield from pre_order(rootnode.right)
        yield rootnode.value


if __name__ == '__main__':
    singer = TreeNode("Taylor Swift")

    genre_country = TreeNode("Country")
    genre_pop = TreeNode("Pop")

    album_fearless = TreeNode("Fearless")
    album_red = TreeNode("Red")
    album_1989 = TreeNode("1989")
    album_reputation = TreeNode("Reputation")

    song_ls = TreeNode("Love Story")
    song_wh = TreeNode("White Horse")
    song_wanegbt = TreeNode("We Are Never Ever Getting Back Together")
    song_ikywt = TreeNode("I Knew You Were Trouble")
    song_sio = TreeNode("Shake It Off")
    song_bb = TreeNode("Bad Blood")
    song_lwymmd = TreeNode("Look What You Made Me Do")
    song_g = TreeNode("Gorgeous")

    singer.left, singer.right = genre_country, genre_pop
    genre_country.left, genre_country.right = album_fearless, album_red
    genre_pop.left, genre_pop.right = album_1989, album_reputation
    album_fearless.left, album_fearless.right = song_ls, song_wh
    album_red.left, album_red.right = song_wanegbt, song_ikywt
    album_1989.left, album_1989.right = song_sio, song_bb
    album_reputation.left, album_reputation.right = song_lwymmd, song_g

    print(list(pre_order(singer)))
    print(list(in_order(singer)))
    print(list(post_order(singer)))

