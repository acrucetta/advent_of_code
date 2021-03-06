"""
Utility functions and classes for Advent of Code
"""

import shapely.geometry
import shapely.affinity
import math
import copy
import parse
import numpy as np

# References: 
# github.com/borja

#
# DEBUGGING/LOGGING
#

DEBUG=False

def set_debug(debug):
    """
    Enables/disables debug messages
    """
    global DEBUG
    DEBUG = debug


def log(*args):
    """
    Prints a debugging message (if debugging messages are enabled)
    """
    if DEBUG: 
        print('\x1b[7;30;47m', end="")
        print(*args, end="")
        print('\x1b[0m')
        
def call_and_print(fn, *args):
    """
    Call a function with some parameters, and print the
    function call and the return value.
    """
    str_args = ", ".join(repr(arg) for arg in args)

    if len(str_args) > 20:
        str_args = str_args[:20] + "..."

    print("{}({}) = {}".format(fn.__name__, str_args, fn(*args)))


#
# FILE I/O
#

def read_strs(filename, sep=None):
    """
    Read strings from a file, separated by whitespace or by the
    specified separator.
    """
    with open(filename) as f:
        txt = f.read().strip()
        strs = txt.split(sep=sep)    

    return strs

def read_grid(filepath):
    '''
    Reads matrix from the filepath.
    '''
    with open(filepath) as f:
        data = f.readlines()
    
    rows = list(map(lambda x: x.strip('\n'),data))
    matrix = []
    
    for row in rows:
        split_row = [int(r) for r in row]
        matrix.append(split_row)
    
    return np.array(matrix)

#
# GRID CLASS
#

class Grid:
    '''
    A class used to read a grid and manipulate its positions
    (x,y) where the top-left position is (0,0)
    '''
    # Useful for problems that require checking adjacent positions (from Borja's Grid class)
    DIRECTIONS = [(-1, -1), (0, -1), (+1,-1),
                  (-1,  0),          (+1, 0),
                  (-1, +1), (0, +1), (+1,+1)]

    CARDINAL_DIRS = [          (0, -1),
                     (-1,  0),          (+1, 0),
                               (0, +1)         ]   
    
    
    def __init__(self,grid):
        self._grid = copy.deepcopy(grid)
        self.max_x = len(grid[0])
        self.max_y = len(grid)
    
    def __validate_coordinates(self,x,y):
        orig_x = x
        orig_y = y
        if orig_x < 0 or orig_x >= self.max_x:
            raise IndexError("Invalid x coordinate: {}".format(orig_x))
        if orig_y < 0 or orig_y >= self.max_y:
            raise IndexError("Invalid y coordinate: {}".format(orig_y))
        return x,y
    
    def __str__(self):
        '''
        Prints the existing grid class.
        '''
        rows = [", ".join(str(x) for x in row) for row in self._grid]
        return "\n".join(rows)
    
    def __getitem__(self,pos):
        '''
        Returns the value at the specified position.
        '''
        x,y = self.__validate_coordinates(pos[0],pos[1])
        
        return self._grid[y][x]
    
    def __setitem__(self,pos,value):
        '''
        Sets the value at the specified position.
        '''
        x,y = self.__validate_coordinates(pos[0],pos[1])
        self._grid[y][x] = value
    
    def __iter__(self):
        '''
        Iterates over the grid.
        '''
        for row in self._grid:
            for item in row:
                yield item
    
    def get_adjacent_positions(self,pos):
        '''
        Returns a list of adjacent positions to the specified position.
        '''
        x, y = self.__validate_coordinates(pos[0],pos[1])
        positions = {"UP":(x,y-1),"DOWN":(x,y+1),"RIGHT":(x+1,y),"LEFT":(x-1,y),
                     "UP-LEFT":(x-1,y-1),"UP-RIGHT":(x+1,y-1),"DOWN-LEFT":(x-1,y+1),"DOWN-RIGHT":(x+1,y+1)}
        for adj,pos in positions.items():
            try:
                x, y = self.__validate_coordinates(pos[0],pos[1])
            except IndexError:
                positions[adj] = None
        return positions
    
    def get_cardinal_positions(self,pos):
        '''
        Returns a list of cardinal positions to the specified position.
        '''
        x,y = self.__validate_coordinates(pos[0],pos[1])
        positions = {"N":(x,y-1),"S":(x,y+1),"E":(x+1,y),"W":(x-1,y)}
        # Check that all cardinal positions are valid
        for card,pos in positions.items():
            try:
                x, y = self.__validate_coordinates(pos[0],pos[1])
            except IndexError:
                positions[card] = None
        return positions
        