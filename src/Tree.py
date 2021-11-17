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


class TreeNode:
    def __init__(self, nodeNumber, parent):
        self.number = nodeNumber
        self.parent = parent
        self.children = []

    def addChild(self, child, weight):
        self.children.append([child, weight])
