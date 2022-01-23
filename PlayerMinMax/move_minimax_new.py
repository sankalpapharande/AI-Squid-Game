from Grid import Grid
from Utils import *
import sys
import random
from helper_functions import *
ALPHA = -sys.maxsize
BETA = sys.maxsize
MAX_DEPTH = 3


def get_continuous_space(grid, current_pos):
    count = 0
    x, y = current_pos
    x_search = x
    while x_search >= 0:
        if grid.getCellValue((x_search, y)) == 0:
            count = count + 1
            x_search = x_search - 1
        else:
            break
    x_search = x
    while x_search <= 6:
        if grid.getCellValue((x_search, y)) == 0:
            count = count + 1
            x_search = x_search + 1
        else:
            break

    y_search = y
    while y_search >= 0:
        if grid.getCellValue((x, y_search)) == 0:
            count = count + 1
            y_search = y_search - 1
        else:
            break

    y_search = y
    while y_search <= 6:
        if grid.getCellValue((x, y_search)) == 0:
            count = count + 1
            y_search = y_search + 1
        else:
            break
    return count + 0.5


def get_emptiness_around_the_move(grid, current_pos):
    white_cells = 0
    empty_space = get_continuous_space(grid, current_pos)
    for x in range(max(current_pos[0] - 2, 0), min(current_pos[0] + 2, 6), 1):
        for y in range(max(current_pos[1] - 2, 0), min(current_pos[1] + 2, 6), 1):
            if grid.getCellValue((x, y)) == 0:
                white_cells = white_cells + 1
    return white_cells + empty_space


def move_heuristic(player_num: int, grid: Grid):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    grid_clone = grid.clone()
    position = grid.find(player_num)
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    for i in range(len(my_new_available_moves)):
        board_v = board_value(grid_clone, my_new_available_moves[i], opponent_pos)
        moves_dict[my_new_available_moves[i]] = board_v
    max_position = list(sorted(moves_dict, key=moves_dict.get, reverse=True))
    return max_position


def diagonal(pos1, pos2):
    (x1,y1) = pos1
    (x2, y2) = pos2
    if x1 != x2 and y1 != y2:
        return True
    else:
        return False


def find_candidate_moves(grid, my_position, opponent_pos, player_neighbours, opponent_neighbours):
    moves_dict = {}
    for i in range(len(player_neighbours)):
        board_v = white_cell_move_heuristic(grid, my_position, opponent_pos, player_neighbours[i], len(player_neighbours),
                                            len(opponent_neighbours))
        moves_dict[player_neighbours[i]] = board_v
    max_position = list(sorted(moves_dict, key=moves_dict.get, reverse=True))
    return max_position


def get_opponent_neighbours(grid: Grid, player_num: int):
    opponent_pos = grid.find(3-player_num)
    opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
    return opponent_neighbours


# heuristic given to us by them
def white_cell_move_heuristic(grid, my_position, opponent_pos, current_move, player_neighbours, opponent_neighbours):
    emptiness = get_emptiness_around_the_move(grid, current_move)
    if diagonal(my_position, current_move):
        emptiness = 1.5 * emptiness
    # print("Move:{}, emptiness:{}".format(current_move, emptiness))
    if 47 - len(grid.getAvailableCells()) < 15:
        # Chasing the opponent
        d = manhattan_distance(my_position, opponent_pos)
        return 2*player_neighbours - opponent_neighbours + 2*emptiness - 2*d
    else:
        return 2*player_neighbours - opponent_neighbours + 2*emptiness


# motive: trap the opponent based on some heuristic
def minimax_move(grid: Grid, depth, player, isMax,  alpha, beta, current_move: tuple):
    '''
    BASE CASES
    '''
    opp_neighbours = get_opponent_neighbours(grid, player)
    player_neighbours = grid.get_neighbors(grid.find(player), True)
    opponent_pos = grid.find(3 - player)
    player_pos = grid.find(player)
    if depth > 3:
        return white_cell_move_heuristic(grid, player_pos, opponent_pos, current_move, len(player_neighbours),
                                         len(opp_neighbours))

    # if we win
    if len(opp_neighbours) == 0:
        return sys.maxsize

    # if opponent wins
    if len(player_neighbours) == 0:
        return -sys.maxsize

    # good_moves_for_player = move_heuristic(player, grid)
    good_moves_for_player = find_candidate_moves(grid, player_pos, opponent_pos, player_neighbours, opp_neighbours)
    if isMax == 1:
        # we move
        best_value = -sys.maxsize
        previous_player_position = grid.find(player)
        for i in good_moves_for_player:
            grid.move(i, player)
            best_value = max(best_value, minimax_move(grid, depth+1, player, 0, alpha, beta, (0,0)))
            alpha = max(alpha, best_value)
            grid.move(previous_player_position, player)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best_value

    elif isMax == 0:
        # opponent puts trap
        best_value = sys.maxsize
        for j in good_moves_for_player:
            hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(3 - player), j) - 1)
            if hit_probability > 0.9 or depth > MAX_DEPTH-1:
                expectation = minimax_move(grid, depth + 1, player, 1, alpha, beta, (0, 0))
            else:
                expectation = minimax_move(grid, depth, player, 2, alpha, beta, j)
            best_value = min(expectation, best_value)
            beta = min(beta, best_value)
            # Alpha Beta Pruning
            if beta <= alpha:
                break
        return best_value

    else:
        # chance node
        best_value = sys.maxsize
        current_trap_position = current_move
        hit_probability = 1 - 0.05 * (manhattan_distance(grid.find(3-player), current_trap_position) - 1)
        missing_probability = ((1 - hit_probability) / len(grid.get_neighbors(current_trap_position)))
        expectation = 0
        all_possible_positions = grid.get_neighbors(current_trap_position, only_available=True)
        all_possible_positions.append(current_trap_position)
        for j in range(len(all_possible_positions)):
            grid.setCellValue(all_possible_positions[j], -1)
            if current_trap_position == all_possible_positions[j]:
                recursion_value = minimax_move(grid, depth + 1, player, 1, alpha, beta, (0, 0))
                expectation = expectation + hit_probability * recursion_value
            else:
                recursion_value = minimax_move(grid, depth + 1, player, 1, alpha, beta, (0, 0))
                expectation = expectation + missing_probability * recursion_value

            grid.setCellValue(all_possible_positions[j], 0)

            best_value = min(expectation, best_value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return expectation


def find_move(grid, player):
    my_neighbours = grid.get_neighbors(grid.find(player), True)
    grid_clone = grid.clone()
    good_move = -sys.maxsize
    good_move_pos = random.choice(my_neighbours)
    for i in range(len(my_neighbours)):
        grid_clone.move(my_neighbours[i], player)
        move_value = minimax_move(grid_clone, 0, player, 1, ALPHA, BETA, (0,0))
        grid_clone.setCellValue(my_neighbours[i], 0)
        if good_move < move_value:
            good_move = move_value
            good_move_pos = my_neighbours[i]
    return good_move_pos

