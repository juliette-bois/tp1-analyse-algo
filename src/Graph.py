# Kruskal's algorithm in Python
from time import sleep


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    # Search function
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def get_edge(self, u, v):
        for edge in self.graph:
            if (edge[0] == u and edge[1] == v) or (edge[0] == v and edge[1] == u):
                return edge
        return None

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    #  Applying Kruskal algorithm
    def kruskal_algo(self, sortedResult=False):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        if sortedResult is True:
            return self.sort_kruskal_result(result)
        return result

    def get_node(self, nodes, node, first):
        for i in range(len(nodes)):
            if nodes[i][1] is False and (nodes[i][0][0] == node or (first is False and nodes[i][0][1] == node)):
                nodes[i][1] = True
                return nodes[i][0]
        return None

    def sort_kruskal_result(self, result):
        sortedResult = []
        nodeEdgeNumber = [0] * self.V
        for node in result:
            nodeEdgeNumber[node[0]] += 1
            nodeEdgeNumber[node[1]] += 1
        nodeEdgeNumber = [[i, nodeEdgeNumber[i]] for i in range(self.V)]
        nodeEdgeNumber.sort(key=lambda node: node[1], reverse=True)
        nodes = [[node, False] for node in result]
        first = True
        for n, nodeNumber in nodeEdgeNumber:
            node = self.get_node(nodes, n, first)
            first = False
            while not node is None:
                sortedResult.append(node)
                node = self.get_node(nodes, n, False)
        return sortedResult

    def rmvEdge(self, u, v, graph):
        for index, key in enumerate(graph[u]):
            if key == v:
                graph[u].pop(index)
        for index, key in enumerate(graph[v]):
            if key == u:
                graph[v].pop(index)

    def DFSCount(self, v, visited, graph):
        count = 1
        visited[v] = True
        for i in graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited, graph)
        return count

    def isValidNextEdge(self, u, v, graph):
        if len(graph[u]) == 1:
            return True
        else:
            visited = [False] * (self.V)
            count1 = self.DFSCount(u, visited, graph)

            self.rmvEdge(u, v, graph)
            visited = [False] * self.V
            count2 = self.DFSCount(u, visited, graph)

            graph[u].append(v)
            graph[v].append(u)

            return False if count1 > count2 else True

    def _eulerian_cycle(self, u, graph):
        cycle = [u]
        for v in graph[u]:
            if self.isValidNextEdge(u, v, graph):
                cycle.append(v)
                self.rmvEdge(u, v, graph)
                self._eulerian_cycle(v, graph)
        return cycle

    def get_eulerian_cycle(self):
        graph = [[] for x in range(self.V)]
        for u, v, w in self.graph:
            graph[u].append(v)
            graph[v].append(u)
        visited = [False] * self.V
        visited[0] = True
        cycle = self._eulerian_cycle(0, graph)
        while all(visited) is False:
            for i in range(len(graph)):
                if len(graph[i]) > 0 and visited[i] is False:
                    cycle += self._eulerian_cycle(i, graph)
                    for j in cycle:
                        visited[j] = True
                    break
        return cycle