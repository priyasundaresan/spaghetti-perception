import cv2
import os
import numpy as np

def preprocess(img):
    H,W,C = img.shape
    new_img = cv2.resize(img.copy(), (int(W/2), int(H/2)))
    return new_img

def subtract(img, background_img):
    img = preprocess(img)
    background_img = preprocess(background_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    background_img_gray = cv2.cvtColor(background_img, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(background_img_gray.astype("uint8"), img_gray)
    threshold = 40
    thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow('img', np.hstack((img, background_img)))
    #cv2.imshow('img', thresh)
    result = np.vstack((np.hstack((img_gray, background_img_gray)), np.hstack((diff, thresh))))
    cv2.imshow('img', result)
    cv2.waitKey(0)

if __name__ == '__main__':
    background_img = cv2.imread('output/00000.jpg')
    img_dir = 'output'
    for fn in sorted(os.listdir(img_dir)):
        img_fn = os.path.join(img_dir, fn)
        img = cv2.imread(img_fn)
        subtract(img, background_img)
