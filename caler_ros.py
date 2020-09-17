import requests
import sys

import cv2
import numpy as np

import rospy
import roslib

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from datetime import datetime

def show(img, mask):
    mask2 = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11, 11)))
    mask2 = cv2.GaussianBlur(mask2, (29, 29), 0)
    mask2 = cv2.subtract(mask2, mask)
    mask2 = cv2.GaussianBlur(mask2, (5, 5), 0)
    green = np.zeros(img.shape, np.uint8)
    green[:] = (0, 255, 0)
    mask2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
    mask2 = mask2 / 255.
    res = mask2 * green + (1-mask2) * img
    res = res.astype(np.uint8)
    cv2.imshow("IMG_RES", res)
    key = cv2.waitKey(10)
    if key == 115: # s
        now = datetime.now()
        cv2.imwrite("/tmp/" + now.strftime("%H%M%S") + "_c.jpg", img)
        cv2.imwrite("/tmp/" + now.strftime("%H%M%S") + "_m.png", mask)
        cv2.imwrite("/tmp/" + now.strftime("%H%M%S") + "_r.jpg", res)

def query(fname):
    files = {'file': open(fname,'rb')}
    r = requests.post("http://192.168.18.232:8081/upload", files=files)
    resp = r.content
    nparr = np.frombuffer(resp, np.uint8)
    img = cv2.imread(fname)
    mask = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    show(img, mask)

def callback(data):
    global bridge
    cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imwrite("/tmp/img.jpg", cv_image)
    query("/tmp/img.jpg")

if __name__=="__main__":
    rospy.init_node('caller', anonymous = True)
    try:
        global bridge
        bridge = CvBridge()
        image_sub = rospy.Subscriber("/xtion/rgb/image_rect_color", Image, callback, queue_size=1)
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
