"""
Nelson Chen
nchen9191@gmail.com
06/09/2016

Insight Data Engineering Coding Challenge
Graph and edge objects
"""

from numpy import median

#edges in graph, contains the source, target, and the time of creation        
class edge(object):
    def __init__(self,vertex1,vertex2,timestamp):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.timestamp = timestamp

#specialized graph object for venmo problem
class graph(object):
    
    def __init__(self):
        self.edge_list = [] #list of edges
        self.edge_count = [] #list of degrees
        self.vertex_list = [] #list of nodes in graph
        self.graph_dict = {} #dictionary for all connections in graph
        
    #adds vertex in graph if it is not there already, creates degree
    def add_vertex(self, vertex_name):
        if vertex_name not in self.graph_dict:
            self.graph_dict[vertex_name] = []
            self.vertex_list.append(vertex_name)
            self.edge_count.append(1)
            
    #remove vertex from the graph and degree list
    def remove_vertex(self,vertex_name):
        ind = self.vertex_list.index(vertex_name)
        del self.vertex_list[ind]
        del self.edge_count[ind]

    #add edge to graph and updates degree list and dictionary accordingly
    def add_edge(self, vertex1, vertex2,timestamp):    
        self.edge_list.append(edge(vertex1,vertex2,timestamp))        
        
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].append(vertex2)
            self.edge_count[self.vertex_list.index(vertex1)] += 1
        else:
            self.add_vertex(vertex1)
            self.graph_dict[vertex1] = [vertex2]
            
        if vertex2 in self.graph_dict:
            self.graph_dict[vertex2].append(vertex1)
            self.edge_count[self.vertex_list.index(vertex2)] += 1
        else:
            self.add_vertex(vertex2)
            self.graph_dict[vertex2] = [vertex1]
            
    #remove edge from graph and updates degree list and dictionary accordingly
    def remove_edge(self, edge):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        
        ind1 = self.vertex_list.index(vertex1)
        if self.edge_count[ind1] == 1:
            self.remove_vertex(vertex1)
            self.graph_dict.pop(vertex1)
        else:
            self.edge_count[ind1] -= 1
            self.graph_dict[vertex1].remove(vertex2)
            
        ind2 = self.vertex_list.index(vertex2)
        if self.edge_count[ind2] == 1:
            self.remove_vertex(vertex2)
            self.graph_dict.pop(vertex2)
        else:
            self.edge_count[ind2] -= 1
            self.graph_dict[vertex2].remove(vertex1)
            
        self.edge_list.remove(edge)

    #returns the median of the degree list using numPy's median function
    def get_median(self):
        return median(self.edge_count)

