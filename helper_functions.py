from Grid import Grid
from Utils import *


def get_opponent_position(grid: Grid, player_num: int):
    opponent_no = 3 - player_num
    opponent_pos = grid.find(opponent_no)
    return opponent_pos


def get_opponent_neighbours(grid: Grid, player_num: int):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    opponent_neighbours = grid.get_neighbors(opponent_pos, only_available=True)
    return opponent_neighbours


def trap_heuristic(player_num: int, grid: Grid):
    opponent_neighbours = get_opponent_neighbours(grid, player_num=player_num)
    moves_dict = {}
    grid_clone = grid.clone()
    opponent_pos = get_opponent_position(grid_clone, player_num)
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            grid_clone.trap(opponent_neighbours[i])
            available_opponent_moves = grid_clone.get_neighbors(opponent_pos, only_available=True)
            moves_dict[opponent_neighbours[i]] = len(available_opponent_moves)
            grid_clone.setCellValue(opponent_neighbours[i], 0)
    print(moves_dict)
    good_trap = min(moves_dict, key=moves_dict.get)
    return good_trap


def get_nearest_trap(top_positions, player_pos):
    distance_dict = {}
    for key in top_positions:
        distance_dict[key] = manhattan_distance(key, player_pos)
    nearest_trap = min(distance_dict, key=distance_dict.get)
    # print("Nearest Position: {}".format(nearest_trap))
    return nearest_trap


def trap_h(player_num: int, grid: Grid):
    opponent_neighbours = get_opponent_neighbours(grid, player_num=player_num)
    board_value_dict = {}
    grid_clone = grid.clone()
    opponent_pos = get_opponent_position(grid_clone, player_num)
    player_pos = grid.find(player_num)
    # print("Player Position:{}".format(player_pos))
    for i in range(len(opponent_neighbours)):
        if grid_clone.getCellValue(opponent_neighbours[i]) == 0:
            board_v = board_value(grid_clone, opponent_neighbours[i], player_pos)
            # print("Position: {} and board value:{}".format(opponent_neighbours[i], board_v))
            board_value_dict[opponent_neighbours[i]] = board_v

    max_position = max(board_value_dict, key=board_value_dict.get)
    tied_positions = {}
    for key in board_value_dict.keys():
        if board_value_dict[key] == board_value_dict[max_position]:
            tied_positions[key] = board_value_dict[key]
    # print("Tied positons:{}".format(tied_positions))
    top_position = get_nearest_trap(tied_positions, player_pos)
    # print("top_positions: {}".format(top_position))
    return top_position


def board_value(grid, my_position, opponent_pos):
    distance = manhattan_distance(my_position, opponent_pos)
    no_neighbours = len(grid.get_neighbors(my_position, only_available=True))
    opponent_neighbours = len(grid.get_neighbors(opponent_pos, only_available=True))
    return 2*no_neighbours - opponent_neighbours
    # return (2*no_neighbours - opponent_neighbours)
    # return no_neighbours


def board_value_for_moves(grid, my_position):
    no_neighbours = len(grid.get_neighbors(my_position, only_available=True))
    return no_neighbours


def get_good_position(tied_positions, opponent_pos):
    distance_dict = {}
    for key in tied_positions:
        distance_dict[key] = manhattan_distance(key, opponent_pos)
    farthest_position = max(distance_dict, key=distance_dict.get)
    # print("Farthest Position: {}".format(farthest_position))
    return farthest_position


def move_heuristic(player_num: int, position, grid: Grid):
    opponent_pos = get_opponent_position(grid=grid, player_num=player_num)
    grid_clone = grid.clone()
    my_new_available_moves = grid_clone.get_neighbors(position, only_available=True)
    moves_dict = {}
    grid_clone.print_grid()
    for i in range(len(my_new_available_moves)):
        board_v = board_value_for_moves(grid_clone, my_new_available_moves[i])
        moves_dict[my_new_available_moves[i]] = board_v
        # print("Position: {} and board value:{}".format(my_new_available_moves[i], board_v))
    max_value = moves_dict[max(moves_dict, key=moves_dict.get)]
    tied_positions = {}
    for key in moves_dict.keys():
        if moves_dict[key] == max_value:
            tied_positions[key] = max_value
    good_move = get_good_position(tied_positions, opponent_pos)
    return good_move


def board_value_of_trap(grid: Grid, move, player, opponent):
    grid_clone = grid.clone()
    grid_clone.move(move, player)
    opponent_position = grid.find(opponent)
    my_neighbours = len(grid.get_neighbors(move, only_available=True))
    opponent_neighbours = len(grid.get_neighbors(opponent_position, only_available=True))
    return 2 * my_neighbours - opponent_neighbours


def heuristic_function(grid, move, player, opponent):
    board_value_of_move = board_value_of_trap(grid, move, player, opponent)
    return board_value_of_move




