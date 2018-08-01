import random
import math
import time
from sets import Set
#------------------------------------------------------------------------
NoOfClusters    = 4000       #Number of times you want to cluster
N               = 4000       #NUMBER OF POINTS
MaxCoordinate   = 90000.0

ax = []
ay = []

class Cluster:
    x=0           #Resultant X-Coordinate of this cluster
    y=0           #Resultant Y-Coordinate of this cluster
    clus_str=""   #Cluster String
    total_clus=0  #Number of clusters in this cluster
    
#------------------------------------------------------------------------
#Efficient Algo

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def closest_split_pair(p_x, p_y, delta, best_pair):
    ln_x = len(p_x)  # store length - quicker
    mx_x = p_x[ln_x // 2].x  # select midpoint on x-sorted array
    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array
    s_y = [X for X in p_y if mx_x - delta <= X.x <= mx_x + delta]
    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair[0], best_pair[1], best
 
def brute(ax):            #related to closest_pair. Not complete brute
    mi = dist(ax[0], ax[1])
    p1 = ax[0]
    p2 = ax[1]
    ln_ax = len(ax)
    if ln_ax == 2:
        return p1, p2, mi
    for i in range(ln_ax-1):
        for j in range(i + 1, ln_ax):
            if i != 0 and j != 1:
                d = dist(ax[i], ax[j])
                if d < mi:  # Update min_dist and points
                    mi = d
                    p1, p2 = ax[i], ax[j]
    return p1, p2, mi

def closest_pair(ax, ay):
    ln_ax = len(ax)  # It's quicker to assign variable
    if ln_ax <= 3:
        return brute(ax)  # A call to bruteforce comparison
    mid = ln_ax // 2  # Division without remainder, need int
    Qx = ax[:mid]  # Two-part split
    Rx = ax[mid:]
    # Determine midpoint on x-axis
    midpoint = ax[mid].x  
    Qy = list()
    Ry = list()
    for A in ay:  # split ay into 2 arrays using midpoint
        if A.x <= midpoint:
           Qy.append(A)
        else:
           Ry.append(A)
    # Call recursively both arrays after split
    (p1, q1, mi1) = closest_pair(Qx, Qy)
    (p2, q2, mi2) = closest_pair(Rx, Ry)
    # Determine smaller distance between points of 2 arrays
    if mi1 <= mi2:
        d = mi1
        mn = (p1, q1)
    else:
        d = mi2
        mn = (p2, q2)
    # Call function to account for points on the boundary
    (p3, q3, mi3) = closest_split_pair(ax, ay, d, mn)
    # Determine smallest distance for the array
    if d <= mi3:
        return mn[0], mn[1], d
    else:
        return p3, q3, mi3


def binarySearchX (arr, l, r, X):
    if r >= l:
        mid = l + (r - l)/2
        if arr[mid].x == X:
            return mid
        elif arr[mid].x > X:
            return binarySearchX(arr, l, mid-1, X)
        else:
            return binarySearchX(arr, mid+1, r, X)
    else:
        print "Could not find X.error" + str(X) + "------------------------------------------------------------------------"
        S = len(arr)
        for a in range(0,S):
            if arr[a].x == X:
                print "Did By O(n)"
                return a
                
##        print ""
##        print "AX"
##        printObj(ax)
##        print "AY"
##        printObj(ay)
        return -1
    
def binarySearchY (arr, l, r, Y):
    if r >= l:
        mid = l + (r - l)/2
        if arr[mid].y == Y:
            return mid
        elif arr[mid].y > Y:
            return binarySearchY(arr, l, mid-1, Y)
        else:
            return binarySearchY(arr, mid+1, r, Y)
    else:
        print "Could not find Y.error" + str(Y)+ "------------------------------------------------------------------------"
        S = len(arr)
        for a in range(0,S):
            if arr[a].y == Y:
                print "Did By O(n)"
                return a
##        print ""
##        print "AX"
##        printObj(ax)
##        print "AY"
##        printObj(ay)

        return -1
#------------------------------------------------------------------------------
#Initialization of Points list
Points = []
BPoints = []

def fillPointsList():
    global Points, MaxCoordinate, N,BPoints

    xTaken = Set()
    yTaken = Set()

    for i in range(0,N):
        tempObj = Cluster()

        randx = round(random.uniform(0.0, MaxCoordinate),2)
        randy = round(random.uniform(0.0, MaxCoordinate),2)

        if(randx not in xTaken):
            tempObj.x = randx
            xTaken.add(randx)
        else:
            tempObj.x = randx + round(random.uniform(0, MaxCoordinate-randx-1),2)    #just hope this is not taken
            xTaken.add(tempObj.x)
            
        if(randy not in yTaken):
            tempObj.y = randy
            yTaken.add(randy)
        else:
            tempObj.y = randy + round(random.uniform(0, MaxCoordinate-randy-1),2)    #just hope this is not taken
            yTaken.add(tempObj.y)
        
        tempObj.clus_str = str(i)
        tempObj.total_clus=1

        Points.append(tempObj)
        
        
    del xTaken
    del yTaken

def fillBPointsList():
    global BPoints
    
    for tempObj in Points:
        
        BtempObj = Cluster()
        BtempObj.x = tempObj.x
        BtempObj.y = tempObj.y
        BtempObj.clus_str = tempObj.clus_str
        BtempObj.total_clus=1
        BPoints.append(BtempObj)
#------------------------------------------------------------------------------

def newCluster(ob1,ob2):                   

    if(ob1.x > ob2.x):
        ob1,ob2 = ob2,ob1
           
    ob2x    =ob2.x
    ob2y    =ob2.y
    tc      =ob2.total_clus
    clus_str=ob2.clus_str

    S = len(ax)-1
    
    index1x = binarySearchX(ax,0,S,ob1.x)
    index2x = binarySearchX(ax,0,S,ob2.x) #Cluster one
    index1y = binarySearchY(ay,0,S,ob1.y)
    index2y = binarySearchY(ay,0,S,ob2.y) #Cluster one

    
            
    ob2.total_clus = ob1.total_clus + tc
    ob2.x = round( (((ob1.x * ob1.total_clus) + (ob2x * tc)) / ob2.total_clus),2)
    ob2.y = round( (((ob1.y * ob1.total_clus) + (ob2y * tc)) / ob2.total_clus),2)
    ob2.clus_str = "("+ ob1.clus_str + "," + clus_str + ")"
    
    return index1x,index2x,index1y,index2y
    
#------------------------------------------------------------------------------
#Efficient Main

def alterAX(index1x,index2x):
    global ax
    
   #ob2x should be greater. Pop index1x. index2x got replaced by clusteredobject
   #index2x is the index of this replaced clusteredobject and shift it to top until we get correct place
                                                       

    for ClusI in range(index2x,0,-1):                   #Max number of iterations will be index2x-index1x
        if(ax[ClusI].x < ax[ClusI-1].x):
            ax[ClusI], ax[ClusI-1] = ax[ClusI-1], ax[ClusI]
        else:
            break

    ax.pop(index1x)
    
        
    
def alterAY(index1y,index2y):                                 #index2y must be the new clusteredObj index.We'll remove index1y. If index2y is greater, compare upwards
    global ay

    if(index2y > index1y):
        for ClusI in range(index2y,0,-1):                  
            if(ay[ClusI].y  < ay[ClusI-1].y):
                ay[ClusI], ay[ClusI-1] = ay[ClusI-1], ay[ClusI]
            else:
                break

        ay.pop(index1y)
    else:
        ay.pop(index1y)
        S = len(ay)-1
        for ClusI in range(index2y,S):                  
            if(ay[ClusI].y  > ay[ClusI+1].y):
                ay[ClusI], ay[ClusI+1] = ay[ClusI+1], ay[ClusI]
            else:
                break

    
        

#We'll process ax, ay which will initially contain all the Elements in Points list sorted in corresponding axis
#and at each iteration we remove two objects from it and replace them with corresponding Cluster object
#in the correct place.
# <Removed> We'll also append this cluster object to ClusterList (Done by newCluster Function) which will be used to show graphics

def Main(NoOfClusters):
    global ax,ay

    for i in range(0,NoOfClusters):
        if(len(ax) > 1 and len(ay) > 1):
            global ax,ay
            
            ob1, ob2, d = closest_pair(ax,ay)             #O(n log n) operation
            #print "Original ob1 and ob2:X" + str(ob1.x) + " " + str(ob2.x) + " Y:" + str(ob1.y) + " " + str(ob2.y)
            
            index1x,index2x,index1y,index2y = newCluster(ob1,ob2)                  #this will replace ob2 with the new clustered values.

            #print index1x,index2x,index1y,index2y
            
##            print ""
##            print "AX Before: "
##            printObj(ax)
            alterAX(index1x,index2x)           #It will remove the ob1, and place clustered object(i.e ob2) in right place

##            print ""
##            print "AX After"
##            printObj(ax)
##            
##
##            print ""
##            print "AY Before: "
##            printObj(ay)
            
            alterAY(index1y,index2y)           #O(n) Operation

##            print ""
##            print "AY After"
##            printObj(ay)
        else:
            break        
    
#------------------------------------------------------------------------------
#Brute Force Main

def calDist():
    S = len(BPoints)

    leastD = float("inf")
    Li = -1
    Lj = -1
    
    for i in range(0,S):
        for j in range(0,i):
            d = dist(BPoints[i],BPoints[j])
            if(d<leastD):
                Li,Lj,leastD = i,j,d
            
    
    return Li,Lj

def AlterBPoints(Li,Lj):
    global BPoints

    ob1 = BPoints[Li]
    ob2 = BPoints[Lj]
    
    ob2x    =ob2.x
    ob2y    =ob2.y
    tc      =ob2.total_clus
    clus_str=ob2.clus_str
    
    ob2.total_clus = ob1.total_clus + tc
    ob2.x = round( (((ob1.x * ob1.total_clus) + (ob2x * tc)) / ob2.total_clus),2)
    ob2.y = round( (((ob1.y * ob1.total_clus) + (ob2y * tc)) / ob2.total_clus),2)
    ob2.clus_str = "("+ ob1.clus_str + "," + clus_str + ")"

    BPoints.pop(Li)

def MainBrute(NoOfClusters):
    
    for k in range(0,NoOfClusters-1):
        Li,Lj = calDist()
        AlterBPoints(Li,Lj)
        
#------------------------------------------------------------------------------
def printObj(list):
    for i in range(0,len(list)):
        print str(list[i].x) + " " + str(list[i].y) + " " #+ list[i].clus_str

def printFinalCluster():

    maxSize = -1
    ret_obj = Points[0]
    for obj in Points:
        if(obj.total_clus>maxSize):
            maxSize = obj.total_clus
            ret_obj = obj

    print str(ret_obj.x) + " " + str(ret_obj.y) + " " #+ ret_obj.clus_str

def iniVariablesAndStart(isBrute):
    global ax,ay,Points,NoOfClusters,N

    if(not isBrute):
        fillPointsList()
        fillBPointsList()
        
        start_time=time.time()    
        ax = sorted(Points, key=lambda a: a.x)      # Presorting x-wise
        ay = sorted(Points, key=lambda a: a.y)      # Presorting y-wise

        Main(NoOfClusters)
        stop_time=time.time()
      
        print ""
        print "N=" + str(N)
            
        print "Total time for clustering: " + str(stop_time-start_time) + "secs  " + str((stop_time-start_time)/60) + "Min"
        print "Final Cluster X, Y"
        printFinalCluster()
    else:
        
        start_time=time.time()    
        MainBrute(NoOfClusters)
        stop_time=time.time()
      
        print ""
        print "N=" + str(N)
            
        print "Total time for Brute force clustering: " + str(stop_time-start_time) + "secs  " + str((stop_time-start_time)/60) + "Min"
        print "Final Cluster X, Y"
        printObj(BPoints)


#------------------------------------------------------------------------------   
isBrute = False
iniVariablesAndStart(isBrute)

print "#-------------#"

isBrute = True
iniVariablesAndStart(isBrute)



