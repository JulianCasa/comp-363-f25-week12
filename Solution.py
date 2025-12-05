import copy
def find_path(graph: list[list[int]], source: int, target: int):

    """Return a path -- any path -- from source to target in the graph"""

    # Initialize return item
    path: list[int] = None

    # Make sure inputs are ok
    if graph is not None:
        n: int = len(graph)
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            # Initialize DFS tools
            no_edge: int = graph[0][0]  # absence of edge
            marked: list[int] = [source]  # vertices already processed
            found: bool = False  # Flags detection of path

            # What vertex to explore next and what is the path
            # to it. The information is stored as a tuple in
            # the form:
            #  (vertex, path_to_this_vertex)
            # with path_to_this_vertex being a list of the
            # vertices alonγ the path.
            stack: list[(int, list[int])] = [(source, [source])]

            while len(stack) > 0 and not found:
                # Explore the next vertex from the stack
                (u, path_from_source_to_u) = stack.pop()
                found = (u == target)
                if found:
                    # u is the end of the path, so we got what we are 
                    # looking for
                    path = path_from_source_to_u
                else:
                    # Explore the neighbors of u, hopefully one of them
                    # will get us a stop closer to the target vertex.
                    v: int = n - 1
                    while v >= 0:
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1
    return path

def find_path_flow(graph, source, target):
    #Creates a variable called path and is assigned the value given by find path
    path = find_path(graph, source, target)

    #Checks to see if a path is even possible
    if not path:
        pathFlow = None
    else:
        #Calculates the minimum flow along the path and assigns it to pathflow
        pathFlow = min([graph[path[i]][path[i+1]] for i in range(len(path)-1)]) 

        #for loop that updates the graph with the new flows
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            graph[u][v] -= pathFlow
            graph[v][u] += pathFlow
    
    return pathFlow
     
def ford_fulkerson(graph, source, target):
    #Variable initialization
    maxFlow = 0
    residual = copy.deepcopy(graph)
    flowFound = True

    #While loop that keeps going until no flow is found
    while flowFound:
        #flow variable is assigned the value of find_path_flow
        flow = find_path_flow(residual, source, target)

        #checks to see if loop should continue otherwie it adds the current flow to the max flow
        if flow == None or flow == 0:
            flowFound = False
        else:
            maxFlow += flow

    #Calls min cut function and prints the result
    print(minCut(graph, residual, source))

   

    return maxFlow

def minCut(graph, residual, source):
    #Initialize S and stack
    S = []
    stack = [source]

    #Loops while the stack exists
    while stack:
        #Grabs the last element
        u = stack.pop()
        #as long as its a valid edge it adds it to S and the stack
        for v in range(len(residual)):
            if residual[u][v] != residual[0][0] and v not in S:
                S.append(v)
                stack.append(v)

    #Initialize T and then fills it with the vertices not in S
    T = []

    for i in range(len(graph)):
        if i not in S:
            T.append(i)

    #creates the edges list and then fills it with the edges from S to T
    edges = []

    for u in S:
        for v in T:
            if graph[u][v] != graph[0][0]:
                edges.append((u, v))

    #Returns the s and t arrays along with the edges
    return S, T, edges





# Test graph
G = [#A  B  C  D  E
    [0, 20, 0, 0, 0],  # A
    [0, 0, 5, 6, 0],  # B
    [0, 0, 0, 3, 7],  # C
    [0, 0, 0, 0, 8],  # D
    [0, 0, 0, 0, 0],  # E
]

max_flow = ford_fulkerson(G, 0, 4)
print("Maximum possible flow: %d" %max_flow)


