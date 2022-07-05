import math

maxsize = float('inf')


def copyToFinal(curr_path: list) -> None:
    """Копирует путь в final_path"""
    global final_path
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]


def first_min(adj_matrix: list[list], i: int) -> float:
    """Находит первый минимум в i строке"""
    min_val = maxsize
    for k in range(N):
        if adj_matrix[i][k] < min_val and i != k:
            min_val = adj_matrix[i][k]

    return min_val


def second_min(adj_matrix: list[list], i: int) -> float:
    """Находит второй минимум в строке i"""
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj_matrix[i][j] <= first:
            second = first
            first = adj_matrix[i][j]

        elif (adj_matrix[i][j] <= second and
              adj_matrix[i][j] != first):
            second = adj_matrix[i][j]

    return second


def TSPRec(matrix: list, n: int, curr_bound: float, curr_weight: float, level: int, curr_path: list,
           visited: list):
    """Находит наименьшую стоимость маршрута"""
    global final_cost

    if level == n:
        if matrix[curr_path[level - 1]][curr_path[0]] != 0:
            curr_res = curr_weight + matrix[curr_path[level - 1]][curr_path[0]]

            if curr_res < final_cost:
                copyToFinal(curr_path)
                final_cost = curr_res

        return

    for i in range(n):
        if (matrix[curr_path[level - 1]][i] != 0 and
                visited[i] is False):
            temp = curr_bound
            curr_weight += matrix[curr_path[level - 1]][i]

            if level == 1:
                curr_bound -= ((first_min(matrix, curr_path[level - 1]) +
                                first_min(matrix, i)) / 2)
            else:
                curr_bound -= ((second_min(matrix, curr_path[level - 1]) +
                                first_min(matrix, i)) / 2)

            if curr_bound + curr_weight < final_cost:
                curr_path[level] = i
                visited[i] = True
                TSPRec(matrix, n, curr_bound, curr_weight, level + 1, curr_path, visited)

            curr_weight -= matrix[curr_path[level - 1]][i]
            curr_bound = temp
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def TSP(matrix: list, n: int) -> None:
    curr_bound = 0
    curr_path = [-1] * (n + 1)
    visited = [False] * n

    for i in range(n):
        curr_bound += (first_min(matrix, i) +
                       second_min(matrix, i))
    curr_bound = math.ceil(curr_bound / 2)
    visited[0] = True
    curr_path[0] = 0
    TSPRec(matrix, n, curr_bound, 0, 1, curr_path, visited)


def distance(point_1: int, point_2: int) -> float:
    """Вычисляет расстояние между двумя точками"""
    return math.sqrt((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2)


def make_matrix(p: list) -> list[list]:
    """Создаёт матрицу смежности"""
    result = []
    for i in range(len(p)):
        row = []
        for j in range(len(p)):
            row.append(distance(p[i], p[j]))
        result.append(row)
    return result


def print_result(p: list, matrix: list, fin_path: list, fin_cost: float) -> None:
    """Выводит конечный ответ"""
    dist = 0
    for i in range(N + 1):
        if i == 0:
            print(f'{p[fin_path[i]]} -> ', end='')
        elif i != N:
            dist += matrix[fin_path[i]][fin_path[i - 1]]
            print(f'{p[fin_path[i]]}[{dist}] ->', end=' ')
        else:
            print(f'{p[fin_path[i]]}[{fin_cost}] = {fin_cost}', end=' ')


if __name__ == "__main__":
    # points = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]
    points = [(0, 2), (2, 5), (5, 2), (6, 6), (5, 5), (8, 3)]
    # points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    # points = [(0, 2), (2, 5), (5, 2), (6, 6), (20, 60), (8, 3)]

    # points = [(0, 1), (1, 4), (4, 1), (5, 5), (7, 2)]
    adjacent_matrix = make_matrix(points)

    N = len(adjacent_matrix)

    final_path = [None] * (N + 1)
    final_cost = maxsize

    TSP(adjacent_matrix, N)

    print_result(points, adjacent_matrix, final_path, final_cost)
