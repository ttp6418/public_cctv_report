import numpy as np
import cv2

import tkinter
from tkinter import Tk, Label
from tkinter import messagebox
from tkinter import Radiobutton
from tkinter import Entry
from tkinter import filedialog
from tkinter import Menu
from tkinter import *
import tkinter.ttk as ttk

import PIL
# from PIL import Image, ImageTk
from PIL import Image
from PIL import ImageTk

import time
import threading
import socket
import os
import sys

import requests #웹 페이지의 HTML을 가져오는 모듈


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath('__file__')))

    return os.path.join(base_path, relative_path)


def onDraw():
    global mainWindow
    global loginCombo_cctv
    global loginCombo_ID
    global loginWindow
    global loginTextBox
    global alert_signal
    global label_alert
    global label_1
    global label_2
    global label_3
    global label_4
    global delbutton
    global check_alert

    mainWindow = tkinter.Tk()
    mainWindow.title("Main Window")
    mainWindow.geometry("480x480+100+100")
    mainWindow.resizable(False, False)
    mainWindow.iconphoto(False, tkinter.PhotoImage(file=resource_path('./river.png')))

    leftIcon = PhotoImage(file=resource_path('./left.png'))
    rightIcon = PhotoImage(file=resource_path('./right.png'))

    checkVariety_alert = tkinter.IntVar()
    check_alert = tkinter.Checkbutton(mainWindow, text="알림 여부", variable=checkVariety_alert, command=onAlert_reverse, overrelief='sunken', activebackground="yellow", highlightbackground="red")
    check_alert.toggle()
    check_alert.place(x=360, y=2)

    notebook = tkinter.ttk.Notebook(mainWindow, width=440, height=420)
    notebook.place(x=20, y=20)

    alertFrame = tkinter.Frame(mainWindow)
    notebook.add(alertFrame, text="Alert Window")
    recordFrame = tkinter.Frame(mainWindow)
    notebook.add(recordFrame, text="Record Window")

    noneImage = cv2.imread(resource_path('./none.png'), cv2.IMREAD_COLOR)
    noneImage = cv2.resize(noneImage, (100, 100))
    noneIamge2 = cv2.resize(noneImage, (160, 160)).copy()

    TKImage_none = cv2.cvtColor(noneImage, cv2.COLOR_BGR2RGB)
    TKImage_none = Image.fromarray(TKImage_none)
    imgtk_none = ImageTk.PhotoImage(image=TKImage_none)

    TKImage_none2 = cv2.cvtColor(noneIamge2, cv2.COLOR_BGR2RGB)
    TKImage_none2 = Image.fromarray(TKImage_none2)
    imgtk_none2 = ImageTk.PhotoImage(image=TKImage_none2)

    if ID == -1:
        loginWindow = tkinter.Tk()
        loginWindow.title("Login")
        loginWindow.geometry("300x120+400+400")
        loginWindow.resizable(False, False)

        logintextBox1 = tkinter.Text(loginWindow, width=12, height=1)
        logintextBox1.insert(tkinter.CURRENT, "CCTV번호")
        logintextBox1.configure(state='disabled') #읽기전용
        logintextBox1.place(x=10, y=10)

        loginCombo_cctv = ttk.Combobox(loginWindow, height=16, width=20, state="readonly", value=videoName, postcommand=None)
        loginCombo_cctv.place(x=110, y=10)
        loginCombo_cctv.set("선택")

        logintextBox2 = tkinter.Text(loginWindow, width=12, height=1)
        logintextBox2.insert(tkinter.CURRENT, "기관선택")
        logintextBox2.configure(state='disabled')
        logintextBox2.place(x=10, y=40)

        loginCombo_ID = ttk.Combobox(loginWindow, height=16, width=20, state="readonly", value=IDInfo, postcommand=None)
        loginCombo_ID.place(x=110, y=40)
        loginCombo_ID.set("선택")

        loginbutton = tkinter.Button(loginWindow, text="확인", command=onLogin)
        loginbutton.place(x=100, y=80)

    loginTextBox = tkinter.Text(alertFrame, width=40, height=1)
    loginTextBox.place(x=20, y=20)

    label_alert = tkinter.Label(alertFrame, image=imgtk_none)
    label_alert.place(x=20, y=40)
    label_alert.place_forget()

    delbutton = tkinter.Button(alertFrame, text="확인완료", command=onDelete)
    delbutton.place(x=180, y=400)
    delbutton.place_forget()

    leftbutton = tkinter.Button(recordFrame, text="", command=onLeft, image=leftIcon, compound=LEFT)
    leftbutton.place(x=20, y=200)

    label_1 = tkinter.Label(recordFrame, image=imgtk_none2)
    label_1.place(x=60, y=40)
    label_1.bind("<Button-1>", onShow)

    label_2 = tkinter.Label(recordFrame, image=imgtk_none2)
    label_2.place(x=220, y=40)
    label_2.bind("<Button-1>", onShow)

    label_3 = tkinter.Label(recordFrame, image=imgtk_none2)
    label_3.place(x=60, y=200)
    label_3.bind("<Button-1>", onShow)

    label_4 = tkinter.Label(recordFrame, image=imgtk_none2)
    label_4.place(x=220, y=200)
    label_4.bind("<Button-1>", onShow)

    loginbutton = tkinter.Button(recordFrame, text="", command=onRight, image=rightIcon, compound=LEFT)
    loginbutton.place(x=400, y=200)

    savebutton = tkinter.Button(recordFrame, text="모든 기록정보 저장", command=onRecordSave)
    savebutton.place(x=160, y=400)

    mainWindow.mainloop()


