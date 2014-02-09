import os
from random import randint

# Make table, one for each possible state of the game
states1 = []
V1 = []
totalStates1 = 0

board = [0,0,0,0,0,0,0,0,0]

states2 = []
V2 = []
totalStates2 = 0

board2 = [0,0,0,0,0,0,0,0,0]
          
tiles = [0,1,2]


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# FUNCTIONS
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def initBoard():
  for i in range(0,9):
    board[i] = 0

def determineValue(_board, player):
  won = hasWinner(_board)
  
  # win
  if 1 == won:
    if 1 == player:
      return 1.0
    else:
      return 0.0
  # draw
  elif -1 == won:
    return 0.0
  else:
    return 0.5

def switchPlayer(player):
  if player == 1:
    return 2
  else:
    return 1

def printBoard(_board):
  size = len(_board)
  for index in range(0, size):
    if _board[index] == 1:
      print 'X',
    elif _board[index] == 2:
      print 'O',
    else:
      print '_',
    if 0 == ((index + 1) % 3):
      print
  
def hasWinner(_board):
  for player in range(1, 3):
    tile = tiles[player]
    
    # check horizontal
    for i in range(0, 3):
      i = i * 3
      if (_board[i]     == tile) and \
         (_board[i + 1] == tile) and \
         (_board[i + 2] == tile):
           return 1
           
    # check vertical
    for i in range(0, 3):
      if (_board[i]     == tile) and \
         (_board[i + 3] == tile) and \
         (_board[i + 6] == tile):
           return 1
           
    # check backward diagonal
    if (_board[0] == tile) and \
       (_board[4] == tile) and \
       (_board[8] == tile):
         return 1
         
    # check forward diagonal
    if (_board[6] == tile) and \
       (_board[4] == tile) and \
       (_board[2] == tile):
         return 1
  
  # check for draw
  for i in range(0, 9):
    # 0 estimated probability of winning
    if _board[i] == 0:
      return 0 
         
  # -1 is for draw match
  return -1

def updateBoard(_board, player, index):
  if _board[index] == 0:
    _board[index] = player
    return True
  
  return False
  
def getListOfBlankTiles():
  blanks = []
  for i in range(0, 9):
    if board[i] == 0:
      blanks.append(i)
  return blanks

def greedyMove(states, V, player):
  maxVal = 0
  maxIndex = 0
  
  nextMoves = getListOfBlankTiles()
  boardIndex = nextMoves.pop()
  board[boardIndex] = player
  maxIndex = states.index(board)
  maxVal = V[maxIndex] 
  board[boardIndex] = 0
  
  for i in nextMoves:
    board[i] = player
    idx = states.index(board)
    if V[idx] > maxVal:
      boardIndex = i
      maxIndex = idx
      maxVal = V[idx]
    board[i] = 0
    
  return boardIndex, maxIndex

# State-Value Function V(s)
# V(s) = V(s) + alpha [ V(s') - V(s) ]
# s  = current state
# s' = next state
# alpha = learning rate
def updateEstimateValueOfS(sPrime, s, alpha, V):
  V[s] = V[s] + alpha*(V[sPrime] - V[s])


def saveStatesToFile(filename, states, V, totalStates):
    fp = open(filename, "w")
    for index in range(0, totalStates):
        state_string = ':'.join(map(str,states[index]))
        value_string = str(V[index])
        fp.write("%s %s\n" %(state_string, value_string))
    fp.close()

def loadStatesFromFile(fp, states, V):
    total = 0
    while True:
        line = fp.readline()
        if line == "":
            break
        first_split = line.split(' ')
        state = map(int,first_split[0].split(':'))
        value = float(first_split[1])
        states.append(state)
        V.append(value)
        total = total + 1
    return total

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROGRAM STARTS HERE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# step-size parameter (rate of learning)
alpha = 0.01

# exploration rate
exploreRate = 0.1

filename1 = "tictactoe.dat"
filename2 = "tictactoe2.dat"
# Create table of all possible TicTacToe states

# Build states for RL player 1
fp = open(filename1, "r")
print "Building states from file..."
totalStates1 = loadStatesFromFile(fp, states1, V1)
fp.close()

# Build states for RL player 2
fp = open(filename2, "r")
print "Building states from file..."
totalStates2 = loadStatesFromFile(fp, states2, V2)
fp.close()

print "Player 1 Total States: %d" %(totalStates1)
print "Player 1 Total States: %d" %(totalStates2)
raw_input("Press <Enter> to continue!")


