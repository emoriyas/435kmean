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
    expo = -1 * b * math.pow(getDist(x_i, x_c), 2)
    print("expo:", expo)
    #print("dist:", getDist(x_i, x_c))
    ret = math.exp(expo)
    print("ret:", ret)
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
    xtot = 0
    ytot = 0
    xRet = 0
    yRet = 0
    ptot = 0

    for i in range (0, len(mat)):
        #print(mat[i])
        ptot = ptot + clustering[i][c]
        xtot = xtot + mat[i][0]
        ytot = ytot + mat[i][1]
        xRet = xRet + (clustering[i][c] * mat[i][0])
        #print(clustering[i][c])
        yRet = yRet + (clustering[i][c] * mat[i][1])
    #if(xtot == 0 or ytot == 0):
    #    print("aa")
    #    return([0, 0])
    #print(xRet, xtot)
    return([xRet/ptot, yRet/ptot])
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
n = 100
cNum = 4
mu = 10
sigma = 10
mat = [] #points
clustering = [] #Cluster assignment for points
xmat = np.random.normal(mu, sigma, 100)
ymat = np.random.normal(mu, sigma, 100)
b= 0.5

for i in range (0, n):
    #if (xmat[i]**2>=0.005 and ymat[i]**2>=0.005):
    #    mat.append([xmat[i], ymat[i], -1])
    mat.append([xmat[i], ymat[i]])
    temp = []
    for c in range (0, cNum):
        temp.append(0)
    #print(temp)
    clustering.append(temp)

print(clustering)
#mat = [[1, 0, -1], [2, 4, -1], [5, 5, -1], [10, 1, -1], [9, 2, -1], [6, 4, -1], [7, 9, -1]]
#print(mat)

xc = []
xcPrev = []

xc.append([0,0])
xc.append([10,10])
xc.append([10,0])
xc.append([0,10])

for i in range (0, cNum):
    #xc.append([ round(rand.uniform(-0.3, 0.3), 2), round(rand.uniform(-0.3, 0.3), 2)])
    #xc.append([np.random.normal(mu, sigma, 1), np.random.normal(mu, sigma, 1)])
    #print(xc[i])
    xcPrev.append([])

print("-------------")

#xc.append([rand.randrange(10), rand.randrange(10)])
#xc.append([rand.randrange(10), rand.randrange(10)])

#print(xc)

nNum = len(mat)
cNum = len(xc)



#while(checkConvergence(xc, cNum) == 0 or checkConvergence(xc, xcPrev, cNum) == 0):
while(checkPrev(xc, xcPrev, cNum) == 0):
#for a in range (0, 2):
    #print(xcPrev)
    print(xc)

    for i in range (0, cNum):
        xcPrev[i] = xc[i]
    for i in range (0, nNum):
        totalprob = 0;
        for c in range(0, cNum):
            temp = getDist(mat[i], xc[c])
            prob = soft(mat[i], xc[c], b);
            #print(prob)
            clustering[i][c] = prob
            #print(xc)
            #print(c, mat[c], prob)
            totalprob = totalprob + prob
            #print(temp)
        #print("total prob: ", totalprob)
        #print(distList)

        for c in range (0, len(clustering[i])):
            if (totalprob != 0):
                clustering[i][c] = clustering[i][c]/totalprob
            print("cluster prob:", clustering[i][c])

        #print(mat[i])
    for c in range(0, cNum):
        #print(c)
        xc[c] = centerOfGravity(mat, clustering, c)
        #print(xc[c])
    #print(xcPrev)

print(xc)

#print(clustering)

for i in range (0, nNum):
    minIndex = clustering[i].index(max(clustering[i]))
    if(minIndex == 0):
        plt.plot(mat[i][0], mat[i][1], 'ro')
    elif (minIndex == 1):
        plt.plot(mat[i][0], mat[i][1], 'bo')
    elif (minIndex == 2):
        plt.plot(mat[i][0], mat[i][1], 'go')
    else:
        plt.plot(mat[i][0], mat[i][1], 'yo')

for i in range (0, cNum):
    #plt.scatter(xc[i][0], xc[i][1], s=100)
    plt.plot(xc[i][0], xc[i][1], 's')

#plt.scatter(xc[0][0], xc[0][1], s=100)
#plt.scatter(xc[1][0], xc[1][1], s=100)

plt.show()
#print(checkConvergence(xc, cNum));
#print(checkConvergence(xc, cNum));
