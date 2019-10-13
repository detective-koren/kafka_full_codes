#!/usr/bin/env python
# coding: utf-8


# For debugging :
# - run the server and remember the IP of the server
# And interact with it through the command line:
# echo -n "get" > /dev/udp/192.168.0.39/1080
# echo -n "quit" > /dev/udp/192.168.0.39/1080

import socket
import cv2
import sys
from threading import Thread, Lock
import sys
import time
import base64
from kafka import KafkaProducer
import os
import argparse

#arguments
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str)
parser.add_argument('--topic', type=str)
parser.add_argument('--images_dir_path', type=str)

args = parser.parse_args()


#settings
debug = True
jpeg_quality = 90
host = args.host
#host = '203.237.53.3:9092'
topic = args.topic
#topic = "test"
key = "value"
data = "get"
path = args.images_dir_path
#path = "/home/konan1/konan/producer/"


def get_ip(interface_name):
    """Helper to get the IP adresse of the running server
    """
    import netifaces as ni
    ip = ni.ifaddresses(interface_name)[2][0]['addr']
    return ip  # should print "192.168.100.37"

def send_frame(path, producer, topic):
    global data
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    fname_list = os.listdir(path)
    fname_list = sorted(fname_list)
    for i in range(len(fname_list)):
        if i == len(fname_list):
            print("append checksum")
            producer.send(topic, b"checksum")
        else:
            read_im = cv2.imread(path+fname_list[i],1)
            result, img = cv2.imencode('.jpg', read_im, encode_param)
            producer.send(topic, img.tobytes())
            print(path + fname_list[i])
            os.remove(path+fname_list[i])
        time.sleep(0.1)


class VideoGrabber(Thread):
    """A threaded video grabber.

    Attributes:
    encode_params ():
    cap (str):
    attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    def __init__(self, jpeg_quality):
        """Constructor.

        Args:
        jpeg_quality (:obj:`int`): Quality of JPEG encoding, in 0, 100.

        """
        Thread.__init__(self)
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.buffer = None
        self.lock = Lock()

    def stop(self):
        self.running = False
        self.cap.release()

    def get_buffer(self):
        """Method to access the encoded buffer.

        Returns:
        np.ndarray: the compressed image if one has been acquired. None otherwise.
        """
        if self.buffer is not None:
            self.lock.acquire()
            cpy = self.buffer.copy()
            self.lock.release()
            return cpy

    def run(self):
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue

            # JPEG compression
            # Protected by a lock
            # As the main thread may asks to access the buffer
            self.lock.acquire()
            result, self.buffer = cv2.imencode('.jpg', img, self.encode_param)
            self.lock.release()


running = True

producer = KafkaProducer(bootstrap_servers=[host])

while(running):
    try:
        if data == "get":
            path_mod = path
            topic_mod = topic
            print("current path: " + path_mod)
            print("current topic: " + topic_mod)
            send_frame(path_mod, producer, topic_mod)
            if True:
                data = "end"
                print("sended")
        elif data == "end":
            running = False
            break
    except KeyboardInterrupt:
        running = False
        break

print("Quitting..")