def onLogin():
    global cctv_number
    global id_number
    global clientID
    global ID
    global alert_msg

    cctv_number = loginCombo_cctv.current()
    id_number = loginCombo_ID.current()

    if cctv_number == -1 or id_number == -1:
        alert_msg = '필수 선택 사항입니다.'
    else:
        loginWindow.destroy()
        loginTextBox.insert(tkinter.CURRENT, "장소:"+str(videoName[cctv_number]) + ', ' + str(IDInfo[id_number]))

        ID = int(str('2') + str(cctv_number).zfill(2) + str(id_number))
        print(ID)


def onRegister():
    global videoName
    global videoURL
    global videoReg
    global videoSection

    # (720, 480), (1920, 1080)
    videoReg = []

    videoName.append('금강-팔결교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3011635&chid=BOOKIL')
    # videoURL.append("http://59.18.117.222:7081/d0lgTS6dU/3hVQZPbdBW+b1yJw5Lmqq8Im3d9ps7JY8=.m3u8")
    videoSection.append(np.array([(0, 192), (720, 480)]))

    videoName.append('금강-흥덕교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3011645&chid=CHUNGJU')
    # videoURL.append("http://59.18.117.222:7081/hqR8igF9RNGzRhxw/5GreFvfSQBYRoO5nXm7CnJZOkk=.m3u8")
    videoSection.append(np.array([(0, 520), (1240, 680)]))

    # videoName.append('금강-미호천교')
    # videoURL.append("http://59.18.117.222:7081/rx54ORfELbLurgHyDBkJzFz0DYz7hqI9Q7GGj6n6gS8=.m3u8")
    # videoSection.append(np.array([(1200, 540), (1920, 1080)]))

    videoName.append('금강-세종리')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3012602&chid=SEJONG')
    # videoURL.append("http://59.18.117.222:7081/aDoiA1hjzm6Q1bu2QXjRfy84Ggq2BH/bdcdQROVuxnY=.m3u8")
    videoSection.append(np.array([(0, 270), (1920, 1080)]))

    # videoName.append('금강-금강교')
    # videoURL.append("http://59.18.117.222:7081/4FFxrKoU/BZAKL86cfM5uTGZaA0SNaVI8d/Rj4t2IJs=.m3u8")

    videoName.append('금강-백제교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3012675&chid=KUARM')
    # videoURL.append("http://59.18.117.222:7081/1kydo0gN6BeCK7KyikXJ9dmyQSn8sDevY7mZydI1Eew=.m3u8")
    videoSection.append(np.array([(960, 500), (1920, 1080)]))

    videoName.append('금강-노천교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3203652&chid=WOONGCHUN')
    # videoURL.append("http://59.18.117.222:7081/HMyjEVBMTgoXL7By5+6zlRVXTrc1XdoWdmbwlhc0moU=.m3u8")
    videoSection.append(np.array([(0, 240), (720, 480)]))

    videoName.append('금강-동대교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3203620&chid=DAECHUN')
    # videoURL.append("http://59.18.117.222:7081/nuKYK1YqHJtBJ+ehShMjmIRF7hw+IbPlOjOaNs7xbCU=.m3u8")
    videoSection.append(np.array([(0, 240), (720, 480)]))

    # videoName.append('금강-예산대교')
    # videoURL.append("http://59.18.117.222:7081/aQfPFu51HnOIl2pxO55LakKqWxUY4GTUYcWNCRy4/Nk=.m3u8")
    # videoSection.append(np.array([(0, 460), (1880, 620)]))

    videoName.append('금강-충무교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3101685&chid=CHUNGMU')
    # videoURL.append("http://59.18.117.222:7081/qWDL0rg2WJaS71QsdkteIxBCid6EHdj5BKRQstlP3g4=.m3u8")
    videoSection.append(np.array([(0, 620), (1920, 1080)]))

    videoName.append('금강-강청교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3101690&chid=KANGCHUNG')
    # videoURL.append("http://59.18.117.222:7081/GVwc9CVV1tQ8veeHoND1Vfeiz68HNVoHy3O7ZbzVNPE=.m3u8")
    videoSection.append(np.array([(0, 600), (1920, 920)]))

    videoName.append('금강-황산대교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3014610&chid=KANGKYUNG')
    # videoURL.append("http://59.18.117.222:7081/mjy66kHl3mGUFXTDSw943rv3XqA9eIUAbkpkKtOoyo8=.m3u8")
    videoSection.append(np.array([(0, 240), (720, 420)]))

    videoName.append('금강-논산대교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3013670&chid=NONSAN')
    # videoURL.append("http://59.18.117.222:7081/CGyg9Bwdv5H7CUZ9aoj8BflewvEdBRlnoP8msMzBWR8=.m3u8")
    videoSection.append(np.array([(60, 120), (320, 160)]))

    videoName.append('금강-복수교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009630&chid=BOKSU')
    # videoURL.append("http://59.18.117.222:7081/2VZMagKCEv1EVRDh6D52TCkSvN4P01DfhXTdRhECGRU=.m3u8")
    videoSection.append(np.array([(0, 520), (1920, 1020)]))

    videoName.append('금강-가수원교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009665&chid=KASUWON')
    # videoURL.append("http://59.18.117.222:7081/tAzP65MdTZwBohwH17BKzgHa/iTyqEYYnNV3Uz/aznI=.m3u8")
    videoSection.append(np.array([(0, 240), (580, 480)]))

    # videoName.append('금강-만년교')
    # videoURL.append("http://59.18.117.222:7081/XG6oJH1zkZ3WptEKfP/66Yhqz1CjSHbDU5pOw/cK5Fw=.m3u8")

    videoName.append('금강-인창교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3009640&chid=INDONG')
    # videoURL.append("http://59.18.117.222:7081/cJ+M0/l9TiBLeswKhSTnwWB18Qv7y9l+ISGDraDilAc=.m3u8")
    videoSection.append(np.array([(0, 240), (640, 480)]))

    # videoName.append('금강-한밭대교')
    # videoURL.append("http://59.18.117.222:7081/XPhZR/8vXgJhVsv5zMYjANt2zHqExolyvNXl99Gc3Fk=.m3u8")

    # videoName.append('금강-원촌교') #낮은 수심
    # videoURL.append("http://59.18.117.222:7081/zT6pjUXx1ICllX5ogJZR8/vjI9CbI8mBSWdFC1PKJQU=.m3u8")

    videoName.append('금강-제원교')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3008670&chid=GEUMSAN')
    # videoURL.append("http://59.18.117.222:7081/pqpywCWmzGuw2X8IlE7aHk/g4BF6H9LyxiumWAoRZR0=.m3u8")
    videoSection.append(np.array([(240, 400), (1920, 1080)]))

    videoName.append('금강-무주군 취소장')
    videoReg.append('http://www.geumriver.go.kr/html/sumun/rtmpView.jsp?wlobscd=3003680&chid=MUJU')
    # videoURL.append("http://59.18.117.222:7081/4fwXzHVtrvs+8hP08vy0AiNajVGUxYRMDiygTQq3nSA=.m3u8")
    videoSection.append(np.array([(0, 360), (1920, 1080)]))
    count = 0
    for videos in videoReg:
        videoParts = requests.get(videos).text.split()
        for videoList in videoParts:
            if 'http:' in videoList:
                videoURL.append(videoList.lstrip('="').rstrip('"'))
                break

    try:
        os.mkdir(os.getcwd() + '/client')
    except:
        pass
    try:
        os.mkdir(os.getcwd() + '/client/result_save/')
    except:
        pass

    for file in os.listdir(os.getcwd() + '/client/result_save/'):
        os.remove(os.getcwd() + '/client/result_save/' + file)
    videoName.append('Test Only')