playTimes = 100000      # number of plays during Learning Phase

numPlayer1Won = 0       # number of games won Player 1
numPlayer2Won = 0       # number of games won Player 2
numDraws = 0            # number of draws
player = 1              # starts with Player 1 during Learning Phase

while (1):
  # ensure board is all zeroes
  initBoard()
  
  # player 1 = 1 and player 2 = 2
  
  # Game phase:
  # randomly select who goes first
  player = randint(1,2)
  
  # Prints board
  print "New Game (Episode): "
  printBoard(board)
  print
    
  prevIndex1 = 0          # previous state index
  maxIndex1 = 0           # index with maximum state value
  firstPlay1 = True       # flag for first play of a game episode
  
  prevIndex2 = 0          # previous state index
  maxIndex2 = 0           # index with maximum state value
  firstPlay2 = True       # flag for first play of a game episode

  while (True):
    
    nextMoves = getListOfBlankTiles()
    countNextMoves = len(nextMoves)
    exploring = False
    
    print "Player %d's move:" %(player)
    
    while (True):
      ex = randint(1, 100)/100.0
      
      # player 2
      if player == 2:
        if ex <= exploreRate:
          userPlay = nextMoves[randint(0, countNextMoves - 1)]
          exploring = True
          print "exploring"
        else:
          userPlay, maxIndex2 = greedyMove(states2, V2, player)
          print "greedy"
          if not firstPlay2:
            print "V2(s) = %f changed to" %(V2[prevIndex2]),
            updateEstimateValueOfS(maxIndex2, prevIndex2, alpha, V2)
            print "V2(s) = %f" %(V2[prevIndex2])
          prevIndex2 = maxIndex2
        
          # player 2 has done one play
          firstPlay2 = False
        
      # player 1 (Computer)
      else:
        if ex <= exploreRate:
          userPlay = nextMoves[randint(0, countNextMoves - 1)]
          exploring = True
          print "exploring"
        else:
          userPlay, maxIndex1 = greedyMove(states1, V1, player)
          print "greedy"
          if not firstPlay1:
            print "V1(s) = %f changed to" %(V1[prevIndex1]),
            updateEstimateValueOfS(maxIndex1, prevIndex1, alpha, V1)
            print "V1(s) = %f" %(V1[prevIndex1])
          prevIndex1 = maxIndex1
        
          # player 1 has done one play
          firstPlay1 = False

      # update board from user play (might be unnecessary)
      if True == updateBoard(board, player, userPlay):
        if exploring:
            if player == 1:
                prevIndex1 = states1.index(board)
            else:
                prevIndex2 = states2.index(board)
        break
    
    printBoard(board)
    
    won = hasWinner(board)
    if 1 == won:
      if 1 == player:
        # player 1 wins
        numPlayer1Won = numPlayer1Won + 1
        maxIndex2 = states2.index(board)
        print "V2(s) = %f changed to" %(V2[prevIndex2]),
        updateEstimateValueOfS(maxIndex2, prevIndex2, alpha, V2)
        print "V2(s) = %f" %(V2[prevIndex2])
        
      else:
        # player 2 wins
        numPlayer2Won = numPlayer2Won + 1
        
        maxIndex1 = states1.index(board)
        print "V1(s) = %f changed to" %(V1[prevIndex1]),
        updateEstimateValueOfS(maxIndex1, prevIndex1, alpha, V1)
        print "V1(s) = %f" %(V1[prevIndex1])
        
      print "Player %d has won!" %(player) 
      print
      break
    
    if -1 == won:
      numDraws = numDraws + 1
      #maxIndex = states.index(board)
      #print "V(s) = %f changed to" %(V[prevIndex]),
      #updateEstimateValueOfS(maxIndex, prevIndex)
      #print "V(s) = %f" %(V[prevIndex])
      print "It's a draw!"
      print
      break
    
    player = switchPlayer(player)
    print

  
  if playTimes:
    playTimes = playTimes - 1
  elif raw_input("Play Again[y]: ") != "y":
    break

saveStatesToFile(filename1, states1, V1, totalStates1)
saveStatesToFile(filename2, states2, V2, totalStates2)

print
print "-----"
print "Game Stats: "
print "Player 1 # of Wins  : %d" %(numPlayer1Won)
print "Player 2 # of Wins  : %d" %(numPlayer2Won)
print "         # of Draws : %d" %(numDraws)
