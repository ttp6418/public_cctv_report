import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

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
#from PIL import Image, ImageTk
from PIL import Image
from PIL import ImageTk

import time
from datetime import datetime
import threading
import socket
import select
import os
import sys
import h5py
from dataclasses import dataclass #구조체
import random

import requests #웹 페이지의 HTML을 가져오는 모듈
from bs4 import BeautifulSoup #HTML을 파싱하는 모듈

def onDraw():
    mainWindow = tkinter.Tk()
    mainWindow.title("Main Window")
    mainWindow.geometry("480x480+100+100")
    mainWindow.resizable(False, False)



    mainWindow.mainloop()

drawThread = threading.Thread(target=onDraw)
drawThread.start()