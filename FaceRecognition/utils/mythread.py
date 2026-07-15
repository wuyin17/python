# 读取摄像头流的线程


import threading
from copy import deepcopy
import numpy as np
import cv2
thread_exit=True
thread_lock = threading.Lock()
import glob

import time as tim

import xml.dom.minidom as xmldom

class MyThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(MyThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        self.lock = threading.Lock()
    def get_frame(self):
        # with self.lock:
            return deepcopy(self.frame), self.img_width, self.img_height

    def run(self):
        global thread_exit
        print("self.camera_id", self.camera_id)
        cap = cv2.VideoCapture(self.camera_id)
        while thread_exit:
            ret, frame = cap.read()
            if ret:
                self.img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                # frame = cv2.resize(frame, (self.img_width, self.img_height))
                with self.lock:
                    self.frame = frame
                    cv2.waitKey(1)
            else:
                cap.release()
                cap = cv2.VideoCapture(self.camera_id)
        cap.release()