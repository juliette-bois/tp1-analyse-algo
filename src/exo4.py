import math
from pulp import *
import time


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def findNext(routes, current):
    for c in routes:
        if c[2] == False and c[0] == current:
            return c[1]


def main(filename):
    cities = []
    with open(filename, 'r', encoding='UTF-8') as file:
        while line := file.readline().rstrip():
            x, y = line.split(' ')
            cities.append([int(x), int(y)])
    prob = LpProblem('problem', LpMinimize)
    x = []
    d = []
    for i in range(len(cities)):
        x.append([])
        d.append([])
        for j in range(len(cities)):
            x[i].append(LpVariable('x_' + str(i) + '_' + str(j), cat=LpBinary))
            d[i].append(dist(cities[i][0], cities[i][1], cities[j][0], cities[j][1]))

    prob += (lpSum([(d[i][j] * x[i][j]) for i in range(len(cities)) for j in range(len(cities)) if i != j]))

    for i in range(len(cities)):
        prob += lpSum([(x[i][j]) for j in range(len(cities)) if i != j]) == 1

    for j in range(len(cities)):
        prob += lpSum([(x[i][j]) for i in range(len(cities)) if i != j]) == 1

    Qs = allcombinations(range(len(cities)), len(cities) - 1)
    for q in Qs:
        if len(q) >= 2:
            prob += lpSum([(x[i][j]) for i in q for j in q if i != j]) <= (len(q) - 1)
    prob.solve()
    routes = []
    for v in prob.variables():
        if v.varValue:
            _, f, t = v.name.split('_')
            routes.append([int(f), int(t), False])
    cycle = [0]
    i = 1
    current = 0
    while i <= len(routes):
        current = findNext(routes, current)
        cycle.append(current)
        i += 1
    print('La distance minimale est :', value(prob.objective))
    print('Un cycle possible est :', cycle)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        exit(1)

    start_time = time.time()
    main(sys.argv[1])
    print("--- %s seconds ---" % (time.time() - start_time))
