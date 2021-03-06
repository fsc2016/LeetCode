'''
实现一个 Trie (前缀树)，包含 insert, search, 和 startsWith 这三个操作。

示例:

Trie trie = new Trie();

trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");
trie.search("app");     //
'''
'''
N叉树 使用字典实现
'''
class Trie:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.lookup = {}


    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        tree = self.lookup
        for w in word:
            if w not in tree:
                tree[w] = {}
            tree = tree[w]
        tree['#'] = '#'


    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        tree = self.lookup
        for w in word:
            if w not in tree:
                return False
            tree = tree[w]
        if '#' in tree:
            return True
        return False



    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        tree = self.lookup
        for w in prefix:
            if w not in tree:
                return False
            tree = tree[w]
        return True