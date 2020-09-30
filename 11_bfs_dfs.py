from collections import deque

class Graph:
    def __init__(self,v):
        # 图的顶点数
        self.num_v = v
        # 使用邻接表来存储图
        self.adj = [[] for _ in range(v)]

    def add_edge(self,s,t):
        self.adj[s].append(t)
        self.adj[t].append(s)

    def _generate_path(self, s, t, prev):
        '''
        打印路径
        :param s:
        :param t:
        :param prev:
        :return:
        '''
        if prev[t] or s != t:
            yield from self._generate_path(s, prev[t], prev)
        yield str(t)

    def bfs(self,s,t):
        '''
        广度优先
        :param s: 起始节点
        :param t: 终止节点
        :return:
        visited 是用来记录已经被访问的顶点，用来避免顶点被重复访问。如果顶点 q 被访问，那相应的 visited[q]会被设置为 true。
        queue 是一个队列，用来存储已经被访问、但相连的顶点还没有被访问的顶点
        prev 用来记录搜索路径。当我们从顶点 s 开始，广度优先搜索到顶点 t 后，prev 数组中存储的就是搜索的路径
        '''
        if s == t : return

        visited = [False] * self.num_v
        visited[s] = True
        prev = [None] * self.num_v
        q = deque()
        q.append(s)

        while q :
            w = q.popleft()
            # 从邻接表中查询
            for neighbour in self.adj[w]:
                # 没访问过就访问这个节点，并且加入路径
                if not visited[neighbour]:
                    prev[neighbour] = w
                    if neighbour == t:
                        print("->".join(self._generate_path(s, t, prev)))
                        return
                    # 当前节点不是，就把节点加入已访问节点列表
                    visited[neighbour] = True
                    q.append(neighbour)


    def dfs(self,s,t):
        '''
        深度优先
        采用回溯算法的思想，采用递归来实现
        :param s: 起始节点
        :param t: 终止节点
        :return:
        '''
        found = False
        visited = [False] * self.num_v
        prev = [None] * self.num_v

        def _dfs(from_vertex):
            nonlocal found
            if found :return
            # 当前节点不是终结点，就不停往下一层探寻
            visited[from_vertex] = True
            if from_vertex == t:
                found = True
                return

            for neighbour in self.adj[from_vertex]:
                if not visited[neighbour]:
                    prev[neighbour] = from_vertex
                    _dfs(neighbour)

        _dfs(s)
        print("->".join(self._generate_path(s, t, prev)))


if __name__ == "__main__":
    graph = Graph(8)

    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(4, 6)
    graph.add_edge(5, 7)
    graph.add_edge(6, 7)

    graph.bfs(0, 7)
    graph.dfs(0, 7)