# https://bong-sik.tistory.com/16
# https://deep-learning-study.tistory.com/299

import os
import cv2
import numpy as np
import time


if __name__ == '__main__':
    pass


def video_test_yolov4(video_path):
    net = cv2.dnn.readNet(os.getcwd() + "/yolo/yolov4.weights", os.getcwd() + "/yolo/yolov4.cfg")  # 학습데이터 로드(DNN)
    classes = []
    with open(os.getcwd() + "/yolo/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]  # 아마도 양옆 공백 없에서 한줄씩 저장하는것 같음(아마 라벨링)
    print('학습된 클래스:' + str(classes))  # 총80개
    layer_names = net.getLayerNames()  # ['conv_0', 'bn_0', 'relu_1', 'conv_1', 'bn_1', 'relu_2' ...]
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  # 여러 레이어들중에 감지된 아웃풋 레이어만을 저장
    print(output_layers)
    colors = np.random.uniform(0, 255, size=(len(classes), 3))  # 0~255 사이의 (라벨, 3)의 랜덤난수 배열 생성(클래스별로 색생 다르게표시)

    video = cv2.VideoCapture(video_path)
    FPS = video.get(cv2.CAP_PROP_FPS) * 2
    time_prev = time.time()
    while(1):
        time_cur = time.time() - time_prev
        if time_cur > 1 / FPS:
            retval, frame = video.read()  # 반환값은 True,False --> retval
            if not retval:  # maybe not used
                print('Replay')
                break
            img = frame.copy()
            # img = cv2.GaussianBlur(img, (5, 5), 0)
            # print(img.shape[1], img.shape[0])
            # img = cv2.resize(img, None, fx=0.4, fy=0.4)  # 크기 0.4배
            height, width, channels = img.shape

            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # 블롭객체 생성 (CNN등에 넣어야할 이미지 전처리가 쉬워지는 장점)
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
                    scores = detection[5:]  # 출력층의 5~85는 학습된 80개의 라벨링정보 나머지 0~3는 좌표 및 크기 정보, 4는 모름
                    class_id = np.argmax(scores)  # 가장 높은 값을 지정해준 이유는 class confidence
                    confidence = scores[class_id]  # 각 값들은 한 클래스에 대한 신뢰도 정보를 가짐
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

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  # 박스 중복 제거

            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, 2, color, 2)
            # cv2.imshow("Image", cv2.resize(img, (400,400)))
            # img = cv2.resize(img, None, fx=0.75, fy=0.75)
            # img = cv2.resize(img, None, fx=2.25, fy=2.25)
            img = cv2.resize(img, (600, 400))
            cv2.imshow("Image", img)
            time_prev = time.time()
            if cv2.waitKey(1) & 0xFF == ord('q'):  # q를 누르면 종료 ord는 문자열을 아스키코드 반환
                break
    video.release()
    cv2.destroyAllWindows()


video_test_yolov4(os.getcwd() + '/test_video/16.mp4')