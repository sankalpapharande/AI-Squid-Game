import sys
import os
from helper_functions import *
# setting path to parent directory
sys.path.append(os.getcwd())
import random
from BaseAI import BaseAI
from Grid import Grid
from PlayerMinMax.trap_minimax_new import find_trap
from PlayerMinMax.move_minimax_new import find_move
OPPONENT = lambda player: 3 - player


class HardAI(BaseAI):

    def __init__(self, initial_position=None) -> None:
        super().__init__()
        self.pos = initial_position
        self.player_num = None

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos

    def getPosition(self):
        return self.pos

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid):
        """ Returns a random, valid move """

        # new_pos = move_heuristic(player_num=self.player_num, position=self.pos, grid=grid)
        available_moves = grid.get_neighbors(self.pos, only_available=True)
        new_pos = random.choice(available_moves) if available_moves else None
        #new_pos = find_move(grid, self.player_num)
        return new_pos

    def getTrap(self, grid: Grid):
        """EasyAI throws randomly to the immediate neighbors of the opponent"""

        # find opponent
        opponent = grid.find(3 - self.player_num)

        # find all available cells surrounding Opponent
        available_cells = grid.get_neighbors(opponent, only_available=True)

        # throw to one of the available cells randomly
        #trap = random.choice(available_cells)
        trap = trap_h(player_num=self.player_num, grid=grid)
        #trap = find_trap(grid, self.player_num)
        return trap