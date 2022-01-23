import os
import sys
from helper_functions import *
from BaseAI import BaseAI
from Grid import Grid

# setting path to parent directory
sys.path.append(os.getcwd())
OPPONENT = lambda player: 3 - player


class MediumAI(BaseAI):

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

        new_pos = move_heuristic(player_num=self.player_num, position=self.pos, grid=grid)
        return new_pos

    def getTrap(self, grid: Grid):
        """EasyAI throws randomly to the immediate neighbors of the opponent"""

        # throwing a trap using heuristic
        trap = trap_h(player_num=self.player_num, grid=grid)
        return trap
