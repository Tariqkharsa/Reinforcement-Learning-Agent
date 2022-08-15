import numpy as np
import pygame
import random
from collections import defaultdict
import math

random.seed(14)
learningRate = 0.3
discountRate = 0.5
epilson = 0

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

bl = np.array([[0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]])
q_table = np.array([[0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0],
                  [0,0,0,0,0]], dtype=np.float64)
q_actions = np.array([["n/a","n/a","n/a","n/a","n/a"],
                  ["n/a","n/a","n/a","n/a","n/a"],
                  ["n/a","n/a","n/a","n/a","n/a"],
                  ["n/a","n/a","n/a","n/a","n/a"],
                  ["n/a","n/a","n/a","n/a","n/a"]])
ut = np.array([1,1,1,1,1,1])

bl[pir1][pic1] = 10
bl[pir2][pic2] = 10

cnt = 0
turn = 0

def updateStatus():
    if bl[pir1][pic1] == 0:
        ut[0] = 0
    if bl[pir2][pic2] == 0:
        ut[1] = 0
    if bl[dr1][dc1] == 5:
        ut[2] = 0
    if bl[dr2][dc2] == 5:
        ut[3] = 0
    if bl[dr3][dc3] == 5:
        ut[4] = 0
    if bl[dr4][dc4] == 5:
        ut[5] = 0
class Agent:
  def __init__(self, row, column, left, right, up, down, hold):
    self.row = row
    self.column = column
    grid[row][column] = 1
    self.left = left
    self.right = right
    self.up = up
    self.down = down
    self.hold = hold
    self.cur_action = "down"

  def moveUP(self):
      if(self.up and grid[self.row-1][self.column] != 1):
        grid[self.row][self.column] = 0
        self.row = self.row - 1
        grid[self.row][self.column] = 1
        self.down = 1
        self.cur_action = "up"
        if self.row == 0:
            self.up = 0

  def moveDOWN(self):
      if(self.down and grid[self.row+1][self.column] != 1):
        grid[self.row][self.column] = 0
        self.row = self.row + 1
        grid[self.row][self.column] = 1
        self.up = 1
        self.cur_action = "down"
        if self.row == 4:
            self.down = 0

  def moveLEFT(self):
      if(self.left and grid[self.row][self.column-1] != 1):
        grid[self.row][self.column] = 0
        self.column = self.column - 1
        grid[self.row][self.column] = 1
        self.right = 1
        self.cur_action = "left"
        if self.column == 0:
            self.left = 0

  def moveRIGHT(self):
      if(self.right and grid[self.row][self.column+1] != 1):
        grid[self.row][self.column] = 0
        self.column = self.column + 1
        grid[self.row][self.column] = 1
        self.left = 1
        self.cur_action = "right"
        if self.column == 4:
            self.right = 0

  def pickUP(self):
        if(bl[self.row][self.column] > 0 and self.hold == 0):
            if((self.row == pir1 and self.column == pic1) or (self.row == pir2 and self.column == pic2)):
                bl[self.row][self.column] -=1
                self.hold = 1
                self.cur_action = "pkUP"
                return True
            else:
                return False
        else:
            return False
    

  def DROP(self):
    if(bl[self.row][self.column] < 5):
        if(self.row == dr1 and self.column == dc1 and self.hold == 1):
            bl[self.row][self.column] +=1
            self.hold = 0
            self.cur_action = "drop"
            return True 
        elif(self.row == dr2 and self.column == dc2 and self.hold == 1):
            bl[self.row][self.column] +=1
            self.hold = 0 
            self.cur_action = "drop"
            return True 
        elif(self.row == dr3 and self.column == dc3 and self.hold == 1):
            bl[self.row][self.column] +=1
            self.hold = 0
            self.cur_action = "drop"
            return True   
        elif(self.row == dr4 and self.column == dc4 and self.hold == 1):
            bl[self.row][self.column] +=1
            self.hold = 0
            self.cur_action = "drop"
            return True 
        else:
            return False     
    else:
        return False


