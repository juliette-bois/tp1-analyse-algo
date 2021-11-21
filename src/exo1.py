import math

from Graph import Graph
from Tree import Tree


def compute_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def get_child(graph, node, used):
    for i in range(len(graph)):
        if used[i] == False and (graph[i][0] == node or graph[i][1] == node):
            used[i] = True
            return graph[i]
    return None


def main(filename):
    cities = []
    with open(filename) as file:
        while line := file.readline().rstrip():
            x, y = line.split(' ')
            cities.append([int(x), int(y)])

    graph = Graph(len(cities))
    index = 0
    for city in cities:
        for i in range(index + 1, len(cities), 1):
            distance = compute_distance(city[0], city[1], cities[i][0], cities[i][1])
            graph.add_edge(index, i, distance)
        index += 1

    results = graph.kruskal_algo()
    used = [False] * len(results)
    useCount = 1
    used[0] = True
    tree = Tree()
    tree.addNode(results[0][0], results[0][1], results[0][2])
    current = results[0][1]
    lasts = [results[0][0]]
    while useCount < len(results):
        child = get_child(results, current, used)
        if child is None:
            current = lasts.pop()
        else:
            useCount += 1
            lasts.append(current)
            if child[0] == current:
                tree.addNode(child[0], child[1], child[2])
                current = child[1]
            else:
                tree.addNode(child[1], child[0], child[2])
                current = child[0]
    dfsResult = tree.dfs()
    cycle = []
    i = 0
    foundZero = False
    while len(cycle) < len(dfsResult):
        if (foundZero is True or dfsResult[i] == 0):
            foundZero = True
            cycle.append(dfsResult[i])
        i = (i + 1) % len(dfsResult)
    cycle.append(cycle[0])
    weight = 0
    for i in range(len(cycle) - 1):
        weight += graph.get_edge(cycle[i], cycle[i + 1])[2]
    print("La distance minimale est : ", weight)
    print("Un cycle possible est : ", cycle)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: {} file".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
