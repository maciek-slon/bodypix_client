import requests
import sys

import cv2
import numpy as np



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
    cv2.waitKey(-1)

def query(fname):
    files = {'file': open(fname,'rb')}
    r = requests.post("http://127.0.0.1:8081/upload", files=files)
    resp = r.content
    nparr = np.frombuffer(resp, np.uint8)
    img = cv2.imread(fname)
    mask = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    show(img, mask)

if __name__=="__main__":
    query(sys.argv[1])
