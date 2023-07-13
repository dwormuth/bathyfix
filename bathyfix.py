# Python code to Adjust the depths in GPX files using meters, negative number are below normal.
# dwormuth 7/13/23

import argparse
import os.path
from pathlib import Path

# Defines
StartTag = "<gpxtpx:depth>"
EndTag = "</gpxtpx:depth>"
StartTagLen = len(StartTag)
EndTagLen = len(EndTag)
#adjustment = 99

# 7/10/23 DWW changing to using argparse per page 275 of Python in a Nutshell, v4
ap = argparse.ArgumentParser(description="Adjust the depths in GPX files using meters, negative number are below normal.")
ap.add_argument("-d","--depth",help="Enter adjustment in meters, negative are below normal", type=float,
                required=True, default=0.0)
ap.add_argument("-f","--file", required=True, help="File to read without extension (.GPX assumed)")
ns = ap.parse_args()
print(ns)

adjustment = ns.depth
file2read = ns.file

#if adjustment == 99:
#    print("Water level offsets are positive if above normal and negative if below normal.")
##    try:
#        adjustment = float(input('Enter water level offset in meters: '))
#        print(adjustment)
#    except ValueError:
#        print('Enter a valid float')
#        exit(996)

# Using readlines()
infile = "/Users/dwormuth/Documents/GIS_Data/ReefMaster/LongLakeBathy" + file2read[2:] + "/" + file2read + ".gpx"
txt_path = Path(infile)
#print(txt_path)
# 7/10/23 DWW Testing file existence

if not os.path.exists(infile):
    print("Input file does not exist")
    exit(999)

outfile = "/Users/dwormuth/Documents/GIS_Data/ReefMaster/LongLakeBathy" + file2read[2:] + "/" + file2read + "_n.gpx"
txt_path = Path(outfile)
txt_path.touch(exist_ok=True)
if not os.path.exists(outfile):
    print("Output file cannot be written")
    exit(998)

with open(infile, 'r') as file1, open(outfile, 'w') as file2:
    Lines = file1.readlines()
    count = 0

    for line in Lines:
        count += 1
        if count == 2:
            file2.write("<!-- " + "File has been normalized by subtracting " + str(adjustment) + " meters" + " -->\n")
        if line.find(StartTag) != -1:
            StartDepth = line.find(StartTag)
            EndDepth = line.find(EndTag)
            Depth = float(line[(StartDepth + StartTagLen):EndDepth])
            file2.write("<gpxtpx:atemp>" + str(Depth) + "</gpxtpx:atemp>\n")
            file2.write("<gpxtpx:depth>" + str(Depth - adjustment) + "</gpxtpx:depth>\n")
        else:
            file2.write(line)
