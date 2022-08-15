import numpy as np
import pygame
import random

random.seed(100)

rows = 5
columns = 5
terminalStates = 1
nva = 0

#Intial Location
alocR1, alocR2 = 4, 0 
alocC1, alocC2 = 2, 2

#Pickup Locations
pir1, pir2 = 3, 2
pic1, pic2 = 1, 4

#Drop Locations
dr1, dr2, dr3, dr4 = 0, 0, 2, 4
dc1, dc2, dc3, dc4 = 0, 4, 2, 4

grid = np.array([[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]])

blocks = np.array([[0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]])

ut = np.array([1,1,1,1,1,1])

blocks[pir1][pic1] = 10
blocks[pir2][pic2] = 10

cnt = 0
turn = 0

def updateStatus():
    if blocks[pir1][pic1] == 0:
        ut[0] = 0
    if blocks[pir2][pic2] == 0:
        ut[1] = 0
    if blocks[dr1][dc1] == 5:
        ut[2] = 0
    if blocks[dr2][dc2] == 5:
        ut[3] = 0
    if blocks[dr3][dc3] == 5:
        ut[4] = 0
    if blocks[dr4][dc4] == 5:
        ut[5] = 0

class Agent:
  def __init__(self, row, column, left, right, up, down, pickup, drop, hold):
    self.row = row
    self.column = column
    grid[row][column] = 1
    self.left = left
    self.right = right
    self.up = up
    self.down = down
    self.pickup = pickup
    self.drop = drop
    self.hold = hold

  def moveUP(self):
      if(self.up and grid[self.row-1][self.column] != 1):
        grid[self.row][self.column] = 0
        self.row = self.row - 1
        grid[self.row][self.column] = 1
        self.down = 1
        if self.row == 0:
            self.up = 0

  def moveDOWN(self):
      if(self.down and grid[self.row+1][self.column] != 1):
        grid[self.row][self.column] = 0
        self.row = self.row + 1
        grid[self.row][self.column] = 1
        self.up = 1
        if self.row == 4:
            self.down = 0

  def moveLEFT(self):
      if(self.left and grid[self.row][self.column-1] != 1):
        grid[self.row][self.column] = 0
        self.column = self.column - 1
        grid[self.row][self.column] = 1
        self.right = 1
        if self.column == 0:
            self.left = 0

  def moveRIGHT(self):
      if(self.right and grid[self.row][self.column+1] != 1):
        grid[self.row][self.column] = 0
        self.column = self.column + 1
        grid[self.row][self.column] = 1
        self.left = 1
        if self.column == 4:
            self.right = 0

  def pickUP(self):
        if(blocks[self.row][self.column] > 0 and self.hold == 0):
            if((self.row == pir1 and self.column == pic1) or (self.row == pir2 and self.column == pic2)):
                blocks[self.row][self.column] -=1
                self.hold = 1
                return True
            else:
                return False
        else:
            return False
  def DROP(self):
    if(blocks[self.row][self.column] < 5):
        if(self.row == dr1 and self.column == dc1 and self.hold == 1):
            blocks[self.row][self.column] +=1
            self.hold = 0
            return True 
        elif(self.row == dr2 and self.column == dc2 and self.hold == 1):
            blocks[self.row][self.column] +=1
            self.hold = 0 
            return True 
        elif(self.row == dr3 and self.column == dc3 and self.hold == 1):
            blocks[self.row][self.column] +=1
            self.hold = 0
            return True   
        elif(self.row == dr4 and self.column == dc4 and self.hold == 1):
            blocks[self.row][self.column] +=1
            self.hold = 0
            return True 
        else:
            return False     
    else:
        return False      



p1 = Agent(alocR1, alocC1, 1, 1, 1, 0, 0, 0, 0)
p2 = Agent(alocR2, alocC2, 1, 0, 1, 1, 0, 0, 0)

"""for i in range(1):
    p1.moveUP()
    p1.moveDOWN()
    p1.moveLEFT()
    p1.moveRIGHT()
"""

