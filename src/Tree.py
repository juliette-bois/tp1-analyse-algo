import math

from Simplex import Simplex


class Tree:
    def __init__(self):
        self.root = None
        self.nodes = []

    def addNode(self, parent, child, weight):
        if self.root is None:
            self.root = TreeNode(parent, None)
            childNode = TreeNode(child, self.root)
            self.nodes.append([parent, self.root])
            self.nodes.append([child, childNode])
            self.root.addChild(childNode, weight)
        else:
            found = False
            i = 0
            while found == False and i < len(self.nodes):
                if self.nodes[i][0] == parent:
                    found = True
                else:
                    i += 1
            if found != False:
                childNode = TreeNode(child, self.nodes[i][1])
                self.nodes.append([child, childNode])
                self.nodes[i][1].addChild(childNode, weight)

    def dfs(self):
        return self.dfs_recursive(self.root, [])

    def dfs_recursive(self, start, cycle):
        cycle.append(start.number)
        for child in start.children:
            self.dfs_recursive(child[0], cycle)
        return cycle

    def computeMinCouplage(self, graph):
        nodes = list(filter(lambda node: len(node[1].children) % 2 != 0, self.nodes))
        nodeTransform = []
        for i, node in nodes:
            try:
                i = nodeTransform.index(nodes)
            except ValueError:
                nodeTransform.append(i)
        result = [['0.0' for col in range(len(nodes))] for row in range(len(nodes))]
        for i, node in nodes:
            for child, weight in node.children:
                if child.number in nodeTransform:
                    i_index = nodeTransform.index(i)
                    child_index = nodeTransform.index(child.number)
                    result[i_index][child_index] = str(weight)
                    result[child_index][i_index] = str(weight)
        with open('input_graph', 'w+', encoding='UTF-8') as file:
            file.write(str(len(nodes)) + '\n')
            for line in result:
                file.write(' '.join(line) + '\n')
        Simplex.computeFile('input_graph', 'output_matching')
        with open('output_matching', 'r+', encoding='UTF-8') as file:
            n = float(file.readline().rstrip())
            while line := file.readline().rstrip():
                x, y = line.split(' ')
                edge = graph.get_edge(nodeTransform[int(x)], nodeTransform[int(y)])
                self.addNode(edge[0], edge[1], edge[2])


def compute_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


class TreeNode:
    def __init__(self, nodeNumber, parent):
        self.number = nodeNumber
        self.parent = parent
        self.children = []

    def addChild(self, child, weight):
        self.children.append([child, weight])
