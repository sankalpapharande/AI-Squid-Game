from BaseAI import BaseAI
import sys
import os
from helper_functions import *
from PlayerMinMax.move_minimax_new import find_move
from PlayerMinMax.trap_minimax_new import find_trap


# setting path to parent directory
sys.path.append(os.getcwd())


# TO BE IMPLEMENTED
#
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions,
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """

        #new_pos = move_heuristic(player_num=self.player_num, position=self.pos, grid=grid)
        #new_pos = find_best_move(grid, self.player_num)
        #new_pos = find_best_move_new_minmax(grid, self.player_num)
        new_pos = find_move(grid, self.player_num)
        return new_pos

    def getTrap(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions,
        taking into account the probabilities of it landing in the positions you want.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """
        #trap = trap_h(player_num=self.player_num, grid=grid)
        #trap = find_best_trap(grid=grid, player_no=self.player_num)
        #trap = find_best_trap_new_minimax(grid, self.player_num)
        trap = find_trap(grid, self.player_num)
        return trap
