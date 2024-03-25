import cv2
import os
import random

path = os.getcwd() + '/test_video_make/'

"""for [index, file] in enumerate(os.listdir(path)):
    image = cv2.imread(path+file, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (800, 600))
    cv2.imwrite(path+str(index)+'.jpg', image)
    os.remove(path+file)"""

fps = 120
image_size_x = 600
image_size_y = 400

for i in os.listdir(path):
    img = cv2.imread(path + i, cv2.IMREAD_COLOR)
    cur_dot_x = 0
    cur_dot_y = 0
    frame = []
    jump = 2
    for j in range(4):
        for k in range(100):
            for s in range(1):
                if j == 0:
                    img_new = img[cur_dot_y:cur_dot_y + image_size_y, cur_dot_x + k * jump:cur_dot_x + k * jump + image_size_x]
                elif j == 1:
                    img_new = img[cur_dot_y + k * jump:cur_dot_y + k * jump + image_size_y, cur_dot_x + 200:cur_dot_x + 200 + image_size_x]
                elif j == 2:
                    img_new = img[cur_dot_y + 200:cur_dot_y + 200 + image_size_y, cur_dot_x + 200 - k * jump:cur_dot_x + 200 - k * jump +image_size_x]
                elif j == 3:
                    img_new = img[cur_dot_y + 200 - k * jump:cur_dot_y + 200 - k * jump + image_size_y, cur_dot_x:cur_dot_x + image_size_x]
                frame.append(img_new)
    try:
        out = cv2.VideoWriter(os.getcwd() + '/test_video/' + i.split('.')[0] + '.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, (image_size_x, image_size_y))
        for t in range(len(frame)):
            # writing to a image array
            out.write(frame[t])
        out.release()
    except:
        print('error')

"""for j in range(120):
        img = cv2.imread(i)

        frameSize_y = img.shape[0]
        frameSize_x = img.shape[1]
        frameSize_x = frameSize_x + (30 - (frameSize_x % 30))
        frameSize_y = frameSize_y + (30 - (frameSize_y % 30))
        img = cv2.resize(img, (frameSize_x, frameSize_y))
        img_move = img[:, j:j]

        height, width, layers = img_move.shape
        size = (width, height)
        frame_array.append(img_move)
try:
    out = cv2.VideoWriter(os.getcwd() + '/temp/result.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
except:
    print('error')

for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()"""