def onRECV():
    global alert_image
    global alert_signal
    global recordArray

    global alert_msg

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5001

    while (1):
        if ID == -1:
            pass
        else:
            break
    userSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        userSocket.connect((TCP_IP, TCP_PORT))
    except:
        messagebox.showinfo('Notice', 'Server is down')
        mainWindow.quit()
        exit(1)
    userSocket.sendall(str(ID).encode())  # id값은 어디 카메라의 어느 관공서인지

    while(1):
        length_data = userSocket.recv(6)
        new_length_data = length_data.rstrip()
        try:
            try:
                new_length_data = int(new_length_data)
            except:
                messagebox.showinfo('Notice', 'refuse connection')
                mainWindow.quit()
                exit(1)
            time.sleep(0.2)
            data = receive_all(userSocket, new_length_data)
            time.sleep(0.2)
            imgArray = np.frombuffer(data, dtype=np.uint8)
            alert_image = cv2.imdecode(imgArray, 1)

            label_alert.place(x=20, y=40)

            TKImage_alert = cv2.cvtColor(cv2.resize(alert_image, (320, 320)), cv2.COLOR_BGR2RGB)  # TKinter는 RGB중심
            TKImage_alert = PIL.Image.fromarray(TKImage_alert)  # numpy 배열을 이미지객체화
            imgtk_alert = PIL.ImageTk.PhotoImage(image=TKImage_alert)  # TKinter와 호완되는 이미지객체화

            if alert_stop == True:  # 멈춤상태
                pass
            else:
                label_alert.configure(image=imgtk_alert)
                label_alert.image = imgtk_alert

                alert_msg = '긴급 상황 발생'
            delbutton.place(x=200, y=400)
            try:
                cv2.imwrite(os.getcwd() + '/client/result_save/' + str(len(os.listdir(os.getcwd() + '/client/result_save/'))) + '.jpg', alert_image)
            except:
                cv2.imwrite(os.getcwd() + '/client/result_save/except.jpg', alert_image)

            recordArray = []

            for file in os.listdir(os.getcwd() + '/client/result_save/'):
                recordArray.append(file)
            refresh_record()
        except():
            data = receive_all(userSocket, new_length_data)
            time.sleep(0.2)