p1 = Agent(alocR1, alocC1, 1, 1, 1, 0, 0)
p2 = Agent(alocR2, alocC2, 1, 1, 0, 1, 0)

"""for i in range(1):
    p1.moveUP()
    p1.moveDOWN()
    p1.moveLEFT()
    p1.moveRIGHT()
"""
ut2 = defaultdict(dict)
for i1 in range(5):
    for j1 in range(5):
        for h1 in range(2):
            for pk1 in range(2):
                    for pk2 in range(2):
                        for dk1 in range(2):
                            for dk2 in range(2):
                                for dk3 in range(2):
                                    for dk4 in range(2):
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["left"] = 0
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["right"] = 0
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["up"] = 0
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["down"] = 0
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["pkUP"] = 0
                                        ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["drop"] = 0

def pRandom(mA, fA, trn):
        if(ut[0] == 0 and ut[1] == 0 and p1.hold == 0 and p2.hold == 0):
            return 1
        else:
            if trn%2 == 1:
                chsan = 100*random.random()
                if mA.pickUP():
                    updateStatus()
                elif mA.DROP():
                    updateStatus()
                elif chsan < 25 and mA.up:
                    mA.moveUP()
                elif chsan < 50 and mA.down:
                    mA.moveDOWN()
                elif chsan < 75 and mA.left:
                    mA.moveLEFT()
                elif chsan < 100 and mA.right:
                    mA.moveRIGHT()
                return 1
            elif trn%2 == 0:
                chsan = 100*random.random()
                if fA.pickUP():
                    updateStatus()
                elif fA.DROP():
                    updateStatus() 
                elif chsan < 25 and fA.up:
                    fA.moveUP()
                elif chsan < 50 and fA.down:
                    fA.moveDOWN()
                elif chsan < 75 and fA.left:
                    fA.moveLEFT()
                elif chsan < 100 and fA.right:
                    fA.moveRIGHT()
                return 1
def possibleActions(agent):
    maxVal = 0
    pkVal, drVal, lfVal,rtVal,doVal, upVal = -10000, -10000, -10000, -10000, -10000, -10000
    v2 = (agent.row,agent.column,agent.hold,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])
    if agent.pickUP():
        bl[agent.row][agent.column] +=1
        agent.hold = 0
        pkVal = ut2[v2]["pkUP"]
    elif agent.DROP():
        bl[agent.row][agent.column] -=1
        agent.hold = 1 
        drVal = ut2[v2]["drop"]
    else:
        if agent.up:
            upVal = ut2[v2]["up"]
        if agent.down:
            doVal = ut2[v2]["down"]
        if agent.left:
            lfVal = ut2[v2]["left"]
        if agent.right:
            rtVal = ut2[v2]["right"]
    maxVal = max(pkVal, drVal, upVal, doVal, lfVal, rtVal)
    return maxVal

def chooseAction(agent):
    choiceA = []
    maxVal = 0
    v3 = (agent.row,agent.column,agent.hold,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])
    lfVal,rtVal,doVal, upVal = -10000, -10000, -10000, -10000
    if(agent.up and grid[agent.row-1][agent.column] != 1):
        upVal = ut2[v3]["up"]
    if(agent.down and grid[agent.row+1][agent.column] != 1):
        doVal = ut2[v3]["down"]
    if(agent.left and grid[agent.row][agent.column-1] != 1):
        lfVal = ut2[v3]["left"]
    if(agent.right and grid[agent.row][agent.column+1] != 1):
        rtVal = ut2[v3]["right"]
    maxVal = max(upVal, doVal, lfVal, rtVal)
    if(upVal == maxVal and agent.up and grid[agent.row-1][agent.column] != 1):
        choiceA.append("up")
    if(doVal == maxVal and agent.down and grid[agent.row+1][agent.column] != 1):
        choiceA.append("down")
    if(lfVal == maxVal and agent.left and grid[agent.row][agent.column-1] != 1):
        choiceA.append("left")
    if(rtVal == maxVal and agent.right and grid[agent.row][agent.column+1] != 1):
        choiceA.append("right")
    chsa = math.floor(len(choiceA)*random.random())
    chsa2 = 100*random.random()
    if len(choiceA) == 0:
        chsa2 = 90
    if chsa2 < (100 - epilson*10):
        if choiceA[chsa] == "up":
            return 0
        elif choiceA[chsa] == "down":
            return 1
        elif choiceA[chsa] == "left":
            return 2
        elif choiceA[chsa] == "right":
            return 3
    else:
        chsa3 = 100*random.random()
        if chsa3 < 25 and agent.up:
            return 0
        elif chsa3 < 50 and agent.down:
            return 1
        elif chsa3 < 75 and agent.left:
            return 2
        elif chsa3 < 100 and agent.right:
            return 3

