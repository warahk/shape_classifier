from scipy import stats
import numpy as np
import Image
import Harris
import math
import csv

objList = ["Acute",
           "Hexagon",
           "Obtuse",
           "Octagon",
           "Parallel",
           "Pentagon",
           "Rectangle",
           "Right",
           "Square",
           "Trap"]

##############Function: knn_search####################
##  Purpose:    Perform knn search on dataset.
##  Input:      x = Feature vector in list. Format: [nCorner, angleVar, sideRatioAvg]
##              D = 2d array of data in list form; row format same as above.
##              K = number of neighbors to check.
##  Output:     The shape classifcation of record x.
######################################################
def knn_search(x, D, K):
    """ find K nearest neighbours of data among D """
    ndata = len(D)
    K = K if K < ndata else ndata

    pointDistance = []

    ##Loop to find distance between all points of dataset
    for line in D:
        xdist = float(line[0]) - float(x[0])
        ydist = float(line[1]) - float(x[1])
        zdist = float(line[2]) - float(x[2])
        totaldist = math.sqrt( (xdist**2) + (ydist**2) + (zdist**2)) #Pythagorean theorem

        #build list of distances and their class
        pointDistance.append([totaldist, line[3]]) 

    #sort by their distances in ascending order
    pointDistance = sorted(pointDistance, key= lambda pClass: pClass[0])

    dataClass = 0
    cList = []
    for x in range(len(objList)):
        cList.append(0)
    
    for line in pointDistance[:K]:
        if (line[1] == "Acute"):
            cList[0] += 1
        elif(line[1] == "Hexagon"):
            cList[1] += 1
        elif(line[1] == "Obtuse"):
            cList[2] += 1
        elif(line[1] == "Octagon"):
            cList[3] += 1
        elif(line[1] == "Parallel"):
            cList[4] += 1
        elif(line[1] == "Pentagon"):
            cList[5] += 1
        elif(line[1] == "Rectangle"):
            cList[6] += 1
        elif(line[1] == "Right"):
            cList[7] += 1
        elif(line[1] == "Square"):
            cList[8] += 1
        elif(line[1] == "Trap"):
            cList[9] += 1

##    print cList

    cIndex = cList.index(max(cList))        

    return objList[cIndex]
#################END knn_search##################


##############Function: acquire_features##############
##  Purpose:    Extract our desired features from an image
##  Input:      fname = file path of the desired image
##  Output:     Feature vector of image in python list
######################################################
def acquire_features(fname):

    im = np.array(Image.open(fname).convert("L"))

    imThresh = stats.threshold(im, 0, 140, 255)

    harrisim = Harris.compute_harris_response(imThresh)

    filtered_coords = Harris.get_harris_points(harrisim, 10, 0.1)

    numCorner = len(filtered_coords)  #Feature 1

    angle_list = []
    sratio_list = []

    for base in filtered_coords:
        angleMax = 0
        ratioMax = 0
        for firstLine in filtered_coords:
            if (not((firstLine[0] == base[0]) and (firstLine[1] == base[1]))):
                fxdif = firstLine[0] - base[0]  #get vector x component
                fydif = firstLine[1] - base[1]  #get vector y component
                fmag = math.sqrt( fxdif**2 + fydif**2) #get vector magnitue

                fxdif = fxdif / fmag            #Normalize Vector
                fydif = fydif / fmag            #Normalize Vector         
                
                for testLine in filtered_coords:
                    if (not((testLine[0] == base[0]) and (testLine[1] == base[1]))):
                        txdif = testLine[0] - base[0]  #get vector x component
                        tydif = testLine[1] - base[1]  #get vector y component
                        tmag = math.sqrt( txdif**2 + tydif**2) #get vector magnitue

                        txdif = txdif / tmag            #Normalize Vector
                        tydif = tydif / tmag            #Normalize Vector

                        dotprod = ((txdif * fxdif) + (tydif * fydif))

                        if (dotprod < 1.0):
                            curAngle = math.degrees(math.acos(dotprod))
                            if (curAngle > angleMax):
                                angleMax = curAngle
                                if (fmag > tmag):
                                    ratioMax = fmag / tmag;
                                else:
                                    ratioMax = tmag / fmag;
                ###End innermost loop
        ###End of middle loop
        angle_list.append(angleMax) #Acquire angle
        sratio_list.append(ratioMax) #Acquire side length ratio
        
    ###End for loop
    avar = 0

    alen = len(angle_list)
    rlen = len(sratio_list)

    amean = sum(angle_list) / alen
    rmean = sum(sratio_list) / rlen

    for x in angle_list:
        avar = avar + ((x - amean)**2 / alen)

    astd = math.sqrt(avar)

    return [numCorner, astd, rmean]
##############End of acquire_features#############

def main():
    """Driver for knn search of our design data"""

    fvec = acquire_features('Images\AcuteT.png')

    neighbors = int(raw_input("How many neighbors: "))
    data = []

    with open("sDesignData.txt") as tsv:
        for line in csv.reader(tsv, delimiter="\t"):
            data.append(line)

    print knn_search(fvec, data, neighbors)

if __name__ == "__main__":
    main()
