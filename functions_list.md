### Important Functions Useful for this assignment
1. Grid.py: 
   1. `getAvailableCells()`
   2. `setCellValue`
   3. `print_grid`
   4. `trap(pos)` - add trap to a particular pos of board
   5. `move(move_coordinates, playerID)`
   6. `clone` - copy of current grid
   7. `find`- to get the location a player.
      1. To find oponent: find(3-ourplayerID)
   8. `get_neighbours`
      1. get_neighbors(pos,True): get all neighbour cells that are free
      2. get_neighbors(pos, False): get all neighbour cells
      
2. Game.py: will be used to test our playerAI
   1. `throw(player, grid, intended_position)`- returns where the trap lands 
   2. `is_over` - checks if one of player or computer won
   3. `is_valid_move` - returns bool
   4. `is_valid_trap` - cell can't be a player
   5. `updateAlarm` - activates doll if time limit exceeded <br>
   #### Note: update line 231 only to PlayerAI() to test your player!

3. Utils.py: file containing default heuristic function - manhatten function
4. PlayerAI.py: file where all the code will be written<br>
   ##### TODO
   1. getMove() - ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions
   2. getTrap() - ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions
   3. we move before we trap
