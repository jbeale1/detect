#!/home/pi/.virtualenvs/cv/bin/python3

# Run Yolo-v3 in interactive mode, effectively as a server process.  
# Feed it images, use detected areas to crop out detected objects
# Yolo v3 needs image height and width to be multiple of 32
# J.Beale 23-Dec-2019

import subprocess 
import threading
from time import sleep
import os, fcntl    # iterate over files
import sys          # sys.exit()
import cv2
# ================================================================

inpath = "/home/pi/yinput/"    # directory of images to process
outpath = "/home/pi/youtput/"  # detected crops saved here

folder = os.fsencode(inpath)

filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpg', '.png') ): # get the images
        filenames.append(filename)

filenames.sort() # os.listdir gives them in random order

print("First file: %s\n" % filenames[0])

# start darknet process. Note: detections below 50% are more often wrong than right

"""
yolo_proc = subprocess.Popen(["./darknet",
                   "detect",
                   "./cfg/yolov3-tiny.cfg",
                   "./yolov3-tiny.weights",
                   "-thresh","0.5"],
                   stdin = subprocess.PIPE, stdout = subprocess.PIPE)

"""
yolo_proc = subprocess.Popen(["./darknet",
                   "detect",
                   "./cfg/yolov3.cfg",
                   "./yolov3.weights",
                   "-thresh","0.5"],
                   stdin = subprocess.PIPE, stdout = subprocess.PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
# ===========================================

i = 0
rl = 0

print("Started Yolo\n")

while True:
        yline = yolo_proc.stdout.readline()  # get one line from process as string
        scount = len(yline)
        sleep(0.5)
        if scount>0:  # any non-whitespace in output line?
          rl += 1                # increment count of returned lines
          yout = yline.decode('ascii')

          if "Enter Image Path" in yout:
            try:
              fpath = inpath + filenames[i]
              fpathcr = fpath + '\n'
            except:
              print("All done: files = %d\n" % i)  # exit when finished with all files
              sys.exit()

            print("\nFile %d: %s" % (i,fpath))
            to_yolo = str.encode(fpathcr)  # encode as byte array (?)
            yolo_proc.stdin.write(to_yolo)
            yolo_proc.stdin.flush()  # without this nothing happens
            i += 1
          elif "Predicted in" in yout:
            print(yout)
          else:
            fname = os.path.basename(fpath.strip())  # base filename
            fbase = os.path.splitext(fname)[0]  # pathname without '.jpg' and '\n'
            fout = outpath + fbase
            # yout example string: 'person: 95.0% 1: Crop: 268x550+552+438'

            detclass = yout.split(':')[0]  # detected class eg. 'car', 'person' etc.
            detclass = detclass.replace(' ', '-')  # replace spaces with dashes, eg "stop-sign"
            detidx = yout.split(':')[1].split(' ')[-1]  # index of detection within this image
            detconf = yout.split(':')[1].split(' ')[-2]   # confidence %
            print("detected class = %s : %s" % (detclass,detconf) ) # display detected class (maybe more than one word?)
            gspec = yout.split(':')[-1].strip()
            cstr = "convert " + fpath + " -crop " + gspec + ' ' + fout + '_' + detclass + '_' + detidx + '.jpg'
            # print(cstr)  # full command string
            conv_proc = subprocess.Popen(cstr.split(' ')) # execute the crop command
