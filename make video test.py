import cv2
import os
import numpy as np

path = os.getcwd() + '/videos/'
new_path = os.getcwd() + '/videos/new/'

video = cv2.VideoCapture(path + '7.mp4')
videoFPS = video.get(cv2.CAP_PROP_FPS)
videoX = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
videoY = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(videoFPS)
print(videoX)
print(videoY)

new_video = []


def draw_m(event, x, y, flags, param):
    global ix, iy
    global px, py
    if event == cv2.EVENT_LBUTTONDOWN:                                                  #좌클릭을 했을때 약간 개념을 up down을 버튼이라 생각하면 됨. 각종 이벤트 처리 : https://deep-learning-study.tistory.com/110
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:                                                  #좌클릭을 때었을때
        px, py = x, y

retval, frame = video.read()
cv2.namedWindow('M to Draw')
cv2.imshow('M to Draw', frame)
cv2.setMouseCallback('M to Draw', draw_m)
cv2.waitKey(0)
print(ix, iy, px, py)

while(1):
    try:
        retval, frame = video.read()
        if not retval:  # maybe not used
            print('End')
            break
        frame = frame[iy:py, ix:px]
        new_video.append(frame)
    except:
        pass

try:
    out = cv2.VideoWriter(new_path + '7.mp4', cv2.VideoWriter_fourcc(*'XVID'), videoFPS, (px-ix, py-iy))
    for t in new_video:
        # writing to a image array
        out.write(t)
    out.release()
except Exception as e:
    print(e)