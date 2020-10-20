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
inputFile = "C:/ENV859-GIS/ARGOSTracking/Data/ARGOSData/1997dg.txt"
outputFC = "C:/ENV859-GIS/ARGOSTracking/scratch/ARGOStrack.shp"

#%%Prepare new FC to add tracking points

#Create empty feature class, requires path & name as separate parameters
outPath, outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath, outName)

#%%Construct a while loop to iterate through all lines in the datafile

#Open the ARGOS data file for reading
inputFileObj = open(inputFile, "r")

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
        #Extract location info from the next line
        line2String = inputFileObj.readline()
        #Parse line into list
        line2Data = line2String.split()
        #Extract data we need to variables
        obsLat = line2Data[2]
        dateVal = lineData[3]
        TimeVal = lineData[4]
        LocClass = lineData[7]
        obsLon = line2Data[5]     
        #Print results to check so far
        print(tagID,"Lat:"+obsLat,"Long:"+obsLon,"Date:"+dateVal,"Time:"+TimeVal,"LC:"+LocClass)
    #Move to next line so loop progresses
    lineString = inputFileObj.readline()

#Close file object
inputFileObj.close()