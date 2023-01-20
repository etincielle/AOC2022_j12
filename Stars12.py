def manhattanDistance(a,b) :
    return abs(a[0] - b[0]) + abs(a[1]-b[1])

def neighbours(x):
    return [(x[0]-1,x[1]),(x[0]+1,x[1]),(x[0],x[1]-1),(x[0],x[1]+1)]

def minTupleList(tupleList):
    weightList = []
    for tuples in tupleList :
        weightList.append(tuples[1])
    minimum = min(weightList)
    minIndex = weightList.index(minimum)
    return tupleList[minIndex]
    

class Node(object):
    def __init__(self,value, cordinates,neighbors = None):
        self.value = value
        self.cordinates = cordinates
        self.x = cordinates[0]
        self.y = cordinates[1]
        self.parent = None
        self.f = 0
        if value[0]=="S":
            self.height = 0
        elif value[0]=="E":
            self.height = 25
        else :
            for (height,letter) in enumerate("abcdefghijklmnopqrstuvwxyz") :
                if value[0] == letter :
                    self.height = height
        self.heuristic_value = -1
        if neighbors is None :
            self.neighbors = dict()
        else :
            self.neighbors = neighbors
        self.parent = None

    def has_neighbors(self):
        if len(self.neighbors)==0 :
            return False
        else :
            return True
    
    def add_neighbor(self,neighbor,cordinates):
        self.neighbors[cordinates] = (neighbor, manhattanDistance(self.cordinates,cordinates))
    
class Graph(object):
    def __init__(self, nodes = None):
        if nodes is None :
            self.nodes = dict()
        else :
            self.nodes = nodes
    def addNode(self, node, cordinates):
        self.nodes[cordinates] = node
    def findNode(self,cordinates):
        if cordinates in self.nodes :
            return self.nodes[cordinates]
    def addEdge(self,cordinates1,cordinates2):
        if cordinates1 != cordinates2 :
            node1 = self.findNode(cordinates1)
            node2 = self.findNode(cordinates2)
            if node1 and node2 :
                node1.add_neighbor(node2,cordinates2)
                node2.add_neighbor(node1,cordinates1)


    


with open("puzzle12.txt") as file :
    puzzle = file.read().splitlines()
    lowest = dict()
    e = ()
    openList = dict()
    closeList = dict()
    lines = len(puzzle)
    columns = len(puzzle[0])
    graph = Graph()
    # FINDING E AND S
    for i in range(lines) :
        for j in range(columns):
            if puzzle[i][j] == "E":
                e = (i,j)
            elif puzzle[i][j] == "S":
                lowest[(i,j)] = 0
            elif puzzle[i][j] == "a":
                lowest[(i,j)] = 0
    # COMPUTING THE MANHATTAN DISTANCE FOR EACH COORDINATES AND ADDING THEM TO THE GRAPH
    for i in range(lines) :
        for j in range(columns):
            node = Node(puzzle[i][j] + str(i) + str(j),(i,j))
            if node.value[0] == "S" :
                node.heuristic_value = 0
            else :
                node.heuristic_value = manhattanDistance((i,j), e)
            graph.addNode(node,(i,j))
    # ADDING EDGES TO THE GRAPH
    for i in range(lines) :
        for j in range(columns):
            for neighbor in neighbours((i,j)) :
                graph.addEdge((i,j),neighbor)

    # APPLYING A* ALGORITHM
    for s in lowest :
        print("Starting from ", graph.nodes[s].value)
        for node in graph.nodes.values() :
            node.parent = None
            node.f = 0
        graph.nodes[s].parent = None
        openList[s]=0
        closeList = dict()
        numberOfSteps = 0
        found = False
        #print(graph.nodes[(36,69)].neighbors[(35,69)][0].value)
        while len(openList) != 0 and not found:
            currentNode = min(openList, key=openList.get)
            #print(graph.nodes[currentNode].value, " ", end="")
            closeList[currentNode] = openList[currentNode]
            del openList[currentNode]
            if currentNode == e :
                print("Exit found !")
                parent = graph.nodes[currentNode].parent
                while parent != None:
                    parent = parent.parent
                    numberOfSteps += 1
                print("The most optimal path is :", numberOfSteps, "steps long.") 
                lowest[s]=numberOfSteps
                found = True
            for neighbor in graph.nodes[currentNode].neighbors.values() :
                if neighbor[0].height > graph.nodes[currentNode].height + 1 :
                    continue
                if neighbor[0].cordinates in closeList :
                    continue
                f = neighbor[0].heuristic_value + closeList[currentNode] + neighbor[1]
                neighbor[0].f = f
                if graph.nodes[currentNode].parent != neighbor[0] and neighbor[0].cordinates != s :
                    if neighbor[0].parent != None :
                        if graph.nodes[currentNode].f < neighbor[0].parent.f :
                            neighbor[0].parent = graph.nodes[currentNode]
                    else :
                        neighbor[0].parent = graph.nodes[currentNode]
                if neighbor[0].cordinates in openList :
                    if openList[neighbor[0].cordinates] < neighbor[1] :
                        continue
                openList[neighbor[0].cordinates] = f

notTooLows = []
for notTooLow in lowest.values() :
    if notTooLow > 100:
        notTooLows.append(notTooLow)

print("Minimum steps :", min(notTooLows))

    
