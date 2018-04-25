#inixialize x_c to random values
#for i = 1 ... N
#	calculate 1/2(x_i - x_c)^2 for all c
#	assign x_i to the nearest x_c by an indicator function I(i, c)
#for c = 1 ... K
#	recompute X_c to be the center of gravity of all points assigned to C
#	X_C = ..
#
#
#repeat Until convergence
import random as rand
import math
import numpy as np
import matplotlib.pyplot as plt

###################################################################
# Function getDist
#
# Calculates a distance between two points using the Pythagorean Theorem.
# Z = sqrt(x^2 + Y^2)
# 
# Parameter x_i (array) : An array holding x and y data of a point.
#                         First index holds the x data, second index
#                         holds y data.
# Parameter x_c (array) : An array holding x and y data of a point.
#                         First index holds the x data, second index
#                         holds y data.
#
# returns a float value
#
def getDist(x_i, x_c):
    #print(x_i[0])
    xVector = abs(x_i[0] - x_c[0])
    yVector = abs(x_i[1] - x_c[1])
    zVector = math.sqrt(math.pow(xVector, 2) + math.pow(yVector, 2))
    #ret = 0
    #ret = (0.5) * math.pow(zVector , 2)
    return(zVector)


def soft(x_i, x_c, b):
    expo = -1 * b * getDist(x_i, x_c)
    ret = (0.5) * math.exp(expo)
    return(ret)

###################################################################
# Function indexOf
#
# Finds the index of the specified value.
# 
# Parameter list (array) : An array to be searched
# Parameter min          : The element to be searched for
#
# returns the index of the element
#
def indexOf(list, min):
    ret = -1;
    for i in range (0, len(list)):
        if(list[i] == min):
            ret = i;
    return(ret)

###################################################################
# Function center of gravity
#
# Finds the  "Center of gravity" for a specified cluster center
# based on its points
# 
# Parameter mat (array)  : The matrix/array containing the points
# Parameter c (int)      : The cluster number
#
# returns the location of the "center of gravity"
#
def centerOfGravity(mat, clustering, c):
    count = 0;
    retList = [];
    xRet = 0
    yRet = 0

    for i in range (0, len(mat)):
        #print(mat[i][2])
        if(clustering[i][c] == 1):
            count = count + 1
            #print(count)
            xRet = xRet + mat[i][0]
            yRet = yRet + mat[i][1]
            #xList.append(mat[i][0])
            #yList.append(mat[i][1])
    if(count == 0):
        return([0, 0]);
    return([xRet/count, yRet/count])
###################################################################
#Not used
def checkConvergence(x_c, c):
    ret = 1

    for i in range(0, c):
        for j in range(i, c):
            if(x_c[i] != x_c[j]):
                ret = 0

    return(ret)
###################################################################
#Comapres two arrays, returns 1 if the two arrays are identical.
#Returns 0 if there are defferences
def checkPrev(x_c, x_cPrev, c):
    ret = 1

    for i in range(0, c):
        if(x_c[i] != x_cPrev[i]):
            ret = 0
    return(ret)
###################################################################
#number of datapoints
n = 100
#number of clusters
cNum = 4
#Average value of datapoints
mu = 0
#distribution of datapoints
sigma = 0.1
mat = [] #points, a 2d appray
clustering = [] #Cluster assignment for points
xmat = np.random.normal(mu, sigma, 100)
ymat = np.random.normal(mu, sigma, 100)

#Creates the matrix contaiing data points.
for i in range (0, n):
    mat.append([xmat[i], ymat[i]])
    temp = []
    for c in range (0, cNum):
        temp.append(0)
    print(temp)
    clustering.append(temp)

#print(clustering)
#mat = [[1, 0, -1], [2, 4, -1], [5, 5, -1], [10, 1, -1], [9, 2, -1], [6, 4, -1], [7, 9, -1]]
#print(mat)

xc = [] #The current cluster position
xcPrev = [] #The previosu cluster position, used to check if cluster position as changed

#assigns cluster randomly
for i in range (0, cNum):
    xc.append([rand.randrange(1), rand.randrange(1)])
    #print(xc[i])
    xcPrev.append([])

print("-------------")

#xc.append([rand.randrange(10), rand.randrange(10)])
#xc.append([rand.randrange(10), rand.randrange(10)])

#print(xc)

nNum = len(mat)
cNum = len(xc)



#while(checkConvergence(xc, cNum) == 0 or checkConvergence(xc, xcPrev, cNum) == 0):
while(checkPrev(xc, xcPrev, cNum) == 0): #Keeps running unless there are no changes in cluster positions
    #print(xcPrev)
    #print(xc)

    #Saves cluster positions to compare later
    for i in range (0, cNum):
        xcPrev[i] = xc[i]
    #For all data points
    for i in range (0, nNum):
        distList = [] #Used to store the distances
        for c in range(0, cNum):
            temp = getDist(mat[i], xc[c]) #temp varaible, holds distance
            #print(prob)
            distList.append(temp)
            #print(temp)
        #print("total prob: ", totalprob)
        #print(distList)
        minIndex = indexOf(distList, min(distList)) #gets the index of the closest cluster
        #mat[i][2] = minIndex
        for x in range (0, len(clustering[i])): #writes 0 to every thing
            clustering[i][x] = 0
        clustering[i][minIndex] = 1 #sets minimum cluster index to 1
        #print(mat[i])
    for c in range(0, cNum): #Updates cluster positions
        #print(c)
        xc[c] = centerOfGravity(mat, clustering, c)
        #print(xc[c])
    #print(xcPrev)

#Plotting&graphinh
for i in range (0, nNum):
    if(clustering[i][0] == 1):
        plt.plot(mat[i][0], mat[i][1], 'ro')
    elif (clustering[i][1] == 1):
        plt.plot(mat[i][0], mat[i][1], 'bo')
    elif (clustering[i][2] == 1):
        plt.plot(mat[i][0], mat[i][1], 'go')
    else:
        plt.plot(mat[i][0], mat[i][1], 'yo')

for i in range (0, cNum):
    #plt.scatter(xc[i][0], xc[i][1], s=100)
    plt.plot(xc[i][0], xc[i][1], 'x')

#plt.scatter(xc[0][0], xc[0][1], s=100)
#plt.scatter(xc[1][0], xc[1][1], s=100)

plt.show()
#print(checkConvergence(xc, cNum));
#print(checkConvergence(xc, cNum));
