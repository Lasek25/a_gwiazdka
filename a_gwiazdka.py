from map import Map
from point import *
from numpy import *

# MAP_SIZE -> size of map (length and height)
MAP_SIZE = 20
MS = MAP_SIZE-1


def calc_distance(current, cost, end=Point(MS, MS), step_value=1):
    return round((cost * step_value + pow(pow((end.y - current.y), 2) + pow((end.x - current.x), 2), 0.5)), 2)


def load_map(sciezka):
    plik = open(sciezka)
    mapa = []
    for line in plik:
        line = line.split()
        mapa.append(line)
    plik.close()
    size_map = mapa[0].__len__()
    tab = zeros((size_map, size_map), double)
    for i in range(size_map):
        for j in range(size_map):
            tab[i][j] = mapa[i][j]
    return tab


def get_distance(mapa, current, position_list, value_list):
    # first parametr(current.x) -> row; second parametr(current.y) -> column
    if 0 <= current.x < MAP_SIZE and 0 <= current.y < MAP_SIZE and mapa.value_map[MS - current.x][current.y] != -5:
        range_list = (current.x+1, current.x-1, current.y-1, current.y+1)
        for i in range_list:
            if 0 <= i < MAP_SIZE:
                if (i == range_list[2] or i == range_list[3]) and mapa.value_map[MS - current.x][i] == 0 and \
                        mapa.closed_map[MS - current.x][i] == 0 and mapa.cost_map[MS - current.x][i] == 0:
                    mapa.cost_map[MS - current.x][i] = mapa.cost_map[MS - current.x][current.y] + 1
                    point = Point(i, current.x)
                    # MS-current.x -> point(0,0) in left down corner
                    distance = calc_distance(point, mapa.cost_map[MS - current.x][i])
                    mapa.value_map[MS - current.x][i] = distance
                    position_list.append(point)
                    value_list.append(distance)
                    if i == range_list[2]:
                        mapa.parents_map[MS - current.x][i] = 2
                    if i == range_list[3]:
                        mapa.parents_map[MS - current.x][i] = 4
                    if mapa.cost_map[MS - current.x][i] == 0:
                        mapa.cost_map[MS - current.x][i] = mapa.cost_map[MS-current.x][current.y]
                if (i == range_list[0] or i == range_list[1]) and mapa.value_map[MS - i][current.y] == 0 and \
                        mapa.closed_map[MS - i][current.y] == 0 and mapa.cost_map[MS - i][current.y] == 0:
                    mapa.cost_map[MS - i][current.y] = mapa.cost_map[MS - current.x][current.y] + 1
                    point = Point(current.y, i)
                    # MS-i -> point(0,0) in left down corner
                    distance = calc_distance(point, mapa.cost_map[MS - i][current.y])
                    mapa.value_map[MS - i][current.y] = distance
                    position_list.append(point)
                    value_list.append(distance)
                    if i == range_list[0]:
                        mapa.parents_map[MS - i][current.y] = 3
                    if i == range_list[1]:
                        mapa.parents_map[MS - i][current.y] = 1
                    if mapa.cost_map[MS - i][current.y] == 0:
                        mapa.cost_map[MS - i][current.y] = mapa.cost_map[MS-current.x][current.y]
    return mapa


def find_the_smallest(mapa, position_list, value_list):
    smallest = 1000
    point = Point(0, 0)
    tmp = None
    for i in range(len(value_list)):
        if value_list[i] <= smallest:
            smallest = value_list[i]
            point = position_list[i]
            tmp = i
    if tmp is not None:
        mapa.closed_map[MS-point.x][point.y] = 1
        value_list.pop(tmp)
        position_list.pop(tmp)
    return point


def print_road(mapa):
    mapa.road_map[0][MS] = 3
    dest = mapa.parents_map[0][MS]
    current = Point(MS, 0)
    while mapa.road_map[MS][0] != 3:
        # from destination to start (from right up corner to left down corner of the map)
        # parents_map values: 1 up, 3 down, 4 left, 2 right
        if dest == 1:
            current.x -= 1
            dest = mapa.parents_map[current.x][current.y]
            mapa.road_map[current.x][current.y] = 3
        elif dest == 3:
            current.x += 1
            dest = mapa.parents_map[current.x][current.y]
            mapa.road_map[current.x][current.y] = 3
        elif dest == 4:
            current.y -= 1
            dest = mapa.parents_map[current.x][current.y]
            mapa.road_map[current.x][current.y] = 3
        elif dest == 2:
            current.y += 1
            dest = mapa.parents_map[current.x][current.y]
            mapa.road_map[current.x][current.y] = 3
    return mapa


def way(mapa):
    mapa.change_five()
    mapa.closed_map[MS][0] = 1
    current = Point(0, 0)
    position_list = []
    value_list = []
    current = get_distance(mapa, current, position_list, value_list)
    while mapa.closed_map[0][MS] != 1:
        current = find_the_smallest(mapa, position_list, value_list)
        get_distance(mapa, current, position_list, value_list)
        if value_list.__len__() == 0:
            print("Dotarcie do celu nie jest mozliwe")
            return mapa
    print_road(mapa)
    return mapa


a = load_map('C:\\Users\\Krzysztof\\Downloads\\grid.txt')
b = load_map('C:\\Users\\Krzysztof\\Downloads\\grid.txt')
c = load_map('C:\\Users\\Krzysztof\\Downloads\\grid.txt')
d = load_map('C:\\Users\\Krzysztof\\Downloads\\grid.txt')
e = load_map('C:\\Users\\Krzysztof\\Downloads\\grid.txt')
abc = Map(a, b, c, d, e)
abc = way(abc)
plik = open('C:\\Users\\Krzysztof\\Downloads\\new_grid.txt', 'w')
plik.write(str(abc.road_map))
plik.close()
print("otwarta\n", abc.value_map, "\nzamknieta\n", abc.closed_map, "\nrodzicow\n", abc.parents_map, "\nkosztow\n", abc.cost_map, "\ndroga\n", abc.road_map)