def receive_all(sock, length):
    buf = b''
    try:
        step = length
        while True:
            data = sock.recv(step)
            buf = buf + data
            if len(buf) == length:
                break
            elif len(buf) < length:
                step = length - len(buf)
    except Exception as e: #예외처리해준거에대한 실행문
        print(e)
    return buf[:length]


def onDelete():
    global delbutton
    global label_alert

    delbutton.place_forget()
    label_alert.place_forget()


def onRecordSave():
    Tk.foldername = filedialog.askdirectory(initialdir="C:/Users/82107/PycharmProjects/engineeringDesign/", title="저장할 폴더 선택")
    for file in os.listdir(os.getcwd() + '/client/result_save/'):
        print(file)
        cv2.imwrite(Tk.foldername+'/'+str(file), cv2.imread(os.getcwd() + '/client/result_save/' + file, cv2.IMREAD_COLOR))
        print(Tk.foldername)


def refresh_record():
    noneImage2 = cv2.imread(resource_path('./none.png'), cv2.IMREAD_COLOR)
    noneIamge2 = cv2.resize(noneImage2, (160, 160)).copy()

    TKImage_none2 = cv2.cvtColor(noneIamge2, cv2.COLOR_BGR2RGB)
    TKImage_none2 = Image.fromarray(TKImage_none2)
    imgtk_none2 = ImageTk.PhotoImage(image=TKImage_none2)
    try:
        TKImage_1 = cv2.cvtColor(cv2.resize(cv2.imread(os.getcwd() + '/client/result_save/' + str(recordArray[recordPage * 4 - 4])), (160, 160)), cv2.COLOR_BGR2RGB)
        TKImage_1 = Image.fromarray(TKImage_1)
        imgtk_1 = ImageTk.PhotoImage(image=TKImage_1)

        label_1.configure(image=imgtk_1)
        label_1.image = imgtk_1
    except:
        label_1.configure(image=imgtk_none2)
        label_1.image = imgtk_none2
    try:
        TKImage_2 = cv2.cvtColor(cv2.resize(cv2.imread(os.getcwd() + './client/result_save/' + str(recordArray[recordPage * 4 - 3])), (160, 160)), cv2.COLOR_BGR2RGB)
        TKImage_2 = Image.fromarray(TKImage_2)
        imgtk_2 = ImageTk.PhotoImage(image=TKImage_2)

        label_2.configure(image=imgtk_2)
        label_2.image = imgtk_2
    except:
        label_2.configure(image=imgtk_none2)
        label_2.image = imgtk_none2
    try:
        TKImage_3 = cv2.cvtColor(cv2.resize(cv2.imread(os.getcwd() + './client/result_save/' + str(recordArray[recordPage * 4 - 2])), (160, 160)), cv2.COLOR_BGR2RGB)
        TKImage_3 = Image.fromarray(TKImage_3)
        imgtk_3 = ImageTk.PhotoImage(image=TKImage_3)

        label_3.configure(image=imgtk_3)
        label_3.image = imgtk_3
    except:
        label_3.configure(image=imgtk_none2)
        label_3.image = imgtk_none2
    try:
        TKImage_4 = cv2.cvtColor(cv2.resize(cv2.imread(os.getcwd() + './client/result_save/' + str(recordArray[recordPage * 4 - 1])), (160, 160)), cv2.COLOR_BGR2RGB)
        TKImage_4 = Image.fromarray(TKImage_4)
        imgtk_4 = ImageTk.PhotoImage(image=TKImage_4)

        label_4.configure(image=imgtk_4)
        label_4.image = imgtk_4
    except:
        label_4.configure(image=imgtk_none2)
        label_4.image = imgtk_none2


