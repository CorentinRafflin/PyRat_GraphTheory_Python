###############################
# Team name to be displayed in the game 
TEAM_NAME = "Trap"

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here
import heapq
import time
###############################
# Please put your global variables here
pathCheese= []

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    (distances, predecessors)=dijkstra(mazeMap, mazeHeight, mazeWidth, playerLocation)
    pathCheese=shortestPathOptim(predecessors,playerLocation,piecesOfCheese[0]) 
    
###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    debut=time.time()
    global pathCheese
    if len(pathCheese)>1:
    	Move = move(mazeMap, pathCheese[0], pathCheese[1])
    	pathCheese = pathCheese[1:]
    	return Move 
    else :
        (distances, predecessors)=dijkstra(mazeMap, mazeHeight, mazeWidth, playerLocation)
        pathCheese=shortestPathOptim(predecessors,playerLocation,piecesOfCheese[0])
        Move = move(mazeMap, pathCheese[0], pathCheese[1])
        pathCheese = pathCheese[1:]
        print("duree=",time.time()-debut)
        return Move 


###############################

def canMove (mazeMap, fromLocation, toLocation):
	if toLocation in mazeMap[fromLocation]:
		return True
	else:
		return False 

def move(mazeMap, fromLocation, toLocation):
	if canMove(mazeMap, fromLocation, toLocation)==False:
		return None
	else:
		diff_horizontal=toLocation[0]-fromLocation[0]
		diff_vertical=toLocation[1]-fromLocation[1]
		if diff_horizontal==1:
			return MOVE_RIGHT
		elif diff_horizontal==-1:
			return MOVE_LEFT
		elif diff_vertical==1:
			return MOVE_UP
		elif diff_vertical==-1:
			return MOVE_DOWN



####################################################

# Utility function that inserts an element to the min-heap, or replaces it otherwise
def insertOrReplace (minHeap, node, weight) :
    
    # Insert if does not exist
    if node not in [x[1] for x in minHeap] :
        heapq.heappush(minHeap, (weight, node))
    
    # Replace otherwise
    else :
        indexToUpdate = [x[1] for x in minHeap].index(node) #search the location of "node" in the list
        minHeap[indexToUpdate] = (weight, node)
        heapq.heapify(minHeap) #transform a list into a heap
 
###################################################################
  
# Dijkstra takes as an input a source node and a graph
# It outputs the lengths of the shortest paths from the initial node to the others
def dijkstra (graph, height, width, sourceNode) :
 
    # We first initialize the useful data structures
    # Distances is the result of the algorithm, with the lengths of the path from the source node to node i
    # MinHeap is a min-heap that will store the nodes to visit and the associated weight
    # If a node is not in minHeap, it has been visited
    # We initialize the algorithm with the source node at distance 0
    distances = [[float("inf") for i in range(height)] for j in range(width)]
    minHeap = [(0, sourceNode)]
    distances[sourceNode[0]][sourceNode[1]] = 0
    predecessors = [[None for i in range(height)] for i in range(width)] #we keep track of the predecessors of every node along the shortest paths
    
    # Main loop
    while len(minHeap) != 0 :
        
        # We extract the closest node from the heap
        (closestNodeDistance, closestNode) = heapq.heappop(minHeap)
        
        # We update the distance to the neighbors of this node
        for neighbor in graph[closestNode] :
            weight=graph[closestNode][neighbor]
            neighborDistance = closestNodeDistance + weight
            
            distancetocompare=distances[neighbor[0]][neighbor[1]]
            if neighborDistance < distancetocompare :
                insertOrReplace(minHeap, neighbor, neighborDistance)
                distances[neighbor[0]][neighbor[1]] = neighborDistance
                predecessors[neighbor[0]][neighbor[1]] = closestNode # we update the predecessor since the path is shorter when going through the closest node
 
    # We return the distances and the predecessors
    return (distances, predecessors) # <-- new code (we also return the routes)

########

def shortestPathOptim(predecessors, sourceNode, finalNode):
       
        pathToInverse=[finalNode]
        while sourceNode not in pathToInverse:
            finalNode=predecessors[finalNode[0]][finalNode[1]] #Matrix again
            pathToInverse.append(finalNode)
        return list(reversed(pathToInverse))




