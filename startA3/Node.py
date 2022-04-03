# Declan Hollingworth & Anshul Khatri
# 190765210 & 
# CP372 Assignment 3 
# Due: April 1st, 2022

# Imports
from common import *
import sys

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[0 for i in range(num)] for j in range(num)]
        # Changed 0 to i to default to the destination node instead of 0
        self.routes = [i for i in range(num)]
        # Create array for neighbors
        self.neighbors = []

        for i in range(num):
            for j in range(num):
                if i != j:
                    self.distanceTable[i][j] = self.ns.INFINITY # Set the current known cost to infinity
                else:
                    self.distanceTable[i][j] = 0 # Set to 0 if j = i

            if( (i != self.myID) and (costs[i] != self.ns.INFINITY) ):
                self.neighbors.append(i) #Add to neighbours
                packet = RTPacket(ID, i, costs) #Create packet of type RTPacket
                self.ns.tolayer2(packet) # Send the packet to update distance table
        
        #Set current distance table to the cost of the links connecting the node to the neighboring nodes
        self.distanceTable[ID] = costs


    def recvUpdate(self, pkt):
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        # Create a bool variable to track cost updates
        costUpdated = False
        
        # For each node in table
        for _ in range(self.ns.NUM_NODES):
            # Initial distance between current node (myID) and target node (sourceid)
            intitialDist = self.distanceTable[self.myID][pkt.sourceid]
            
            for i in range(self.ns.NUM_NODES):
                # Distance between the target node (sourceid) and another node (i)
                tempDistance = self.distanceTable[pkt.sourceid][i]
                # The current cost 
                currentCost = self.distanceTable[self.myID][i]
                
                # Check to see if new route costs less than current cost
                if( (i != self.myID) and (intitialDist + tempDistance < currentCost) ):
                    self.distanceTable[self.myID][i] = intitialDist + tempDistance
                    
                    # Update route and update bool variable
                    self.routes[i] = self.routes[pkt.sourceid]
                    costUpdated = True
                    
        # If cost was updated
        if(costUpdated == True):
            # Update all neighbours
            for i in range(len(self.neighbors)):
                packet = RTPacket(self.myID, self.neighbors[i], self.distanceTable[self.myID]) # Create packet of type RTPacket
                self.ns.tolayer2(packet) # Send the packet to update distance table
        
        return 

    
    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print() 
        