def onLeft():
    global recordPage

    if recordPage == 1:
        pass
    else:
        recordPage = recordPage - 1
    refresh_record()


def onRight():
    global recordPage

    if recordPage == ((len(recordArray)) + 5) / 4:
        pass
    else:
        recordPage = recordPage + 1
    refresh_record()


def onShow(event):
    x = event.x
    y = event.y
    if x > 60 and x < 220 and y > 40 and y < 200:
        cv2.imshow("Preview", resource_path('./client/result_save/' + recordArray[(recordPage - 1) * 4 + 0]))
    if x > 220 and x < 380 and y > 40 and y < 200:
        cv2.imshow("Preview", resource_path('./client/result_save/' + recordArray[(recordPage - 1) * 4 + 1]))
    if x > 60 and x < 220 and y > 200 and y < 360:
        cv2.imshow("Preview", resource_path('./client/result_save/' + recordArray[(recordPage - 1) * 4 + 2]))
    if x > 220 and x < 380 and y > 200 and y < 360:
        cv2.imshow("Preview", resource_path('./client/result_save/' + recordArray[(recordPage - 1) * 4 + 3]))


def onAlert():
    global alert_msg

    while(True):
        if alert_msg == ' ':
            pass
        else:
            messagebox.showinfo('Notice', alert_msg)
            alert_msg = ' '


def onAlert_reverse():
    global alert_stop
    global check_alert

    alert_stop = not alert_stop
    print(alert_stop)


ID = -1
IDInfo = ['병원(1)', '소방서(2)', '경찰서(3)', '인양업체(4)', '해양구조대(5)']
videoName = []
videoURL = []
videoSection = []
recordPage = 1
alert_msg = ' '
alert_stop = False
onRegister()

try:
    os.mkdir(os.getcwd()+'/client/')
except:
    pass
try:
    os.mkdir(os.getcwd()+'/client/result_save/')
except:
    pass

drawThread = threading.Thread(target=onDraw)
drawThread.start()

readBufThread = threading.Thread(target=onRECV)
readBufThread.daemon = True
readBufThread.start()

alertBufThread = threading.Thread(target=onAlert)
alertBufThread.daemon = True
alertBufThread.start()