def pRandom(mA, fA, trn):
        if(ut[0] == 0 and ut[1] == 0 and p1.hold == 0 and p2.hold == 0):
            print("Game Terminated")
            return 1
        else:
            if trn%2 == 0:
                chsa = 100*random.random()
                if mA.pickUP():
                    updateStatus()
                elif mA.DROP():
                    updateStatus()
                elif chsa < 25 and mA.up:
                    mA.moveUP()
                elif chsa < 50 and mA.down:
                    mA.moveDOWN()
                elif chsa < 75 and mA.left:
                    mA.moveLEFT()
                elif chsa < 100 and mA.right:
                    mA.moveRIGHT()
                return 1
            elif trn%2 == 1:
                chsa = 100*random.random()
                if fA.pickUP():
                    updateStatus()
                elif fA.DROP():
                    updateStatus() 
                elif chsa < 25 and fA.up:
                    fA.moveUP()
                elif chsa < 50 and fA.down:
                    fA.moveDOWN()
                elif chsa < 75 and fA.left:
                    fA.moveLEFT()
                elif chsa < 100 and fA.right:
                    fA.moveRIGHT()
                return 1



#PyGame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0) 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 135
HEIGHT = 135
 
# This sets the margin between each cell
MARGIN = 15
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [765, 765]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
turn = 0
while not done:
    if(cnt > 8000):
        done = True
    if(ut[0] == 0 and ut[1] == 0 and p1.hold == 0 and p2.hold == 0):
        #p1 = Agent(alocR1, alocC1, 1, 1, 1, 0, 0)
        #p2 = Agent(alocR2, alocC2, 1, 1, 0, 1, 0)
        grid[p1.row][p1.column] = 0
        p1.row = alocR1
        p1.column = alocC1
        p1.left = 1
        p1.right = 1
        p1.down = 0
        p1.up = 1
        grid[p1.row][p1.column] = 1

        grid[p2.row][p2.column] = 0
        p2.row = alocR2
        p2.column = alocC2
        p2.left = 1
        p2.right = 1
        p2.down = 1
        p2.up = 0
        grid[p2.row][p2.column] = 1

        blocks[pir1][pic1] = 10
        blocks[pir2][pic2] = 10
        blocks[dr1][dc1] = 0
        blocks[dr2][dc2] = 0
        blocks[dr3][dc3] = 0
        blocks[dr4][dc4] = 0
        ut[0] = 1
        ut[1] = 1
        ut[2] = 0
        ut[3] = 0
        ut[4] = 0
        ut[5] = 0
        print(nva," ",terminalStates)
        nva = 0
        turn = 0
        terminalStates += 1
    else:
        cnt = cnt + pRandom(p1, p2, turn)
        nva = nva + 1
        turn = turn + 1
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the grid
    for row in range(5):
        for column in range(5):
            color = WHITE
            if grid[row][column] == 1:
                if p1.row == row and p1.column == column:
                    color = BLUE
                if p2.row == row and p2.column == column:
                    color = RED
            pygame.draw.rect(screen, color,[(MARGIN + WIDTH) * column + MARGIN, 
                                            (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            if blocks[row][column] > 0 and ((row == pir1 and column == pic1) or (row == pir2 and column == pic2)):
                count = blocks[row][column]
                d1, d2 = 0, 0
                for b in range(count):
                    if b < 5:
                        pygame.draw.circle(screen, ORANGE,[(MARGIN + WIDTH) * column + MARGIN + WIDTH/4, 
                                            (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/5 + b*MARGIN + d1*5 - 10], 10)
                        d1+=2
                    else:
                        pygame.draw.circle(screen, ORANGE,[(MARGIN + WIDTH) * column + MARGIN + WIDTH/2, 
                                            (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/5 + b*MARGIN - 5*MARGIN + d2*5 - 10], 10)
                        d2+=2 
            elif blocks[row][column] > 0:
                count = blocks[row][column]
                d1, d2 = 0, 0
                for b in range(count):
                    if b < 5:
                        pygame.draw.circle(screen, GREEN,[(MARGIN + WIDTH) * column + MARGIN + WIDTH/4, 
                                            (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/5 + b*MARGIN + d1*5 - 10], 10)
                        d1+=2
                    else:
                        pygame.draw.circle(screen, GREEN,[(MARGIN + WIDTH) * column + MARGIN + WIDTH/2, 
                                            (MARGIN + HEIGHT) * row + MARGIN + HEIGHT/5 + b*MARGIN - 5*MARGIN + d2*5 - 10], 10)
                        d2+=2                    
    # Limit to 60 frames per second
    clock.tick(120)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()