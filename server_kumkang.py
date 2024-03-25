import numpy as np
import cv2

import tkinter
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk

import PIL
from PIL import Image
from PIL import ImageTk

import time
import datetime as dt
import threading
import socket
import select
import os

import requests  # 웹 페이지의 HTML을 가져오는 모듈
from bs4 import BeautifulSoup  # HTML을 파싱하는 모듈


class curry:  # 함수 내포 기법에 사용할 클래스
    def __init__(self, func, *args, **kwargs):
        self.func = func  # 함수
        self.pending = args[:]  # 인자
        self.kwargs = kwargs.copy()  # 사전형 인자

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs
        return self.func(*(self.pending+args), **kw)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('__file__')))

    return os.path.join(base_path, relative_path)


def onPlayVideo():
    global video
    global videoUpdate
    global selectIndex
    global frame
    global label_video
    global select
    global boundary_temp
    global show_boundary
    global boundary_temp_read

    # while(select == -1):
        # pass
    # time.sleep(1)
    videoUpdate = False
    time_prev = time.time()
    while(1):
        selectIndex_video = selectIndex
        video = cv2.VideoCapture(videoURL[selectIndex_video])
        videoFPS = video.get(cv2.CAP_PROP_FPS)  # 초당 프레임 정보 불러옴
        print(video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 가로 세로 정보 출력
        while(1):
            time_cur = time.time() - time_prev
            try:
                if time_cur > 1 / videoFPS:
                    retval, frame = video.read()  # 반환값은 True,False --> retval
                    if not retval:  # maybe not used
                        print('Replay')
                        break
                    if videoUpdate == True:
                        print('New Video')
                        videoUpdate = False
                        boundary_temp = []
                        boundary_temp_read = []
                        break
                    try:
                        with open(os.getcwd() + '/camera_area/kumgang/' + str(selectIndex) + '.txt', 'r') as file_boundary_read:
                            boundary_temp_read = (file_boundary_read.readlines())
                        file_boundary_read.close()
                    except:
                        boundary_temp_read = []
                    TKImage_video = cv2.resize(frame, (320, 320))
                    if show_boundary == True:
                        if len(boundary_temp_read) != 0:
                            for frame_recv in range(len(boundary_temp_read)):
                                bound_x1, bound_y1, bound_x2, bound_y2 = boundary_temp_read[frame_recv].rstrip('\n').split('#')
                                bound_x1 = int(bound_x1)
                                bound_x2 = int(bound_x2)
                                bound_y1 = int(bound_y1)
                                bound_y2 = int(bound_y2)
                                TKImage_video = cv2.rectangle(TKImage_video, (bound_x1, bound_y1), (bound_x2, bound_y2), (0, 0, 255), 1)
                    TKImage_video = cv2.cvtColor(TKImage_video, cv2.COLOR_BGR2RGB)  # TKinter는 RGB중심
                    TKImage_video = PIL.Image.fromarray(TKImage_video)  # numpy 배열을 이미지객체화
                    imgtk_video = PIL.ImageTk.PhotoImage(image=TKImage_video)  # TKinter와 호완되는 이미지객체화

                    label_video.configure(image=imgtk_video)
                    label_video.image = imgtk_video

                    time_prev = time.time()
            except:
                # print('Time Error')
                time_prev = time.time()


def onPlayVideoUpdate():
    global video
    global videoUpdate
    global selectIndex

    selectIndex = selectCombo.current()
    if selectIndex == -1:
        messagebox.showinfo('Notice', '아무것도 선택할수는 없어요.')
    else:
        videoUpdate = True


def mini_video_click(event, num):
    global selectIndex
    global videoUpdate

    print(num)
    if num >= len(videoURL):
        pass
    else:
        selectIndex = num
        videoUpdate = True


def update_boundary(event):
    global boundary_temp
    global boundary1

    print(event.x)
    print(event.y)
    boundary1 = np.array([int(event.x), int(event.y)])


def update_boundary2(event):
    global boundary_temp

    print(event.x)
    print(event.y)
    boundary2 = np.array([int(event.x), int(event.y)])

    boundary_temp.append(np.array([boundary1, boundary2]))


def onShow_boundary():
    global show_boundary

    show_boundary = not(show_boundary)


def onDraw():
    global mainWindow
    global notebook
    global originalFrame
    global label_video
    global selectCombo

    global selectWindow
    global selectRiver
    global select

    global mini_video

    global text_logdata

    global weatherText

    mainWindow = tkinter.Tk()
    mainWindow.title("Main Window")
    mainWindow.geometry("860x860+100+000")
    mainWindow.resizable(False, False)
    mainWindow.iconphoto(False, tkinter.PhotoImage(file=resource_path('./river.png')))

    """if select == -1:
        selectWindow = tkinter.Tk()
        selectWindow.title("Select")
        selectWindow.geometry("300x120+400+400")
        selectWindow.resizable(False, False)

        selectRiver = ttk.Combobox(selectWindow, height=16, width=20, state="readonly", value=['한강', '낙동강', '금강'],
                                       postcommand=None)
        selectRiver.place(x=20, y=10)
        selectRiver.set("한강")

        selectRiverButton = tkinter.Button(selectWindow, text="확인", command=onRiver)
        selectRiverButton.place(x=200, y=10)"""

    TKImage_video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # TKinter는 RGB중심
    TKImage_video = PIL.Image.fromarray(TKImage_video)  # numpy 배열을 이미지객체화
    imgtk_video = PIL.ImageTk.PhotoImage(image=TKImage_video)  # TKinter와 호완되는 이미지객체화

    TKImage_video_mini = cv2.cvtColor(cv2.resize(frame, (120, 120)), cv2.COLOR_BGR2RGB)
    TKImage_video_mini = PIL.Image.fromarray(TKImage_video_mini)
    imgtk_video_mini = PIL.ImageTk.PhotoImage(image=TKImage_video_mini)

    exitIcon = PhotoImage(file=resource_path('./exit.png'))

    notebook = tkinter.ttk.Notebook(mainWindow, width=840, height=800)
    notebook.place(x=10, y=10)

    originalFrame = tkinter.Frame(mainWindow)
    notebook.add(originalFrame, text="일반")

    recordFrame = tkinter.Frame(mainWindow)
    notebook.add(recordFrame, text="기록창")

    menubar = Menu(mainWindow)  # 윈도우에 메뉴바 추가
    optionmenu = Menu(menubar, tearoff=0)  # 상위 메뉴 탭 항목 추가
    menubar.add_cascade(label="Menu", menu=optionmenu)  # 상위 메뉴 탭 설정
    optionmenu.add_command(label="Show Boundary", command=onShow_boundary)
    optionmenu.add_command(label="Edit IP Info", command=onOpen_IPTXT)
    optionmenu.add_separator()
    optionmenu.add_command(label="Add Test Data", command=onAddTestData)
    optionmenu.add_separator()
    optionmenu.add_command(label="Quit", command=mainWindow.quit, image=exitIcon, compound=LEFT)

    mainWindow.config(menu=menubar)

    seperator1 = tkinter.ttk.Separator(originalFrame, orient="vertical")  # 세로막대
    seperator1.place(x=120, y=0, relwidth=1, relheight=1)

    boundarySavebutton = tkinter.Button(originalFrame, text="Save Bound", command=onBoundary_save)
    boundarySavebutton.place(x=20, y=40)

    boundaryShowbutton = tkinter.Button(originalFrame, text="Show Bound", command=onShow_boundary)
    boundaryShowbutton.place(x=20, y=80)

    ipEditbutton = tkinter.Button(originalFrame, text="Edit IP Info", command=onOpen_IPTXT)
    ipEditbutton.place(x=20, y=120)

    allQuitbutton = tkinter.Button(originalFrame, text="Shut Down", command=mainWindow.quit)
    allQuitbutton.place(x=20, y=160)

    label_video = tkinter.Label(originalFrame, image=imgtk_video)
    label_video.place(x=140, y=20)  # 320 * 320
    label_video.bind("<Button-1>", update_boundary)
    label_video.bind("<ButtonRelease-1>", update_boundary2)

    selectCombo = ttk.Combobox(originalFrame, height=16, width=22, state="readonly", value=selectComboName, postcommand=updateSelectCombo)
    selectCombo.place(x=480, y=20)
    selectCombo.set("좌표 선택")

    videoSelectbutton = tkinter.Button(originalFrame, text="CCTV 선택", command=onPlayVideoUpdate)
    videoSelectbutton.place(x=680, y=20)

    weatherText = tkinter.Text(originalFrame, width=24, height=1)
    # weatherText.insert(tkinter.CURRENT, "현재 날씨 : ")
    weatherText.place(x=620, y=300)

    seperator1 = tkinter.ttk.Separator(originalFrame, orient="horizontal")  # 가로막대
    seperator1.place(x=120, y=360, relwidth=1, relheight=0)

    for mini_y in range(3):
        for mini_x in range(5):
            mini_video.append(tkinter.Label(originalFrame, image=imgtk_video_mini))
            mini_video[mini_y*5+mini_x].place(x=140 + 140 * mini_x, y=380 + mini_y * 140)
            mini_video[mini_y*5+mini_x].bind("<Double-Button-1>", lambda event, num=mini_y*5+mini_x: mini_video_click(event, num))  # "<Double-Button-1>"

    text_logdata = tkinter.Text(recordFrame, width=118, height=66)
    text_logdata.place(x=0, y=0)

    mainWindow.mainloop()


def updateSelectCombo():
    global selectComboName

    selectComboName = []
    for i in range(len(videoName)):
        selectComboName.append('[' + (str(i+1)).zfill(3) + '] : ' + videoName[i])
    selectCombo["values"] = selectComboName


def onInit():
    record_date = time.ctime()
    print('Server Activate : ' + str(record_date).replace(' ', '_'))
    record_time = int(record_date.split()[3].split(':')[0])

    try:
        os.mkdir(os.getcwd() + "/test/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/log/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/log/kumgang/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/log/hangang/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/log/nakdonggang/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/camera_area/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/camera_area/kumgang/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/camera_area/hangang/")
    except:
        pass
    try:
        os.mkdir(os.getcwd() + "/camera_area/nakdonggang/")
    except:
        pass


def onRegister():
    global videoName
    global videoURL
    global videoReg
    global videoSection
    global select

    global videoNumber

    if select == 0:  # http://www.hrfco.go.kr/sumun/cctvRtmp.do
        videoName.append('한강-군문교')
        videoReg.append('http://www.hrfco.go.kr/popup/cctvRtmpView.do?Obscd=1101635')

        for videos in videoReg:
            videoParts = requests.get(videos).text.split()
            for videoList in videoParts:
                if 'http:' in videoList and 'm3u8' in videoList:
                    videoURL.append(videoList.lstrip('"').rstrip('";'))  # 'http://59.18.117.222:7081/4fwXzHVtrvs+8hP08vy0AiNajVGUxYRMDiygTQq3nSA=.m3u8'
                    break
    elif select == 1:  # 사이트 증발함
        pass
    elif select == 2:
        videoName.append('금강-팔결교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3011635&chid=BOOKIL')
        # videoURL.append("http://59.18.117.222:7081/d0lgTS6dU/3hVQZPbdBW+b1yJw5Lmqq8Im3d9ps7JY8=.m3u8")
        # videoSection.append(np.array([(0, 192), (720, 480)]))

        videoName.append('금강-흥덕교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3011645&chid=CHUNGJU')
        # videoURL.append("http://59.18.117.222:7081/hqR8igF9RNGzRhxw/5GreFvfSQBYRoO5nXm7CnJZOkk=.m3u8")
        # videoSection.append(np.array([(0, 520), (1240, 680)]))

        # videoName.append('금강-미호천교')
        # videoURL.append("http://59.18.117.222:7081/rx54ORfELbLurgHyDBkJzFz0DYz7hqI9Q7GGj6n6gS8=.m3u8")
        # videoSection.append(np.array([(1200, 540), (1920, 1080)]))

        videoName.append('금강-세종리')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3012602&chid=SEJONG')
        # videoURL.append("http://59.18.117.222:7081/aDoiA1hjzm6Q1bu2QXjRfy84Ggq2BH/bdcdQROVuxnY=.m3u8")
        # videoSection.append(np.array([(0, 270), (1920, 1080)]))

        # videoName.append('금강-금강교')
        # videoURL.append("http://59.18.117.222:7081/4FFxrKoU/BZAKL86cfM5uTGZaA0SNaVI8d/Rj4t2IJs=.m3u8")

        videoName.append('금강-백제교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3012675&chid=KUARM')
        # videoURL.append("http://59.18.117.222:7081/1kydo0gN6BeCK7KyikXJ9dmyQSn8sDevY7mZydI1Eew=.m3u8")
        # videoSection.append(np.array([(960, 500), (1920, 1080)]))

        videoName.append('금강-노천교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3203652&chid=WOONGCHUN')
        # videoURL.append("http://59.18.117.222:7081/HMyjEVBMTgoXL7By5+6zlRVXTrc1XdoWdmbwlhc0moU=.m3u8")
        # videoSection.append(np.array([(0, 240), (720, 480)]))

        videoName.append('금강-동대교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3203620&chid=DAECHUN')
        # videoURL.append("http://59.18.117.222:7081/nuKYK1YqHJtBJ+ehShMjmIRF7hw+IbPlOjOaNs7xbCU=.m3u8")
        # videoSection.append(np.array([(0, 240), (720, 480)]))

        # videoName.append('금강-예산대교')
        # videoURL.append("http://59.18.117.222:7081/aQfPFu51HnOIl2pxO55LakKqWxUY4GTUYcWNCRy4/Nk=.m3u8")
        # videoSection.append(np.array([(0, 460), (1880, 620)]))

        videoName.append('금강-충무교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3101685&chid=CHUNGMU')
        # videoURL.append("http://59.18.117.222:7081/qWDL0rg2WJaS71QsdkteIxBCid6EHdj5BKRQstlP3g4=.m3u8")
        # videoSection.append(np.array([(0, 620), (1920, 1080)]))

        videoName.append('금강-강청교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3101690&chid=KANGCHUNG')
        # videoURL.append("http://59.18.117.222:7081/GVwc9CVV1tQ8veeHoND1Vfeiz68HNVoHy3O7ZbzVNPE=.m3u8")
        # videoSection.append(np.array([(0, 600), (1920, 920)]))

        videoName.append('금강-황산대교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3014610&chid=KANGKYUNG')
        # videoURL.append("http://59.18.117.222:7081/mjy66kHl3mGUFXTDSw943rv3XqA9eIUAbkpkKtOoyo8=.m3u8")
        # videoSection.append(np.array([(0, 240), (720, 420)]))

        videoName.append('금강-논산대교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3013670&chid=NONSAN')
        # videoURL.append("http://59.18.117.222:7081/CGyg9Bwdv5H7CUZ9aoj8BflewvEdBRlnoP8msMzBWR8=.m3u8")
        # videoSection.append(np.array([(60, 120), (320, 160)]))

        videoName.append('금강-복수교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009630&chid=BOKSU')
        # videoURL.append("http://59.18.117.222:7081/2VZMagKCEv1EVRDh6D52TCkSvN4P01DfhXTdRhECGRU=.m3u8")
        # videoSection.append(np.array([(0, 520), (1920, 1020)]))

        videoName.append('금강-가수원교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009665&chid=KASUWON')
        # videoURL.append("http://59.18.117.222:7081/tAzP65MdTZwBohwH17BKzgHa/iTyqEYYnNV3Uz/aznI=.m3u8")
        # videoSection.append(np.array([(0, 240), (580, 480)]))

        # videoName.append('금강-만년교')
        # videoURL.append("http://59.18.117.222:7081/XG6oJH1zkZ3WptEKfP/66Yhqz1CjSHbDU5pOw/cK5Fw=.m3u8")

        videoName.append('금강-인창교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009640&chid=INDONG')
        # videoURL.append("http://59.18.117.222:7081/cJ+M0/l9TiBLeswKhSTnwWB18Qv7y9l+ISGDraDilAc=.m3u8")
        # videoSection.append(np.array([(0, 240), (640, 480)]))

        # videoName.append('금강-한밭대교')
        # videoURL.append("http://59.18.117.222:7081/XPhZR/8vXgJhVsv5zMYjANt2zHqExolyvNXl99Gc3Fk=.m3u8")

        # videoName.append('금강-원촌교') #낮은 수심
        # videoURL.append("http://59.18.117.222:7081/zT6pjUXx1ICllX5ogJZR8/vjI9CbI8mBSWdFC1PKJQU=.m3u8")

        videoName.append('금강-제원교')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3008670&chid=GEUMSAN')
        # videoURL.append("http://59.18.117.222:7081/pqpywCWmzGuw2X8IlE7aHk/g4BF6H9LyxiumWAoRZR0=.m3u8")
        # videoSection.append(np.array([(240, 400), (1920, 1080)]))

        videoName.append('금강-무주군 취소장')
        videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3003680&chid=MUJU')
        # videoURL.append("http://59.18.117.222:7081/4fwXzHVtrvs+8hP08vy0AiNajVGUxYRMDiygTQq3nSA=.m3u8")
        # videoSection.append(np.array([(0, 360), (1920, 1080)]))

        for videos in videoReg:
            videoParts = requests.get(videos).text.split()
            for videoList in videoParts:
                if 'http:' in videoList:
                    videoURL.append(videoList.lstrip('="').rstrip('"'))  # 'http://59.18.117.222:7081/4fwXzHVtrvs+8hP08vy0AiNajVGUxYRMDiygTQq3nSA=.m3u8'
                    break

    for i in range(len(videoName)):
        videoIndex.append(i)
        selectComboName.append('[' + (str(i + 1)).zfill(2) + '] : ' + videoName[i])
    videoNumber = len(videoName)


def onRecv():
    global clientSockets
    global clientIDs
    global android_signal

    clientSockets = []
    clientIDs = []

    update_log('Server is on(' + str(TCP_IP) + ', ' + str(TCP_PORT) + ')')
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 서버측 소켓생성
    try:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # WinError 10048 에러해결
    except:
        pass
    serverSocket.bind((TCP_IP, TCP_PORT))  # 접속허용상태
    serverSocket.listen()  # 접속할수 있도록 대기중
    while(1):
        clientSocket, addr = serverSocket.accept()  # 접속한 클라이언트에 새로운 소켓 지정
        clientSockets.append(clientSocket)
        print('Connected by ', addr)
        # print('IP Address : ' + str(addr[0]))
        clientID = clientSocket.recv(6)
        print(int(clientID.rstrip()))
        if int(clientID.rstrip()) == 2999:
            android_signal = True
        with open(os.getcwd() + '/log/kumgang/_ip.txt', 'r') as file_ip:
            ipids = (file_ip.readlines())
        file_ip.close()
        for ipid in ipids:
            ip = ipid.split('#')[1]
            id = int(ipid.split('#')[2].rstrip('\n'))
            if id == int(clientID.rstrip()):
                if str(addr[0]) == str(ip):
                    clientIDs.append(int(clientID.rstrip()))
                    update_log(str(clientSocket) + ' log on')
                else:
                    print('IP address is not matching')
                    update_log(str(clientSocket) + ' ip address is not matching')
                    clientSocket.close()


def onSend():
    global clientSockets
    global clientIDs
    global select
    global boundary_temp_read

    call = np.zeros(5)
    time_yolo_cur = time.time()
    while(1):
        if time.time() - time_yolo_cur > 35 and select != -1:  # 35초마다 검사
            time_yolo_cur = time.time()
            for t in range(len(videoURL)):
                for o in range(len(call)):
                    call[o] = 0
                print(t)
                try:
                    yolo_video = cv2.VideoCapture(videoURL[t])
                    retval, yolo_frame = yolo_video.read()
                    yolo_video.release()
                    try:
                        with open(os.getcwd() + '/camera_area/kumgang/' + str(t) + '.txt', 'r') as file_boundary_read_yolo:
                            boundary_temp_read_yolo = (file_boundary_read_yolo.readlines())
                        file_boundary_read_yolo.close()
                    except:
                        boundary_temp_read_yolo = ['0#0#319#319']
                    yolo_image = yolo_frame.copy()
                    # yolo_image = cv2.resize(yolo_image, None, fx=0.4, fy=0.4)  # 크기 0.4배
                    height, width, channels = yolo_image.shape

                    blob = cv2.dnn.blobFromImage(yolo_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # 블롭객체 생성
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
                                print(width, height)
                                print(x, y, w, h)
                                for boundaries in boundary_temp_read_yolo:
                                    boundary_temp_x1, boundary_temp_y1, boundary_temp_x2, boundary_temp_y2 = str(boundaries).split('#')
                                    print(boundary_temp_x1, boundary_temp_y1, boundary_temp_x2, boundary_temp_y2)
                                    boundary_temp_x1 = (int(boundary_temp_x1)/319) * width
                                    boundary_temp_x2 = (int(boundary_temp_x2)/319) * width
                                    boundary_temp_y1 = (int(boundary_temp_y1)/319) * height
                                    boundary_temp_y2 = (int(boundary_temp_y2)/319) * height
                                    print(boundary_temp_x1, boundary_temp_y1, boundary_temp_x2, boundary_temp_y2)
                                    if (x >= int(boundary_temp_x1) and x <= int(boundary_temp_x2) and y >= int(boundary_temp_y1) and y <= int(boundary_temp_y2)) or ((x + w) >= int(boundary_temp_x1) and (x + w) <= int(boundary_temp_x2) and (y + h) >= int(boundary_temp_y1) and (y + h) <= int(boundary_temp_y2)) or ((x + w) >= int(boundary_temp_x1) and (x + w) <= int(boundary_temp_x2) and y >= int(boundary_temp_y1) and y <= int(boundary_temp_y2)) or (x >= int(boundary_temp_x1) and x <= int(boundary_temp_x2) and (y + h) >= int(boundary_temp_y1) and (y + h) <= int(boundary_temp_y2)):
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
                            cv2.imwrite('./test/' + str(t) + '#' + str(i + 1) + '#' + str(label) + '.jpg', yolo_image[y:y + h, x:x + w])
                            cv2.rectangle(yolo_image, (x, y), (x + w, y + h), color, 2)
                            cv2.putText(yolo_image, label, (x, y + 30), font, 2, color, 2)
                            print(label)
                            if label == 'person':  # 사람이 물에빠짐
                                call[0] = 1  # call은 병원, 소방서, 경찰서, 인양업체, 해양구조대순
                                call[4] = 1
                            if label == 'car' or label == 'truck' or label == 'bus' or label == 'train' or label == 'aeroplane' or label == 'mouse' or label == 'cell phone':  # 차량이 물에빠짐
                                call[0] = 1
                                call[1] = 1
                                call[3] = 1
                                call[4] = 1
                            if weatherWarm_rain == True:
                                if label == 'boat':
                                    call[2] = 1
                        else:
                            pass
                    yolo_image = cv2.resize(yolo_image, (400, 400))
                    cv2.imwrite('./test/example_' + str(t) + '.jpg', yolo_image)

                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    result, encode = cv2.imencode('.jpg', yolo_image, encode_param)  # 이미지 인코딩
                    length = str(len(encode))
                    length = length.encode()

                    for k in range(len(clientIDs)):
                        if call[0] == 1 and str(clientIDs[k]) == '2' + str(t).zfill(2) + '0':
                            try:
                                clientSockets[k].sendall(length)
                                time.sleep(0.2)
                                clientSockets[k].sendall(encode)
                                time.sleep(0.6)
                                update_log(str(clientSockets[k]) + '/hospital/success')
                            except:
                                update_log(str(clientSockets[k]) + '/hospital/fail')
                        if call[1] == 1 and str(clientIDs[k]) == '2' + str(t).zfill(2) + '1':
                            try:
                                clientSockets[k].sendall(length)
                                time.sleep(0.2)
                                clientSockets[k].sendall(encode)
                                time.sleep(0.6)
                                update_log(str(clientSockets[k]) + '/fire station/success')
                            except:
                                update_log(str(clientSockets[k]) + '/fire station/fail')
                        if call[2] == 1 and str(clientIDs[k]) == '2' + str(t).zfill(2) + '2':
                            try:
                                clientSockets[k].sendall(length)
                                time.sleep(0.2)
                                clientSockets[k].sendall(encode)
                                time.sleep(0.6)
                                update_log(str(clientSockets[k]) + '/police/success')
                            except:
                                update_log(str(clientSockets[k]) + '/police/fail')
                        if call[3] == 1 and str(clientIDs[k]) == '2' + str(t).zfill(2) + '3':
                            try:
                                clientSockets[k].sendall(length)
                                time.sleep(0.2)
                                clientSockets[k].sendall(encode)
                                time.sleep(0.6)
                                update_log(str(clientSockets[k]) + '/salvage company/success')
                            except:
                                update_log(str(clientSockets[k]) + '/salvage company/fail')
                        if call[4] == 1 and str(clientIDs[k]) == '2' + str(t).zfill(2) + '4':
                            try:
                                clientSockets[k].sendall(length)
                                time.sleep(0.2)
                                clientSockets[k].sendall(encode)
                                time.sleep(0.6)
                                update_log(str(clientSockets[k]) + '/rescue/success')
                            except:
                                update_log(str(clientSockets[k]) + '/rescue/fail')
                except:
                    print(str(t) + ' except')


def update_log(informationOfLog):  # 로그 업데이트
    global text_logdata

    path_log = os.getcwd() + '\\log\\' + riverList[select] + '\\'
    file_log = str(dt.datetime.now().year).zfill(4) + '_' + str(dt.datetime.now().month).zfill(2) + '_' + str(dt.datetime.now().day).zfill(2)
    with open(path_log + file_log + '.txt', 'a') as file:
        file.write(str(dt.datetime.now().hour).zfill(2) + ':' + str(dt.datetime.now().minute).zfill(2) + ':' + str(dt.datetime.now().second).zfill(2) + ', ' + informationOfLog + '\n')
    file.close()
    try:
        text_logdata.insert(tkinter.CURRENT, str(dt.datetime.now().hour).zfill(2) + ':' + str(dt.datetime.now().minute).zfill(2) + ':' + str(dt.datetime.now().second).zfill(2) + ', ' + informationOfLog + '\n')
    except:
        pass


def read_log(file_name):
    with open(resource_path('.\\log\\' + riverList[select] + '\\' + file_name), 'r') as file_android:
        logs = file_android.read()
    file_android.close()
    length = int(len(logs))
    print(logs, length)

    return logs, length


def onRiver():
    global select
    global selectWindow

    select = selectRiver.current()
    selectWindow.destroy()

    onRegister()
    update_log(' ' + riverList[select] + ' server on')


def onAndroid():
    global clientIDs
    global clientSockets
    global android_signal

    android_signal = False
    while(1):
        if android_signal == True:
            for [p, an] in enumerate(clientIDs):
                if an == 2999:
                    androidSocket = clientSockets[p]
                    del clientIDs[p]
                    del clientSockets[p]
                    print(androidSocket)
                    android_date = androidSocket.recv(10).decode()
                    time.sleep(0.4)
                    print(android_date)
                    update_log(str(androidSocket) + ' android request for ' + str(android_date))
                    for file_log in os.listdir(resource_path('./log/' + riverList[select] + '/')):
                        if android_date + '.txt' == file_log:
                            datas, leng = read_log(android_date + '.txt')
                            update_log(str(androidSocket) + ' android request success')
                            break
                        else:
                            datas = 'no data'
                            leng = len(datas)
                            # update_log(str(androidSocket) + ' android request fail')
                    androidSocket.sendall(str(leng).zfill(10).encode())
                    time.sleep(0.2)
                    androidSocket.sendall(datas.encode())
                    time.sleep(2)
                    android_signal = False
                    androidSocket.close()
                    continue
        else:
            time.sleep(5)


def onTimer_draw():
    global timer_draw
    global videoTemp
    global videoNumber
    global mini_video

    while(1):
        if str(dt.datetime.now().minute).zfill(2) == '00':
            onReadWeather()
            time.sleep(60)
        if time.time() - timer_draw > mini_update_timer:
            timer_draw = time.time()
            for [ind, url] in enumerate(videoURL):
                if ind == videoNumber:
                    pass
                else:
                    videoTemp = cv2.VideoCapture(url)
                    retval, image_timer = videoTemp.read()
                    image_timer = cv2.resize(image_timer, (120, 120))

                    TKImage_video_mini = cv2.cvtColor(image_timer, cv2.COLOR_BGR2RGB)
                    TKImage_video_mini = PIL.Image.fromarray(TKImage_video_mini)
                    imgtk_video_mini = PIL.ImageTk.PhotoImage(image=TKImage_video_mini)

                    mini_video[ind].configure(image=imgtk_video_mini)
                    mini_video[ind].image = imgtk_video_mini


def onBoundary_save():
    global boundary_temp

    if boundary_temp == []:
        pass
    else:
        print(len(boundary_temp))
        with open(os.getcwd() + '/camera_area/kumgang/' + str(selectIndex) + '.txt', 'w') as file_boundary:
            for file_writer in range(len(boundary_temp)):
                file_boundary.write(str(boundary_temp[file_writer][0][0]) + '#' + str(boundary_temp[file_writer][0][1]) + '#' + str(boundary_temp[file_writer][1][0]) + '#' + str(boundary_temp[file_writer][1][1]) + '\n')
        file_boundary.close()
        boundary_temp = []


def onOpen_IPTXT():
    try:
        os.startfile(os.getcwd() + '/log/kumgang/_ip.txt')
    except:
        messagebox.showinfo('Notice', '파일을 열수 없음.')


def onReadWeather():
    global weatherText
    global weatherWarm_rain

    try:
        weather_soup = BeautifulSoup(
            requests.get('http://www.weather.go.kr/weather/observation/currentweather.jsp').content, "html.parser")
        weather_table = weather_soup.find('table', {'class': 'table_develop3'})
        weather_data = []
        weatherWarm_rain = False

        for tr in weather_table.find_all('tr'):
            tds = list(tr.find_all('td'))
            for td in tds:
                if td.find('a'):
                    point = td.find('a').text
                    weather = tds[1].text
                    weather_data.append([point, weather])
        print(weather_data[20])
        if weather_data[20][1] == '\xa0':
            weather_data[20][1] = '맑음'
        if weather_data[20][1] == '약한 비 연속적' or '약한 비 단속적' or '약한 천둥번개, 비' or '보통 비 연속적' or '강한 비 연속적' or '안개 짙어짐':
            weatherWarm_rain = True
        weatherText.insert(tkinter.CURRENT, str(weather_data[20][0]) + " 날씨 : " + str(weather_data[20][1]))
        update_log('Weather Infomation Update : ' + str(weather_data[20][0] + ' ' + str(weather_data[20][1])))
    except:
        weatherText.insert(tkinter.CURRENT, '기상청 사이트 정보 없음')
        update_log('Weather Infomation Update : no connection')
        weatherWarm_rain = False


def onAddTestData():
    global videoName
    global videoURL
    global videoNumber

    Tk.filename = filedialog.askopenfilename(initialdir=str(os.path.dirname(os.getcwd())) + '/', title="비디오 선택", filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg"), ("png files", "*.png")))
    if Tk.filename != '':
        print(Tk.filename)
        try:
            if len(videoName) == videoNumber:
                videoName.append('TestData')
                videoURL.append(str(Tk.filename))
            else:
                videoName[videoNumber] = 'TestData'
                videoURL[videoNumber] = str(Tk.filename)
        except:
            print('Video file only please.')
    else:
        pass


# TCP_IP = str(socket.gethostbyname_ex(socket.getfqdn())[-1][-1])
TCP_IP = '127.0.0.1'
TCP_PORT = 5001  # port번호
print(TCP_IP, TCP_PORT)
# select = -1
select = 2

allQuit = False

# tag = ['car', 'person']

selectIndex = 0
selectComboName = []
videoName = []
videoIndex = []
videoURL = []
videoReg = []
# videoSection = []
# videoCover = []
riverList = ['hangang', 'nakdonggang', 'kumgang']

onRegister()
onInit()

mini_update_timer = 120
timer_draw = time.time() - (mini_update_timer + 10)
videoMini = []
mini_video = []
for i in videoURL:
    videoMini.append(i)

boundary_temp = []
show_boundary = False
boundary_temp_read = []

if os.path.exists(os.getcwd() + '/log/kumgang/_ip.txt'):
    pass
else:
    with open(os.getcwd() + '/log/kumgang/_ip.txt', 'w') as file_ip_text:
        for [i, camera] in enumerate(videoName):
            for [j, call] in enumerate(['병원', '소방서', '경찰서', '인양업체', '해양구조대']):
                file_ip_text.write((str(camera) + str(call)).ljust(20) + '#' + str('127.0.0.1') + '#' + str(2) + str(i).zfill(2) + str(j) + '\n')
        for [k, call] in enumerate(['병원', '소방서', '경찰서', '인양업체', '해양구조대']):
            file_ip_text.write(('금강-test' + str(call)).ljust(20) + '#' + str('127.0.0.1') + '#' + str(2) + str(15).zfill(2) + str(k) + '\n')
    file_ip_text.close()
    # update_log('ip.txt file remake')

# video = cv2.VideoCapture("http://59.18.117.222:7081/d0lgTS6dU/3hVQZPbdBW+b1yJw5Lmqq8Im3d9ps7JY8=.m3u8")
# video.set(cv2.CAP_PROP_FPS, 1)
# retval, frame = video.read()
# frame = cv2.resize(frame, (320, 320))
frame = cv2.imread(resource_path('./black.jpg'))
frame = cv2.resize(frame, (320, 320))

net = cv2.dnn.readNet(resource_path("./yolo/yolov4.weights"), resource_path("./yolo/yolov4.cfg"))  # 학습데이터 로드(DNN)
classes = []
with open(resource_path("./yolo/coco.names"), "r") as f:
    classes = [line.strip() for line in f.readlines()]  # 아마도 양옆 공백 없에서 한줄씩 저장하는것 같음(아마 라벨링)
print('학습된 클래스:'+str(classes))
layer_names = net.getLayerNames()  # 아마도 레이어명
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  # 마지막 레이어 식별
colors = np.random.uniform(0, 255, size=(len(classes), 3))  # 0~255 사이의 (라벨, 3)의 랜덤난수 배열 생성(클래스별로 색생 다르게표시)

drawThread = threading.Thread(target=onDraw)
drawThread.start()

recvThread = threading.Thread(target=onRecv)
recvThread.daemon = True
recvThread.start()

sendThread = threading.Thread(target=onSend)
sendThread.daemon = True
sendThread.start()

androidThread = threading.Thread(target=onAndroid)
androidThread.daemon = True
androidThread.start()

videoPlayThread = threading.Thread(target=onPlayVideo)
videoPlayThread.daemon = True
videoPlayThread.start()

time.sleep(1)
onReadWeather()

updatePreviewThread = threading.Thread(target=onTimer_draw)
updatePreviewThread.daemon = True
updatePreviewThread.start()