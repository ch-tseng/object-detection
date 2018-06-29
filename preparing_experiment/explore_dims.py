# USAGE
# python explore_dims.py --conf conf/cars.json

# import the necessary packages
from __future__ import print_function
from pyimagesearch.utils import Conf
from scipy import io
import numpy as np
import argparse
import glob
from xml.dom import minidom

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the configuration file")
ap.add_argument("-t", "--type", required=True, help="type of annotation file (xml or mat)")
ap.add_argument("-l", "--name", required=False, help="label's name. (for xml files)")
args = vars(ap.parse_args())

# load the configuration file and initialize the list of widths and heights
conf = Conf(args["conf"])
widths = []
heights = []

if(args["type"]=="mat"):
    # loop over all annotations paths
    for p in glob.glob(conf["image_annotations"] + "/*.mat"):
	# load the bounding box associated with the path and update the width and height
	# lists
        (y, h, x, w) = io.loadmat(p)["box_coord"][0]
        widths.append(w - x)
        heights.append(h - y)

else:
    # loop over all annotations paths
    for p in glob.glob(conf["image_annotations"] + "/*.xml"):
        labelName = []
        labelXstart = []
        labelYstart = []
        labelW = []
        labelH = []

        labelXML = minidom.parse(p)

        tmpArrays = labelXML.getElementsByTagName("name")
        for elem in tmpArrays:
            labelName.append(str(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("xmin")
        for elem in tmpArrays:
            labelXstart.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("ymin")
        for elem in tmpArrays:
            labelYstart.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("xmax")
        for elem in tmpArrays:
            labelW.append(int(elem.firstChild.data))

        tmpArrays = labelXML.getElementsByTagName("ymax")
        for elem in tmpArrays:
            labelH.append(int(elem.firstChild.data))

        for i in range(0, len(labelName)):
            if(args["name"]=='' or args["name"]==labelName[i]):
                widths.append(labelW[i]-labelXstart[i])
                heights.append(labelH[i]-labelYstart[i])

# compute the average of both the width and height lists
(avgWidth, avgHeight) = (np.mean(widths), np.mean(heights))
print("[INFO] avg. width: {:.2f}".format(avgWidth))
print("[INFO] avg. height: {:.2f}".format(avgHeight))
print("[INFO] aspect ratio: {:.2f}".format(avgWidth / avgHeight))
