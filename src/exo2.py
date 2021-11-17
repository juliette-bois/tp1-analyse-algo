import math
import time


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def minDelivery(base, S, v):
    if len(S) == 0:
        return [dist(base[0], base[1], v[0], v[1]), [v[2]]]
    data = []
    for x in range(len(S)):
        xMinDelivery = minDelivery(base, [S[y] for y in range(len(S)) if y != x], S[x])
        data.append([xMinDelivery[0] + dist(S[x][0], S[x][1], v[0], v[1]), [v[2]] + xMinDelivery[1]])
    return min(data, key=lambda k: k[0])


def main(filename):
    cities = []
    with open(filename, 'r', encoding='UTF-8') as file:
        index = 0
        while line := file.readline().rstrip():
            x, y = line.split(' ')
            cities.append([int(x), int(y), index])
            index += 1
    Ss = []
    for x in range(1, len(cities)):
        Ss.append([cities[y] for y in range(1, len(cities)) if y != x])
    cycles = []
    for x in range(len(Ss)):
        xMinDelivery = minDelivery(cities[0], Ss[x], cities[x + 1])
        cycles.append([xMinDelivery[0] + dist(cities[0][0], cities[0][1], cities[x + 1][0], cities[x + 1][1]), xMinDelivery[1]])
    minimum = min(cycles, key=lambda k: k[0])
    print("La distance minimale est :", minimum[0])
    print("Un cycle possible est :", [0] + minimum[1] + [0])


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        exit(1)

    start_time = time.time()
    main(sys.argv[1])
    print("--- %s seconds ---" % (time.time() - start_time))
