import cv2
import os
import random

category = ['waterCar', 'waterPerson']
loadPath = os.getcwd() + '/training/'
savePath = os.getcwd() + '/training4/'

try:
    os.mkdir(savePath)
except:
    pass
try:
    os.mkdir(savePath+category[0])
except:
    pass
try:
    os.mkdir(savePath+category[1])
except:
    pass

for label, cate in enumerate(category):
    print(cate)
    # indexOfCar = len(os.listdir(savePath + category[0] + '/'))
    file_index = []
    for index, fileName in enumerate(os.listdir(loadPath+cate)):
        print(loadPath + cate + '/' + fileName)
        image = cv2.imread(loadPath + cate + '/' + fileName)
        image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(savePath + cate + '/' + cate + str(index+1).zfill(6) + '.jpg', image)

    for files in os.listdir(savePath+cate):
        file_index.append(files)
    random.shuffle(file_index)
    train = int(len(file_index) * 0.8)
    valid = int(len(file_index) - train)
    print(train)
    print(valid)
    # print(file_index)
    for new_index in range(train):
        file1 = open('train.txt', 'a')
        file1.write('./build/darknet/x64/data/obj/' + str(file_index[new_index]) + '\n')
        file1.close()
    for new_index in range(valid):
        file2 = open('test.txt', 'a')
        file2.write('./build/darknet/x64/data/obj/' + str(file_index[train + new_index]) + '\n')
        file2.close()

    # file = open('D:/DirectLink/YoloCustomModel/windows_v1.8.0/windows_v1.8.0/data/train.txt', 'a')
    """with open('D:/DirectLink/YoloCustomModel/windows_v1.8.0/windows_v1.8.0/data/train.txt', 'wb') as file:
        file.write(('data/img/' + str(index * 4 + 1).zfill(6) + '.jpg\n').encode())
        file.write(('data/img/' + str(index * 4 + 2).zfill(6) + '.jpg\n').encode())
        file.write(('data/img/' + str(index * 4 + 3).zfill(6) + '.jpg\n').encode())
        file.write(('data/img/' + str(index * 4 + 4).zfill(6) + '.jpg\n').encode())"""
    # for i in range(4):
    # if label == 0:
    # file.write('data/img/' + cate + '/' + str(index * 4 + (i + 1)).zfill(6) + '.jpg\n')
    # elif label == 1:
    # file.write('data/img/' + cate + '/' + str(index * 4 + (i + 1) + indexOfCar).zfill(6) + '.jpg\n')
    # file.close()