def pExploit(mA, fA, trn):
        #shortcut for variables
        mr1 = mA.row
        mc1 = mA.column
        fr1 = fA.row
        fc1 = fA.column
        mh = mA.hold
        fh = fA.hold
        v1 = (mr1,mc1,mh,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])
        v6 = (fr1,fc1,fh,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])
        #check to see if game is terminated
        if(ut[0] == 0 and ut[1] == 0 and p1.hold == 0 and p2.hold == 0):
            print("Game Terminated")
            return 1
        else:
            if trn%2 == 1:
                if mA.pickUP():
                    updateStatus()
                    ut2[v1]["pkUP"] = (1-learningRate)*ut2[v1]["pkUP"] + (learningRate)*(13 + (discountRate)*possibleActions(mA))
                elif mA.DROP():
                    updateStatus()
                    ut2[v1]["drop"] = (1-learningRate)*ut2[v1]["drop"] + (learningRate)*(13 + (discountRate)*possibleActions(mA)) 
                else:
                    chA = chooseAction(mA)
                    if chA == 0:
                        mA.moveUP()
                        ut2[v1]["up"] = (1-learningRate)*ut2[v1]["up"] + (learningRate)*(-1 + (discountRate)*possibleActions(mA))
                    if chA == 1:
                        mA.moveDOWN()
                        ut2[v1]["down"] = (1-learningRate)*ut2[v1]["down"] + (learningRate)*(-1 + (discountRate)*possibleActions(mA))
                    if chA == 2:
                        mA.moveLEFT()
                        ut2[v1]["left"] = (1-learningRate)*ut2[v1]["left"] + (learningRate)*(-1 + (discountRate)*possibleActions(mA))
                    if chA == 3:
                        mA.moveRIGHT()
                        ut2[v1]["right"] = (1-learningRate)*ut2[v1]["right"] + (learningRate)*(-1 + (discountRate)*possibleActions(mA))
                return 1
            elif trn%2 == 0:
                if fA.pickUP():
                    updateStatus()
                    ut2[v6]["pkUP"] = (1-learningRate)*ut2[v6]["pkUP"] + (learningRate)*(13 + (discountRate)*possibleActions(fA))
                elif fA.DROP():
                    updateStatus()
                    ut2[v6]["drop"] = (1-learningRate)*ut2[v6]["drop"] + (learningRate)*(13 + (discountRate)*possibleActions(fA)) 
                else:
                    chA = chooseAction(fA)
                    if chA == 0:
                        fA.moveUP()
                        ut2[v6]["up"] = (1-learningRate)*ut2[v6]["up"] + (learningRate)*(-1 + (discountRate)*possibleActions(fA))
                    if chA == 1:
                        fA.moveDOWN()
                        ut2[v6]["down"] = (1-learningRate)*ut2[v6]["down"] + (learningRate)*(-1 + (discountRate)*possibleActions(fA))
                    if chA == 2:
                        fA.moveLEFT()
                        ut2[v6]["left"] = (1-learningRate)*ut2[v6]["left"] + (learningRate)*(-1 + (discountRate)*possibleActions(fA))
                    if chA == 3:
                        fA.moveRIGHT()
                        ut2[v6]["right"] = (1-learningRate)*ut2[v6]["right"] + (learningRate)*(-1 + (discountRate)*possibleActions(fA))
                return 1



