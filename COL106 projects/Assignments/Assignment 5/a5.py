# assignment 5 


class Empty(Exception):
    pass

class Heap():
    class Item:

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __lt__(self, other):
            return self.key < other.key

    def is_empty(self):
        return len(self.data) == 0
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def add(self, key, value):
        self.data.append(self.Item(key, value))
        self.heap_up(len(self.data) - 1)

    def max(self):
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        item = self.data[0]
        return (item.key, item.value)

    def remove_max(self):
        if self.is_empty():
            raise Empty('Priority queue is empty.')
        self.swap(0, len(self.data) - 1)
        item = self.data.pop()
        self.heapdown(0)
        return (item.key, item.value)

    def parent(self, j):
        return (j - 1) // 2

    def left(self, j):
        return 2 * j + 1

    def right(self, j):
        return 2 * j + 2

    def has_left(self, j):
        return self.left(j) < len(self.data)

    def has_right(self, j):
        return self.right(j) < len(self.data)

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def heap_up(self, j):
        parent = self.parent(j)
        if j > 0 and self.data[j] > self.data[parent]:
            self.swap(j, parent)
            self.heap_up(parent)

    def heapdown(self, j):
        if self.has_left(j):
            left = self.left(j)
            big_child = left
            if self.has_right(j):
                right = self.right(j)
                if self.data[right] > self.data[left]:
                    big_child = right 
            if self.data[big_child] > self.data[j]:
                self.swap(j, big_child)
                self.heapdown(big_child)

def route(parentlist, vertex):
    # takes list of parents and a vertex and returns the route from the source to the vertex if it exits.
    # current vertex is the target .
    path = []
    while parentlist[vertex] != vertex:
        path.append(vertex)
        vertex = parentlist[vertex]
    path.append(vertex) # append source vertex
    path.reverse()      
    return path

def MaximumCapacityRoute(cap_vertex_list, s, t):
    # cap_vertex_list is a list of lists of tuples (capacity, vertex) where each list represent a vertex corresponding to index.
    # and capacity is the capacity of the edge between the vertex and the vertex in the tuple.
    # s is the source vertex and t is the target vertex.
    
    max_packet_from_s = [0 for i in range(len(cap_vertex_list))] # list of max packets from s to each vertex.
    explored = [False for i in range(len(cap_vertex_list))]       # list of explored vertices.
    parent_list = [0 for i in range(len(cap_vertex_list))]        # list of parents of each vertex.

    Unexplored = Heap()                                             # heap of unexplored vertices.
    Unexplored.add(0,s)    #key is the max packet from s to the vertex and value is the vertex.                      
    max_packet_from_s[s] = float("inf")                              # max packet from s to s is infinity.
    parent_list[s] = s                                              # parent of s is s. to terminate the route function.
    count=0
    while len(Unexplored)>0:                        # while there are unexplored vertices.
        max_till_now = Unexplored.remove_max()      # remove the vertex with the max packet from s.
        u = max_till_now[1]                         
        explored[u] = True                          # mark it as explored.
        current_source = max_till_now[1]                                # current source is the vertex with the max packet from s.
       
        for i in range(len(cap_vertex_list[current_source])):          # for each vertex connected to the current source.
            vertex = cap_vertex_list[current_source][i]                # vertex is a tuple (capacity, vertex).                 

            if explored[vertex[1]] == False:                             
                a = min(max_packet_from_s[current_source], vertex[0])   # find the min of the max packet from s to the current source and the capacity of the edge.
                b = max_packet_from_s[vertex[1]]                        # max packet from s to the adjacent vertex.
                new_max = max(a,b)                                          
                if (new_max > max_packet_from_s[vertex[1]]):            # if the new max is greater than the old max.
                    max_packet_from_s[vertex[1]] = new_max              # update the max packet from s to the adjacent vertex.
                    parent_list[vertex[1]] = current_source             # update the parent of the adjacent vertex.
                    Unexplored.add(new_max, vertex[1])  
                                    # add the adjacent vertex to the heap.
                    
  
    x = route(parent_list, t)                   # find the route from s to t.
    return ( max_packet_from_s[t], x)          # return the max packet from s to t and the route.

def findMaxCapacity(n,links, s,t):
    # n is the number of vertices.
    # links is a list of tuples (u,v,capacity) where u and v are vertices and capacity is the capacity of the edge between them.
    # s is the source vertex and t is the target vertex.
    
    cap_vertex_list = [[] for i in range(n)]        # list of lists of tuples (capacity, vertex) where each list represent a vertex corresponding to index.
   
    for i in range(len(links)):           # for each link.
        cap_vertex_list[links[i][0]].append((links[i][2], links[i][1])) 
        cap_vertex_list[links[i][1]].append((links[i][2], links[i][0]))   

    return MaximumCapacityRoute(cap_vertex_list,s,t)

