Experiments with object detection, eg with the Yolo v3 DNN code from https://pjreddie.com/darknet/yolo/
and the version using NNPACK on a Pi, from http://funofdiy.blogspot.com/2018/08/deep-learning-with-raspberry-pi-real.html

For the first time, object detection with useful accuracy is feasible even CPU-only on a very small system.
Runs on Raspberry Pi 4 with 4GB RAM, taking about 3.5 seconds per 1280x720 image using the full YOLO-v3 network.
