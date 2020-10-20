#%%---------------------------------------------------------------------------
#ImportARGOS.py
#Description: Read in ARGOS formatted tracking data and create a line feature
# class from the [filtered] tracking points
#Usage: ImportArgos <ARGOS folder> <Output feature class>
#Created: Fall 2020
#Author: cm498@duke.edu (for ENV859)
###---------------------------------------------------------------------------

#%%Import modules
import sys, os, arcpy

#Allow output overwrite
arcpy.env.overwriteOutput = True

#%%Set input variables (Hard-wired)
inputFolder = "C:/ENV859-GIS/ARGOSTracking/Data/ARGOSData"
inputFiles = os.listdir(inputFolder)
outputFC = "C:/ENV859-GIS/ARGOSTracking/scratch/ARGOStrack.shp"

#Create spatial reference variables
outputSR = arcpy.SpatialReference(54002)

#%%Prepare new FC to add tracking points

#Create empty feature class, requires path & name as separate parameters
outPath,outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath,outName,"POINT","","","",outputSR)

#Add TagID, LC, IQ, and Date fields to the output feature class
arcpy.AddField_management(outputFC,"TagID","LONG")
arcpy.AddField_management(outputFC,"LC","TEXT")
arcpy.AddField_management(outputFC,"Date","DATE")

#%%Create insert cursor
cur = arcpy.da.InsertCursor(outputFC,["Shape@","TagID","LC","Date"])

#%%Construct a for and while loop to iterate through all lines in the datafile for each file in folder

#Loop through each file in ARGOS folder
for inputFile in inputFiles:
    #Give some status
    print("Processing {}".format(inputFile))
    #Skip README.txt file
    if inputFile == "README.txt": continue
    #Append path to file
    inputFile = os.path.join(inputFolder,inputFile)
    #Open the ARGOS data file for reading
    inputFileObj = open(inputFile,"r")    
    #Get first line of data to use a while loop
    lineString = inputFileObj.readline()    
    #Start while loop

    while lineString:
        #Set code to run only if line contains string
        if ("Date :" in lineString):
            #Parse line into list
            lineData = lineString.split() #can examine to see where data elements found
            #Extract attributes from datum header line
            tagID = lineData[0]
            dateVal = lineData[3]
            TimeVal = lineData[4]
            LocClass = lineData[7]
            #Extract location info from the next line
            line2String = inputFileObj.readline()
            #Parse line into list
            line2Data = line2String.split()
            #Extract data we need to variables
            obsLat = line2Data[2]
            obsLon = line2Data[5]     
            #Try to convert coordinates to numbers
            try:
                #Convert raw coordinate strings to numbers
                if obsLat[-1] == 'N':
                    obsLat = float(obsLat[:-1])
                else:
                    obsLat = float(obsLat[:-1] * -1)
                if obsLon[-1] == 'W':
                    obsLon = float(obsLon[:-1])
                else:
                    obsLon = float(obsLon[:-1] * -1)
                #Construct point object from feature class
                obsPoint = arcpy.Point()
                obsPoint.X = obsLon
                obsPoint.Y = obsLat
                #Convert point to point geometry object w/ spatial reference
                inputSR = arcpy.SpatialReference(4326)
                obsPointGeom = arcpy.PointGeometry(obsPoint,inputSR)
                #Create feature object
                cur.insertRow((obsPointGeom,tagID,LocClass,dateVal.replace(".","/") + " " + TimeVal))
            #Handle any error
            except Exception as e:
                pass
        #Move to next line so loop progresses
        lineString = inputFileObj.readline()
    
    #Close file object
    inputFileObj.close()

#Delete the cursor object
del cur
