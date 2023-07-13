# Python code to
# demonstrate readlines()

import getopt, sys
import argparse
import errno
import os.path

from pathlib import Path

# Defines
StartTag = "<gpxtpx:depth>"
EndTag = "</gpxtpx:depth>"
StartTagLen = len(StartTag)
EndTagLen = len(EndTag)

#adjustment = 0.9

#L = ["Geeks\n", "for\n", "Geeks\n"]
L = ["              <extensions>\n",
                    "<gpxtpx:TrackPointExtension>\n",
                        "<gpxtpx:wtemp>26.44</gpxtpx:wtemp>\n",
                        "             <gpxtpx:depth>1.96</gpxtpx:depth>\n",
                    "</gpxtpx:TrackPointExtension>\n",
               " </extensions>\n"]
#options = "hmf:d:"
adjustment = 99
# Remove 1st argument from the
# list of command line arguments
#argumentList = sys.argv[1:]

# Long options
#long_options = ["Help", "My_file", "File=", "Depth="]

# try:
#     # Parsing argument
#     arguments, values = getopt.getopt(argumentList, options, long_options)
#
#     # checking each argument
#     for currentArgument, currentValue in arguments:
#         #print("Looking")
#         if currentArgument in ("-h", "--Help"):
#             print("Used -d or --Depth for depth, -f or --File for input file")
#
#         elif currentArgument in ("-m", "--My_file"):
#             print("Displaying file_name:", sys.argv[0])
#
#         elif currentArgument in ("-f", "--File"):
#             print(("Using filename (%s)") % (currentValue))
#             file2read = currentValue
#
#         elif currentArgument in ("-d", "--Depth"):
#             try:
#                 adjustment = float(currentValue)
#                 print(str(adjustment))
#             except ValueError:
#                 print('Enter a valid float')
#             print(("Depth (% s)") % (currentValue))
#         else:
#             print("Nothing found")
#
# except getopt.error as err:
#     # output error, and return with an error code
#     print(str(err))

#print("nope")
# this accepts the user's input
# and stores in inp

# 7/10/23 DWW changing to using argparse per page 275 of Python in a Nutshell, v4
ap = argparse.ArgumentParser(description="Adjust the depths in GPX files using meters, negative number are below normal.")
ap.add_argument("-d","--depth",help="Enter adjustment in meters, negative are below normal", type=float,
                required=True, default=0.0)
ap.add_argument("-f","--file", required=True, help="File to read")
ns = ap.parse_args()
print(ns)

adjustment = ns.depth
file2read = ns.file

if adjustment == 99:
    print("Water level offsets are positive if above normal and negative if below normal.")
    try:
        adjustment = float(input('Enter water level offset in meters: '))
        print(adjustment)
    except ValueError:
        print('Enter a valid float')
        exit(996)
# writing to file
#file1 = open('myfile.txt', 'w')
#file1.writelines(L)
#file1.close()

# Using readlines()
infile = file2read + ".gpx"
txt_path = Path(infile)
print(txt_path)
# 7/10/23 DWW Testing file existence
#try:
if not os.path.exists(infile):
    print("Input file does not exist")
    exit(999)

# except FileNotFoundError as err:
#     print(f'Input file does not exist {err.filename!r}')
#     exit(999)
# except OSError as oserr:
#     print(f'Input file does not exist 2 - {errno.errorcode[oserr.errno]}')
#     exit(997)

outfile = file2read + "_n.gpx"
txt_path = Path(outfile)
txt_path.touch(exist_ok=True)
if not os.path.exists(outfile):
    print("Output file cannot be written")
    exit(998)
        #file1 = open(infile, 'r')

with open(infile, 'r') as file1, open(outfile, 'w') as file2:
    Lines = file1.readlines()
    count = 0
        # Strips the newline character
    for line in Lines:
        count += 1
        if count == 2:
            file2.write("<!-- " + "File has been normalized by subtracting " + str(adjustment) + " meters" + " -->\n")
        if line.find(StartTag) != -1:
            StartDepth = line.find(StartTag)
            EndDepth = line.find(EndTag)
            Depth = float(line[(StartDepth + StartTagLen):EndDepth])
        #        print(Depth)
            file2.write("<gpxtpx:atemp>" + str(Depth) + "</gpxtpx:atemp>\n")
            file2.write("<gpxtpx:depth>" + str(Depth - adjustment) + "</gpxtpx:depth>\n")
        else:
            file2.write(line)

    #print("Line{}: {}".format(count, line.strip()))

    #count = 0
#        file2.close()
    #file2 = open('myfile2.txt', 'r')
    #Lines2 = file2.readlines()
    #for line2 in Lines2:
    #    count += 1
    #    print("Line{}: {}".format(count, line2.strip()))