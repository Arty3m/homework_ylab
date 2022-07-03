import pygame
import random
import numpy as np
from time import sleep


def draw_board(board: np.ndarray) -> None:
    """Отрисовывает игровое поле"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE + (col + 1) * GAP
            y = row * CELL_SIZE + (row + 1) * GAP
            if board[row, col] == VARIANTS_MOVE[0]:
                move = 0
            elif board[row, col] == VARIANTS_MOVE[1]:
                move = 1
            else:
                move = -1

            draw_cell(x, y, move)


def draw_cell(x: int, y: int, move: int) -> None:
    """Отрисовывает отдельную клетку"""
    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
    if move == 1:
        pygame.draw.line(screen, BLACK, (x + GAP, y + GAP), (x + (CELL_SIZE - GAP), y + (CELL_SIZE - GAP)), 5)
        pygame.draw.line(screen, BLACK, (x + (CELL_SIZE - GAP), y + GAP), (x + GAP, y + (CELL_SIZE - GAP)), 5)
    elif move == 0:
        pygame.draw.circle(screen, RED, (x + (CELL_SIZE // 2), y + (CELL_SIZE // 2)), (CELL_SIZE // 2) - (GAP // 2), 5)


def player_turn(board: np.ndarray, symbol: str, move_count: int, avail_cells: list[int]) -> tuple[int, tuple]:
    """Выполняет ход игрока"""
    row, col = human_select() if symbol == HUMAN_SYMBOL else bot_select()
    if board[row, col] not in VARIANTS_MOVE:
        board[row, col] = symbol
        avail_cells.remove(row * 10 + col)
        is_over = game_over(board, symbol, row, col)
        move_count += 1
        return move_count, is_over

    return move_count, game_info


def human_select() -> tuple[int, int]:
    """Возвращает номер строки и столбца выбранной клетки"""
    x_pos, y_pos = pygame.mouse.get_pos()
    return y_pos // (CELL_SIZE + GAP), x_pos // (CELL_SIZE + GAP)


def bot_select() -> tuple[int, int]:
    """Рандомно выбирает свободную клетку и возвращает номер ее строки и столбца"""
    sleep(0.4)
    return get_row_col(random.choice(available_cells))


def get_row_col(num: int) -> tuple[int, int]:
    """Возвращает строку и столбец, которым соответствует число num"""
    return num // 10, num % 10


def game_over(board: np.ndarray, symbol: str, row: int, col: int) -> tuple[bool, str]:
    """Делает проверки на окончание игры"""
    for_win = ''.join(5 * [symbol])
    check_1 = ''.join(board[row, :])
    check_2 = ''.join(board[:, col])
    check_3 = ''.join(np.diag(board, col - row))
    check_4 = ''.join(np.diag(np.fliplr(board), (BOARD_SIZE - 1) - (row + col)))

    if any((for_win in check_1, for_win in check_2, for_win in check_3, for_win in check_4)):
        return True, f'{"Вы проиграли!" if symbol == HUMAN_SYMBOL else "Вы победили!"}'

    if '*' not in board:
        return True, f'"Ничья. Ходов не осталось."'

    return False, 'Удачи!'


def result_screen(message: str, timeout: float = 1.5) -> None:
    """Выводит на финальный экран сообщение message"""
    sleep(timeout)
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, (180, 0, 0))
    place = text.get_rect(center=(350, 300))
    screen.blit(text, place)
    pygame.display.update()
    sleep(timeout)


WIDTH = 705
HEIGHT = 705
BOARD_SIZE = 10
CELL_SIZE = 65
GAP = 5
VARIANTS_MOVE = ('O', 'X')
HUMAN_SYMBOL, BOT_SYMBOL = VARIANTS_MOVE

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

game_board = np.full((BOARD_SIZE, BOARD_SIZE), '*')
available_cells = [i for i in range(BOARD_SIZE ** 2)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Обратные Крестики-Нолики by Kolbun Artyom')

move_counter = 0
game_info = [False, 'Удачи!']

running = True
while running:
    draw_board(game_board)
    move_symbol = VARIANTS_MOVE[move_counter % 2]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            result_screen(game_info[1], timeout=0.7)
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and move_symbol == HUMAN_SYMBOL:
            move_counter, game_info = player_turn(game_board, move_symbol, move_counter, available_cells)
        elif move_symbol == BOT_SYMBOL:
            move_counter, game_info = player_turn(game_board, move_symbol, move_counter, available_cells)

        if game_info[0]:
            running = False

    pygame.display.update()
else:
    draw_board(game_board)
    pygame.display.update()
    result_screen(game_info[1])
    pygame.quit()
