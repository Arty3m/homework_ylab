import itertools
import math


def distance(point_1: int, point_2: int) -> float:
    """Вычисляет расстояние между двумя точками"""
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def print_result(r: list) -> None:
    """Выводит конечный ответ"""
    value = r[0]
    tup = r[1]
    for i in range(0, len(tup), 2):
        if i == 0:
            print(f'{tup[i]} -> ', end='')
        elif i == len(tup) - 1:
            print(f'{tup[i]}[{tup[i - 1]}] = {value}')
        else:
            print(f'{tup[i]}[{tup[i - 1]}] -> ', end='')


def get_shortest_route(locations: list[tuple]) -> None:
    """Находит кратчайший путь"""
    start_point = locations[0]

    permutations = []
    for item in [x for x in itertools.permutations(locations[1:])]:
        permutations.append([start_point] + list(item) + [start_point])
    route_size = len(permutations[0])
    result = []
    for i in range(len(permutations)):
        total_distance = 0
        tmp_route = ()
        for j in range(route_size):
            if j != route_size - 1:
                total_distance += distance(permutations[i][j], permutations[i][j + 1])
                tmp_route += (permutations[i][j], total_distance)
            else:
                tmp_route += (start_point,)
        result.append([total_distance, tmp_route])

    print_result(sorted(result)[0])


if __name__ == '__main__':
    points = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]
    # points = [(0, 2), (2, 5), (5, 2), (6, 6), (5, 5), (8, 3)]
    # points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    # points = [(0, 1), (1, 4), (4, 1), (5, 5), (7, 2)]

    get_shortest_route(points)