#PyGame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0) 
DOP = (255, 0, 255)
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
font = pygame.font.Font('freesansbold.ttf', 32)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
turn = 0
mhd = 0
q_val = "0"
q_val2 = "0"
while not done:
    if(cnt >= 8000):
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

        bl[pir1][pic1] = 10
        bl[pir2][pic2] = 10
        bl[dr1][dc1] = 0
        bl[dr2][dc2] = 0
        bl[dr3][dc3] = 0
        bl[dr4][dc4] = 0
        ut[0] = 1
        ut[1] = 1
        ut[2] = 0
        ut[3] = 0
        ut[4] = 0
        ut[5] = 0
        print(nva," ",terminalStates)
        turn = 0
        nva = 0
        terminalStates += 1
    elif(cnt < 100):
        cnt = cnt + pRandom(p1, p2, turn)
        nva = nva + 1
        turn = turn + 1
    else:
        q_val = ut2[(p1.row,p1.column,p1.hold,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])][p1.cur_action]
        q_val2 = ut2[(p2.row,p2.column,p2.hold,ut[0],ut[1],ut[2],ut[3],ut[4],ut[5])][p2.cur_action]
        mhd = mhd + abs(p1.row-p2.row) + abs(p1.column-p2.column)
        cnt = cnt + pExploit(p1, p2, turn)
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
            if (row == dr1 and column == dc1) or (row == dr2 and column == dc2) or (row == dr3 and column == dc3) or (row == dr4 and column == dc4):
                    color = DOP 
            if grid[row][column] == 1:
                if p1.row == row and p1.column == column:
                    color = BLUE
                if p2.row == row and p2.column == column:
                    color = RED
            pygame.draw.rect(screen, color,[(MARGIN + WIDTH) * column + MARGIN, 
                                            (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            if cnt >= 100:
                screen.blit(font.render(str(q_table[row][column]), True, (0,0,0)), ((MARGIN + WIDTH) * column + MARGIN*4, (MARGIN + HEIGHT) * row + MARGIN))
                screen.blit(font.render(q_actions[row][column], True, (0,0,0)), ((MARGIN + WIDTH) * column + MARGIN*3, (MARGIN + HEIGHT) * row + MARGIN + MARGIN*6))
                if p1.row == row and p1.column == column:
                    q_table[row][column] = q_val
                    q_actions[row][column] = p1.cur_action
                if p2.row == row and p2.column == column:
                    q_table[row][column] = q_val2
                    q_actions[row][column] = p2.cur_action
            if bl[row][column] > 0 and ((row == pir1 and column == pic1) or (row == pir2 and column == pic2)):
                count = bl[row][column]
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
            elif bl[row][column] > 0:
                count = bl[row][column]
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
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
file1 = open("Q-Table.txt","w")
file1.write("Hello \n")
file1.write("X Y H P1 P2 D1 D2 D3 D4 \n")
for i1 in range(5):
    for j1 in range(5):
        for h1 in range(2):
            for pk1 in range(2):
                    for pk2 in range(2):
                        for dk1 in range(2):
                            for dk2 in range(2):
                                for dk3 in range(2):
                                    for dk4 in range(2):
                                        string1 = str(i1) + " " + str(j1) + " " + str(h1) + " " + str(pk1) + "  " + str(pk2)  + "  " + str(dk1)  + "  " + str(dk2) 
                                        string1 = string1 + "  " + str(dk3) + "  " + str(dk4) + "  "
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["left"] != 0:
                                            file1.write(string1+"left: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["left"]) + "\n")
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["right"] != 0:
                                            file1.write(string1+"right: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["right"]) + "\n")
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["up"] != 0:
                                            file1.write(string1+"up: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["up"]) + "\n")
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["down"] != 0:
                                            file1.write(string1+"down: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["down"]) + "\n")
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["pkUP"] != 0:
                                            file1.write(string1+"pickup: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["pkUP"]) + "\n")
                                        if ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["drop"] != 0:
                                            file1.write(string1+"drop: "+ str(ut2[(i1,j1,h1,pk1,pk2,dk1,dk2,dk3,dk4)]["drop"]) + "\n")
file1.close()