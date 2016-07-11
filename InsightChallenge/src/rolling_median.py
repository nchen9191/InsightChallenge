"""
Nelson Chen
nchen9191@gmail.com
06/09/2016

Insight Data Engineering Coding Challenge
Main Code
"""

from datetime import datetime
import json
import Graph
import sys

#Checks to see if this is duplicate edge between vertices
def isDuplicate(venmo,vertex1,vertex2):
    if vertex1 not in venmo.vertex_list or vertex2 not in venmo.vertex_list:
        return False
    elif vertex2 not in venmo.graph_dict[vertex1]:
        return False
    else:
        return True

#Converts the input line strings of names and time
def getTransaction(venmo_line):
    skip = False
    temp = json.loads(venmo_line)
    vertex1 = temp['actor']
    vertex2 = temp['target'] 
    timestamp = temp['created_time']
    if not vertex1 or not vertex2 or not timestamp:
        skip = True
    #converts time string to datetime object for easy comparison
    timestamp_datetime = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    return vertex1, vertex2, timestamp_datetime, skip

#Updates the latest time stamp and adds nodes and edges appropriately
def updateGraph(venmo,vertex1,vertex2,timestamp_datetime,latest_time):
    if timestamp_datetime > latest_time:
        latest_time = timestamp_datetime
        #if edge does not already exist, add edge to graph, else only update time
        if isDuplicate(venmo,vertex1,vertex2) == False:
            venmo.add_edge(vertex1,vertex2,timestamp_datetime)
    elif (latest_time - timestamp_datetime).total_seconds() <= 60:
        if isDuplicate(venmo,vertex1,vertex2) == False:
            venmo.add_edge(vertex1,vertex2,timestamp_datetime)      
    return latest_time
    
# Iterates through edge list to remove any old edges and updates accordingly
def removeOldEdges(venmo,latest_time):
    for j in range(len(venmo.edge_list)-1,-1,-1):
        edge = venmo.edge_list[j]
        time_diff = (latest_time - edge.timestamp).total_seconds()
        if time_diff > 60:
            venmo.remove_edge(edge)
           
#main executable part
def main():
    #input and output paths from system arguments       
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    #opens text files to read and write
    venmo_input = open(input_file)
    venmo_output = open(output_file, 'w')
    
    #initialize venmo graph and earliest possible time
    venmo = Graph.graph()
    latest_time = datetime(1,1,1,0,0,1)
    
    #loop through input until there are no more entries
    while True:

        #Get transaction
        venmo_line = venmo_input.readline()
        if venmo_line == '' or venmo_line == '\n': #stop loop when there are
            break                                  #no more transactions
        else:
            vertex1, vertex2, timestamp_datetime, skip = getTransaction(venmo_line)
            if skip == False:
                #update Graph and retrieves latest time
                latest_time = updateGraph(venmo,vertex1,vertex2,timestamp_datetime,latest_time)
            
                #evict edges from graph that are older than 60 seconds
                removeOldEdges(venmo,latest_time)
        
                #writes medians to output file
                venmo_output.write('%.2f\n'%venmo.get_median())
       
    #closes text files        
    venmo_input.close()
    venmo_output.close()
    
#execute main code if you call it 
if __name__ == '__main__':
    main()