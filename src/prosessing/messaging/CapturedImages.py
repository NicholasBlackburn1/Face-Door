""" 
this class is for handling and detecting any new files in any of the captured output folders
and sending them to flask so they can be served to user via simple flask rest api
"""

import glob
import os


def getNewestCapturedImage(dir):
    list_of_files = glob.glob(dir+"*") # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print("Got Latest Image Now returning the output in "+ str(latest_file))