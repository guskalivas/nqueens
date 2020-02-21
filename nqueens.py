# Author: Gus Kalivas


import random
import math

'''
succ method takes in a current state and boulders x and y postion.
@returns list of lists of possible next successors of state
'''
def succ(state, boulderX, boulderY):
    full = []
    if state == None: #check if state is none
        return None
    #loop through row and coluyms to find next possible states 
    for row in range(len(state)):
        for col in range(len(state)):
            # if row and col x,y are the boulders postion skip it 
            if row == boulderX and col == boulderY:
                continue
            #if the col does not equal the value in the row
            if col != state[row]:
                ax = list(state) # create a new list
                ax[row] = col   #switch the value of the row with the colum val
                full.append((list(ax))) # append full list
    return full


''''
can_sttack takes in two positions and returns 1 if it can attack and 0 otherwise
'''
def can_attack(one, two):
    # top = y2-y1 to find slope
    top = two[1] - one[1]
    # bottom = x2-x1 to find slope
    bottom = two[0] - one[0]

    # if can attack left - right or top - bottom
    if top == 0 or bottom == 0:
        return 1
    else:

        # if can attack diagonal
        slope = abs(top / bottom)
        if slope == 1:
            return 1
    
    # if can't attack
    return 0


''' 
is_between takes in three positions to find if a point is in between two. 
found algorithm from stack overflow
at https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment 
'''
def is_between(a, c, b):
    #checks the cross-product to see if three points are aligned
    cross = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])

    #to find between find the dot-product and compare to squared if postive it is between
    dot = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
    squared = (b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])

    if abs(cross) != 0 or dot < 0 or dot > squared:
        return False
    return True


'''
f takes in a current state and postion of boulders x and y. It calculates the number of queens
being attacked at the given state
'''
def f(state, boulderX, boulderY):
    #board in x,y coordinates
    board = [(x, y) for x, y in enumerate(state)]
    #dic of attacked queens 
    attacked_quees = {point : 0 for point in board}
    #loop through the boards and compare current to other coordinates
    for current_point in board:
        for other in board:    
            # if the current is not the other and is not between current and boulder and can attack        
            if current_point != other and not is_between(current_point, (boulderX, boulderY), other) and can_attack(current_point, other) == 1:
                attacked_quees[current_point] = 1 #incremenet attacked queens at current postions 

    #returns the sum of total queens that can be attacked            
    return sum(attacked_quees.values())



''''
choose_next takes in a current state and boulders x and y postions and returns the next state to select
'''
def choose_next(curr, boulderX, boulderY):
    full = succ(curr, boulderX,boulderY)
    cF = f(curr,boulderX,boulderY)
    l = []
    for i in full: #loop through full list to create a dictionary of the states used to sort
        d = {}
        d['State'] = i
        d['F'] = f(i, boulderX,boulderY)
        l.append(d)
    full.append(curr)
    #finds the lowest f value in the entire list
    fullx = sorted(l, key = lambda e:e['F'])
    low = fullx[0]
    # if the lowest f is less then currents f and a unique f value 
    if low['F'] <= cF and isUnique(low['F'], fullx):
        return low['State'] # return that state
    else:
        l = [] 
        for i in full: # else create a new full list and add state if less then or equal to the lowest state
            num = f(i, boulderX,boulderY)
            if num <= low['F']:
                l.append(i)
        l.sort() # sort the lists 
        val = l[0]
        if val == curr: # take the lowest 'state' and if its current return none else return val
            return None
        return val

''''
isUnique checks if the f value is unique value in a list of successors
'''
def isUnique(f,succ):
    # loop through list of dictionaries and if any f are the same return false 
    for i in succ:
        if i['F'] == f:
            return False
    return True

''''
nqueens runs the hill climbing algorithm. Takes in the inital state and boulder's x,y postion
and returns the final state with its f value
'''
def nqueens(initial_state, boulderX, boulderY):
    # get current state and current f value
    curr = initial_state
    h = f(curr,boulderX,boulderY)
    # print the first postion
    print(curr, '-', 'f=', h)
    while True: #loop until found solution or till cant go any further
        hf = f(curr,boulderX,boulderY) # get current f value
        next = choose_next(curr,boulderX,boulderY) # get next state 
        if next == None:
            return curr # if next is none breaks and returns current state
        cf = f(next,boulderX,boulderY) # f value of the next state
        if cf > hf: # if this value is greater then are currents f value break
            break
        curr = next # set current to next and print out this step
        print(next, '-', 'f=', cf)
    return curr 

#print(nqueens([0,2,2,3,4,5,6,7], 1, 1))
#print(nqueens([0,1,2,3,5,5,6,7], 4, 4))

'''
nqueens_restart takes in n as the size of the board, k as the number of times to run and
boulders x,y postion and runs hill climbing algorithm
'''
def nqueens_restart(n, k, boulderX, boulderY):
    count = 0 # count for num of solutions it goes though
    lsol =[] 
    solved = []
    while count < k: # while count is less then number of iterations 
        board = genboard(n,k,boulderX,boulderY) # generate the board
        sol = nqueens(board,boulderX,boulderY) # get the solution to this board
        fsol = f(sol,boulderX,boulderY) # get the f value of this solution
        if fsol ==0:    
            print('Found Solution at #:', count, sol, 'f=', fsol)
            return None # print solution found and return none
        if sol not in lsol: # if the solution is not already in this list and not a 0 f, add it 
            lsol.append(sol)
        print('Solution #:', count, ' Gets Stuck at:', fsol)
        print('\n') # for spacing on printing 
        # creating a dictionary for each state with board, f value and what number solution it is
        d={}
        d['state'] = sol
        d['f'] = fsol
        d['count'] = count
        solved.append(d)

        count+=1
    tiedsol(solved) # call tied solution when there are multiple solutions with same f value and not a 0 f

'''
tiedsol takes in the list of dictionaries if no final solution was found
'''
def tiedsol(d):
    l = []
    # sort by the f value first to find the lowest f 
    l = sorted(d, key = lambda e:e['f'])
    lowF = l[0]
    cF = lowF['f']
    # loop through the list and compare the other f values to the lowest 
    for i in l:
        if i['f'] > cF:
            # if its greater sort the list of states by the state
            values = sorted(l, key = lambda k:k['state'])
            for j in values: # looping to find if this f is lower then current to not add duplicate
                if j['f'] <= cF:
                    continue
                else:
                    print('Solution #:', j['count'], 'Stopped at:',j['state'], 'f=', j['f'])
        else: # if its lower then lowest f - has a lower state print the solution 
            print('Solution #:', i['count'], 'Stopped at:',i['state'], 'f=', i['f'])
    return None

'''
genboard takes in the n size, k times and boulders x,y postion to generate a valid state
'''
def genboard(n,k,boulderX,boulderY):
    board = []
    # loops through range of n and adds random values from 0 to n -1 
    for i in range(n):
        board.append(random.randint(0,n-1))
    # loops through the board with coordinates to check if its a valid board
    for x,y in enumerate(board):
        # if x,y equal the boulders postions call the genboard again to create a new board 
        if x == boulderX and y == boulderY: 
            board = genboard(n,k,boulderX,boulderY)
    return board

nqueens_restart(8,5,2,2)
        
