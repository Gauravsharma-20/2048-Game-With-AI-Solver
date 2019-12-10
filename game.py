from random import *
from copy import deepcopy
from itertools import product
import math


# for computing tile indices in each direction.
OFFSETS = {'UP': (1, 0),
           'DOWN': (-1, 0),
           'LEFT': (0, 1),
           'RIGHT': (0, -1)}


def merge(line):
    """
    function that merges a single row or column in 2048
    """
    r1 = [0]*4
    r2 = []
    pos1,pos2 = 0,0
    score = 0
    
    for num in line:
        if num != 0:
            r1[pos1] = num
            pos1 += 1
            
    while len(r1) > 1:
        if r1[pos2] == r1[pos2+1]:
            r2.append(r1[pos2]*2)
            score += r1[pos2]
            del r1[pos2:pos2+2]
        else:
            r2.append(r1[pos2])
            del r1[pos2]
            
    r2 += r1
    
    if len(r2) < len(line):
        r2.extend([0]*(len(line)-len(r2)))
    r2.append(score)
    
    return r2

def std(lst):
    """
    calculates the standard deviation
    """
    average = sum(lst)/float(len(lst))
    variance = sum(list(map(lambda x: (x-average)**2, lst)))/float(len(lst))
    stdev = math.sqrt(variance)
    
    return stdev



class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.numCol = grid_height
        self.numRow = grid_width
        self.grid = []
        self.actualScore = 0
        self.bestScores = []
        
        for i in range(self.numRow):
            self.grid.append([0]*self.numCol)
            
        for i in range(2):
            self.new_tile()


    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.actualScore = 0
        for i in range(self.numRow):
            for j in range(self.numCol):
                self.grid[i][j] = 0
                
        for i in range(2):
            self.new_tile()
                

    def __str__(self):
        """
        Return a string representation of the grid for checking.
        """
        rep = ""
        g = deepcopy(self.grid)
        for i in range(self.numRow):
            for j in range(self.numCol):
                g[i][j] = str(g[i][j])
                
        for row in g:
            rep = rep + "   ".join(row) + "\n"*2
            
        return rep
        

    def get_grid_height(self):
        return self.numRow


    def get_grid_width(self):
        return self.numCol


    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initialTilesDictionary = {
                        'UP': [(0, 0), (0, 1), (0, 2), (0, 3)], 
                        'DOWN': [(3, 0), (3, 1), (3, 2), (3, 3)],
                        'LEFT': [(0, 0), (1, 0), (2, 0), (3, 0)],
                        'RIGHT': [(0, 3), (1, 3), (2, 3), (3, 3)]
                        }
        initialTiles = initialTilesDictionary[direction]
        
        for tile in initialTiles:
            l = [tile]
            line = [int(self.get_tile(*tile))]
            i = 0
            while i < 3:
                c = OFFSETS[direction]
                nextTile = (tile[0] + c[0],tile[1] + c[1])
                l.append(nextTile)
                line.append(int(self.get_tile(*nextTile)))
                tile = nextTile
                i += 1
            mergedLine = merge(line)[:-1]
            self.actualScore += 2*merge(line)[-1]
            for i in range(4):
                self.set_tile(l[i][0],l[i][1], mergedLine[i])
                
        self.new_tile()
        

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 for 90% of the time and
        4 for 10% of the time(probable decision).
        """
        seq = [2]*9 + [4]
        newTile = choice(seq)
        emptySquareList = self.empty_cells()
        emptySquare = choice(emptySquareList)
        self.grid[emptySquare[0]][emptySquare[1]] = newTile
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value
        

    def get_tile(self, row, col):
        return self.grid[row][col]

##    def current_score(self):
##        """
##        Calculate the score by combining several
##        other scores for each game state.
##        """
##        score = self.actualScore + \
##                math.log(self.actualScore+1)*self.number_of_empty_cells() - \
##                math.sqrt(self.clustering_score())
##        return score

    def empty_cells(self):
        """
        Return a list of empty cells.
        """
        emptySquareList = []
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    emptySquareList.append([row, col])
                    
        return emptySquareList


    def number_of_empty_cells(self):
        """
        Calculate the number of empty cells in the grid.
        """
        return len(self.empty_cells())


    def on_the_board(self, row, col):
        if row in range(4) and col in range(4):
            return True
        else:
            return False
    

    def hscore(self):
        """
        Measure how scattered the values of the board are.
        """
        count = {}
        entropy = 0
        nonZero = self.numRow * self.numCol - self.number_of_empty_cells()
        for row in range(self.numRow):
            for col in range(self.numCol):
                if self.grid[row][col] != 0:
                    if self.grid[row][col] in count:
                        count[self.grid[row][col]] += 1
                    else:
                        count[self.grid[row][col]] = 1
        for k in count.keys():
            freq = count[k]/float(nonZero)
            entropy -= freq * math.log(freq)
        entropy /= math.log(self.numRow * self.numCol)
        
        return nonZero + entropy


    def test_move(self, direction):
        """
        Check if a certain move changes the game state
        """
        t = deepcopy(self)
        t.move(direction)
        
        return t.grid == self.grid
            

    def game_over(self):
        """
        Check if the there's any further step that can be taken
        (or if the game has reached its final state)
        """
        gameOver = True
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            try:
                a = self.test_move(direction)
                if not a:
                    return False
            except IndexError:
                pass
        return gameOver and not self.number_of_empty_cells()
            
def Run2048():
    t = TwentyFortyEight(4, 4)
    i = 0
    while i < 60 and not t.game_over():
        hScores = {}
        compt = deepcopy(t)
        d = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for direction in list(product(d, d, d)):
            hScores[direction] = 0
            c = deepcopy(t)
            for j in range(len(direction)):
                try:
                    c.move(direction[j])
                    hScores[direction] += c.hscore()
                except IndexError:
                    break
            
        hScoreList = sorted(hScores.values())
        for key in hScores.keys():
            if hScores[key] == hScoreList[0]:
                direc = key
        for k in range(len(direc)):
            try:
                t.move(direc[k])
            except IndexError:
                break
        i += 1
    j = 0
    while j < 50 and not t.game_over():
        for dir in ['DOWN', 'LEFT', 'DOWN', 'RIGHT']:
            try:
                t.move(dir)
            except IndexError:
                break
            j += 1
    return t

#print(Run2048())

##total = []
##for i in range(100):
##    total.append(run2048())
##print(sum(total)/100)    
