# https://bong-sik.tistory.com/16
# https://deep-learning-study.tistory.com/299

import os
import cv2
import numpy as np

path = os.getcwd() + '/training4/'

net = cv2.dnn.readNet(os.getcwd()+"/yolo/yolov3.weights", os.getcwd()+"/yolo/yolov3.cfg")  # 학습데이터 로드(DNN)
classes = []
with open(os.getcwd()+"/yolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]  # 아마도 양옆 공백 없에서 한줄씩 저장하는것 같음(아마 라벨링)
print('학습된 클래스:'+str(classes))  # 총80개
layer_names = net.getLayerNames()  # 아마도 레이어명
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  # 마지막 레이어 식별
colors = np.random.uniform(0, 255, size=(len(classes), 3))  # 0~255 사이의 (라벨, 3)의 랜덤난수 배열 생성(클래스별로 색생 다르게표시)


for folder in os.listdir(path):
    for file in os.listdir(path+folder):
        print(file)
        img = cv2.imread(path + folder + "/" + file)  # 이미지 로드
        # img = cv2.resize(img, (1920, 1080))
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        print(img.shape[1], img.shape[0])
        # img = cv2.resize(img, None, fx=1.8, fy=1.8)  # 크기 0.4배
        img = cv2.resize(img, (416, 416))
        height, width, channels = img.shape

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # 블롭객체 생성

        # img=이미지, 0.00392=영상픽셀에 곱해줄 개수, (416, 416)=크기(허용되는크기는 (320x320), (609x609), (416x416)뿐임), (0,0,0)=각채널별 빼주는값, True=R,B채널 교환할것인가, False=Crop여부

        # cv2.dnn.blobFromImage => 1개 블롭
        # cv2.dnn.blobFromImages => 여러개의 블롭

        net.setInput(blob)  # 네트워크 인풋 설정
        outs = net.forward(output_layers)  # 네트워크 순방향 설정

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]  # 출력층의 5~85는 학습된 80개의 라벨링정보 나머지 0~4는 기타정보라서 뺀걸까?
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # 0~1의 예측도(신뢰도)
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # 좌표
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])  # 박스바운딩 좌표정보 및 크기정보
                    confidences.append(float(confidence))  # 신뢰도정보
                    class_ids.append(class_id)
                    print('found')

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  # 박스 중복 제거

        font = cv2.FONT_HERSHEY_PLAIN  # 폰트
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 2, color, 2)
                # cv2.imshow("Image", cv2.resize(img, (400,400)))
                img = cv2.resize(img, None, fx=0.75, fy=0.75)
                # img = cv2.resize(img, None, fx=2.25, fy=2.25)
                cv2.imshow("Image", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()