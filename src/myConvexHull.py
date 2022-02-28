import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def findcoefconst(point1, point2): # Determine the equation of a line through point1 and point2
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    a = y2-y1
    b = -(x2-x1)
    c=(x2*y1)-(x1*y2)
    return a,b,c

def measuredistpoints(p1,p2): # Measure distance between two points
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    return math.sqrt((y2-y1)**2 + (x2-x1)**2)

def measuredist(p1,p2,pMeas): # Measure distance from a point to a line that lies on p1 p2
    x0 = pMeas[0]
    y0 = pMeas[1]
    a, b, c = findcoefconst(p1,p2)
    d = abs((a*x0)+(b*y0)+c)/(math.sqrt(a**2 + b**2))
    return d

def measureAngle(p1,p2,pRef): # Measure angle
    b = measuredistpoints(pRef, p1)
    c = measuredistpoints(pRef, p2)
    a = measuredistpoints(p1, p2)
    if(b != 0 and c != 0):
        cosAngle = (b**2+c**2-a**2)/(2*b*c)
        return math.degrees(math.acos(cosAngle))
    else:
        return 0

def leftestRightest(arrOfPoint): # Determine the most left and most right point in an array of points
    min = arrOfPoint[0][0]
    max = arrOfPoint[0][0]
    indeksMin = 0
    indeksMaks = 0
    for i in range(1, len(arrOfPoint)):
        if(arrOfPoint[i][0]<min):
            min = arrOfPoint[i][0]
            indeksMin = i
        if(arrOfPoint[i][0]>max):
            max = arrOfPoint[i][0]
            indeksMaks = i
    return arrOfPoint[indeksMin], arrOfPoint[indeksMaks]

'''Test case leftestRightest'''
# reskiri, reskanan = leftestRightest(arrOfPoint)
# print(f"Leftest: {reskiri}\n \nRightest: {reskanan}\n ")

def farthestPoint(arrOfPoint, p1, p2): # Find farthest point in arrOfPoint from a line that lies on p1 p2 
    max_dist = measuredist(p1, p2, arrOfPoint[0])
    indeksMaxDist = 0

    for i in range(1, len(arrOfPoint)):
        temp = measuredist(p1,p2, arrOfPoint[i])
        if(temp >= max_dist):
            if(temp == max_dist):
                angleTemp = measureAngle(p1, p2, arrOfPoint[i])
                angleCurrMax = measureAngle(p1, p2, arrOfPoint[indeksMaxDist])
                if(angleTemp >= angleCurrMax):
                    max_dist = temp
                    indeksMaxDist = i
                # else indeksMaxDist remain the same 
            else: # temp > max_dist
                max_dist = temp
                indeksMaxDist = i
    return arrOfPoint[indeksMaxDist]
    
def divideArea(arrOfPoint, p1, p2): # Divide area of an array of points where separate between a line that lies on p1 p2
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    leftSidePoint = [] # Left(above)
    rightSidePoint = [] # Right(below)

    for i in range(len(arrOfPoint)):
        xp3 = arrOfPoint[i][0]
        yp3 = arrOfPoint[i][1]

        valDet = (x1*y2)+(xp3*y1)+(x2*yp3)-(xp3*y2)-(x2*y1)-(x1*yp3)

        if(valDet>0):
            leftSidePoint.append(arrOfPoint[i])
        elif(valDet<0):
            rightSidePoint.append(arrOfPoint[i])
    return leftSidePoint, rightSidePoint

def convexHullParticular(arrOfPoint, lp, rp, category):
    arrOfHullPoint=np.array([])
    lp1 = lp.tolist()
    rp1 = rp.tolist()
    arrOfPoint = np.array([x for x in arrOfPoint if list(x) != lp1])
    arrOfPoint = np.array([x for x in arrOfPoint if list(x) != rp1])
    arrOfPointLeft, arrOfPointRight = divideArea(arrOfPoint, lp, rp)
    if(category == "above"):
        if(len(arrOfPointLeft) == 0):
            a = lp[0]
            b = lp[1]
            c = rp[0]
            d = rp[1]
            arrOfHullPoint = np.append(arrOfHullPoint, [[a, c],[b, d]])
        else:
            far = farthestPoint(arrOfPointLeft, lp, rp)
            list1 = convexHullParticular(arrOfPointLeft, lp, far, "above")
            list2 = convexHullParticular(arrOfPointLeft, far, rp, "above")
            arrOfHullPoint = np.append(arrOfHullPoint, list1)
            arrOfHullPoint = np.append(arrOfHullPoint, list2)
    elif(category == "below"):
        if(len(arrOfPointRight) == 0):
            a = lp[0]
            b = lp[1]
            c = rp[0]
            d = rp[1]
            arrOfHullPoint = np.append(arrOfHullPoint, [[a, c],[b, d]])
        else:
            far = farthestPoint(arrOfPointRight, lp, rp)
            list3 = convexHullParticular(arrOfPointRight, lp, far, "below")
            list4 = convexHullParticular(arrOfPointRight, far, rp, "below")
            arrOfHullPoint = np.append(arrOfHullPoint, list3)
            arrOfHullPoint = np.append(arrOfHullPoint, list4)
    arrOfHullPoint = np.reshape(arrOfHullPoint, (int(arrOfHullPoint.size/4), 2, 2))
    return arrOfHullPoint

def convexHull(arrOfPoint, lp, rp):
    resultAbove = convexHullParticular(arrOfPoint, lp, rp, "above")
    resultBelow = convexHullParticular(arrOfPoint, lp, rp, "below")
    result = np.vstack((resultAbove, resultBelow))
    return result

'''TestCase for a small-size case'''
# np.random.seed(0)
# arrOfPoint = np.random.randint(1,10,size=(10,2))
# lp, rp = leftestRightest(arrOfPoint)
# result = convexHull(arrOfPoint, lp, rp)
# print(result)

# for pair in result:
#     plt.plot(pair[0], pair[1])
# plt.show()