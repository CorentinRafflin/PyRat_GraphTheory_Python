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
pathCheese=[]
graphOfCheese=[]
bestPath=[]
listOfCheese=[]
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
    global pathCheese, bestPath, listOfCheese, graphOfCheese
    listOfCheese=piecesOfCheese #we keep the original positions of cheese
    piecesOfCheese.append(playerLocation) #we add the playerLocation to piecesOfCheese
    graphOfCheese = graphCheese(piecesOfCheese, mazeMap, mazeHeight, mazeWidth)
    print("Mauvais graph=",graphOfCheese)
    print("")
    bestPath,bestLength= travellingSalesman(graphOfCheese, playerLocation, piecesOfCheese)  #use of travellingSalesman to find the bestPath
  
    indice0=piecesOfCheese.index(bestPath[0])
    indice1=piecesOfCheese.index(bestPath[1])
    pathCheese=graphOfCheese[indice0][indice1][1]
    indice0=piecesOfCheese.index(bestPath[0])
   
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
    global bestPath, graphOfCheese, pathCheese, listOfCheese
    if len(pathCheese)>1:
    	Move = move(mazeMap, pathCheese[0], pathCheese[1])
    	pathCheese = pathCheese[1:]
    	return Move 
    elif len(bestPath)>2 : #sinon problème pour chercher l'indice1
        bestPath=bestPath[1:]
        indice0=listOfCheese.index(bestPath[0])
        indice1=listOfCheese.index(bestPath[1])
        pathCheese=graphOfCheese[indice0][indice1][1]
        Move = move(mazeMap, pathCheese[0], pathCheese[1])
        pathCheese = pathCheese[1:]
        return Move 
    else:
        Move = move(mazeMap,playerLocation, bestPath[0])
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



###################################################################
  
# This function returns the shortest path in the graph going through all nodes
def travellingSalesman (graphCheese, sourceNode, piecesOfCheese) :
 
    # We store the best path here
    bestLength = float("inf")
    bestPath = None

    # Thus function takes as an argument the nodes that are not visited yet, the graph and a current location
    # In addition, we remember the currently crossed path and the associated weight
    # Basically, we perform a depth-first search and study the path length if it contains all nodes
    def exhaustive (remainingNodes, currentNode, currentPath, currentLength, graphCheese) :
        
        # If no nodes are remaining, we have a path comprising all nodes
        # We save it as the best if it is better than the current best
        if not remainingNodes :
            nonlocal bestLength, bestPath
            if currentLength < bestLength :
                bestLength = currentLength
                bestPath = currentPath
        
        # If some nodes are remaining, we perform a depth-first search
        # We increase the path and its length in the recursive call
        # Obviously, we only consider nodes that are reachable
        else :
            for neighbor in piecesOfCheese :
                weight=graphCheese[piecesOfCheese.index(currentNode)][piecesOfCheese.index(neighbor)][0]
                if neighbor in remainingNodes :
                    otherNodes = [x for x in remainingNodes if x != neighbor]
                    exhaustive(otherNodes, neighbor, currentPath + [neighbor], currentLength + weight, graphCheese)
    
    # We initiate the search from the source node
    otherNodes = [x for x in piecesOfCheese if x != sourceNode] #tous les noeuds du graphe
    exhaustive(otherNodes, sourceNode, [sourceNode], 0, graphCheese)
    
    # We return the result
    return (bestPath, bestLength)
    #We will only use it to find the bestPath in the preprocessing

########

def shortestPathOptim(distances, predecessors, sourceNode, finalNode):
        #return (weight, shortest path from sourceNode to finalNode)
        pathToInverse=[finalNode]
        destination=finalNode
        while sourceNode not in pathToInverse:
            finalNode=predecessors[finalNode[0]][finalNode[1]] #Matrix again
            pathToInverse.append(finalNode)
        return distances[destination[0]][destination[1]],list(reversed(pathToInverse))


def graphCheeseOptim(piecesOfCheese, graph, mazeHeight, mazeWidth):
    #return a matrix whose elements are (weight, shortest path from location1 to location2), location will be a case where there is a cheese
   #graphCheeseIncomplet=[[ "hello" for i in range(len(piecesOfCheese))] for j in range(len(piecesOfCheese))]
   graphCheese=[["hello" for i in range(len(piecesOfCheese))] for j in range(len(piecesOfCheese))]
   for cheese in range(len(piecesOfCheese)):
      for nextCheese in range(cheese,len(piecesOfCheese)):
         
         (distances, predecessors)=dijkstra(graph, mazeHeight, mazeWidth, piecesOfCheese[cheese])
         graphCheese[cheese][nextCheese]=shortestPathOptim(distances,predecessors, piecesOfCheese[cheese], piecesOfCheese[nextCheese])
   
   for i in range(len(graphCheese)):
      for j in range(i+1,len(graphCheese)):
         
         graphCheese[j][i]=graphCheese[i][j]
         
         graphCheese[j][i]=(graphCheese[j][i][0],inverseListTuple(graphCheese[j][i][1]))
   return graphCheese
			


def shortestPath(graph, mazeHeight, mazeWidth, sourceNode, finalNode):
        #return (weight, shortest path from sourceNode to finalNode)
        (distances, predecessors)=dijkstra(graph, mazeHeight, mazeWidth, sourceNode)  #use of dijkstra 
        pathToInverse=[finalNode]
        destination=finalNode
        while sourceNode not in pathToInverse:
            finalNode=predecessors[finalNode[0]][finalNode[1]] #Matrix again
            pathToInverse.append(finalNode)
        return distances[destination[0]][destination[1]],list(reversed(pathToInverse))


def graphCheese(piecesOfCheese, graph, mazeHeight, mazeWidth):
    #return a matrix whose elements are (weight, shortest path from location1 to location2), location will be a case where there is a cheese
   graphCheese=[[None for i in range(len(piecesOfCheese))] for j in range(len(piecesOfCheese))]
   for cheese in piecesOfCheese:
      for nextCheese in piecesOfCheese:
         graphCheese[piecesOfCheese.index(cheese)][piecesOfCheese.index(nextCheese)]=shortestPath(graph,  mazeHeight, mazeWidth, cheese, nextCheese)
   return graphCheese

def inverseListTuple(liste):
   premier=liste.pop(-1) #le premier est le dernier
   dernier=liste[0]
   inverse=[premier]
   while dernier not in inverse:
      premier=liste.pop(-1)
      inverse.append(premier)
   return inverse


