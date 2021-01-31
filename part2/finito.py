import numpy as np
import dlib
import cv2
import pyautogui
import time
from datetime import datetime
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
def face_detect():
    global cc
    img = pyautogui.screenshot(region=(1680, 0, 235, 235))  # face coord
    img = np.array(img)[:, :, :3].astype(np.uint8)
    rec = detector(img)
    # cv2.imwrite(f'check{cc}.png',img)

    try:
        pts = predictor(img,rec[0])
        x1, y1 = pts.part(37).x, pts.part(37).y
        x2, y2 = pts.part(19).x, pts.part(19).y
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 1 / 2
        tmp = 1 if dist > 500 else 2
        print(tmp)
        return tmp
    except:

        return 0
def empty_check(direction):
    im = pyautogui.screenshot()
    im = np.array(im)[:, :, :3].astype(np.uint8)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    x=958        # canavarin karesi
    y = 300
    if direction == 'A':
        x-= 130      #patlayabilir
    elif direction == 'D':
        x+=130
    elif direction == 'S':
        y+=130
    else:
        y-=130
    val = im[y,x]
    tmp = False if (val > 230 )^( val <80) else True
    stat = 'bos' if tmp else 'dolu'
    print(stat)
    return tmp

def revert_direction(direction):
    if direction == 'A':
        return 'D'
    elif direction == 'D':
        return 'A'
    elif direction == 'W':
        return 'S'
    else :
        return 'W'
def move(direction,step=1,s=0.05):
    for _ in range(step):
        pyautogui.keyDown(direction)
        time.sleep(s)
        pyautogui.keyUp(direction)
        # time.sleep(0.2)



def change_dir(direction):
    if direction == 'A':
        return 'S'
    elif direction == 'D':
        return 'A'
    elif direction == 'W':
        return 'D'
    else :
        return 'W'
def index_update(direction):
    if direction == 'A':
        return 'S'
    elif direction == 'D':
        return 'A'
    elif direction == 'W':
        return 'D'
    else :
        return 'W'
def square_check(direction):
    if direction == 'D':
        point = (290,920)
    elif direction == 'A':
        point = (290,997)
    elif direction == 'S':
        point = (212,954)
    else:
        point = (324,961)
    im = pyautogui.screenshot()
    im = np.array(im)[:, :, :3].astype(np.uint8)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    if im[point] > 200:
        return 1 #white
    return 0 #black
def next_point(direction,ind):
    if direction == 'A':
        return (ind[0]-1,ind[1])
    elif direction == 'D':
        return (ind[0]+1,ind[1])
    elif direction == 'W':
        return (ind[0],ind[1]+1)
    else:
        return (ind[0],ind[1]-1)

count = 0
dir = 'W'
time.sleep(2)
prev_bc = 1

grid = np.zeros((100,100))# 1 for seen 2 for blocked
ind = (50,50)#x y
grid[50,50]= 1
stack = []
bug_counter = 0
while True:
    if face_detect() ==0:
        exit()
    if grid[next_point(dir,ind)] == 0 and empty_check(dir) == False and face_detect() == 1 :
        bc = square_check(dir)
        # print(bc)
        if prev_bc != bc:
            prev_bc = bc
            stack.append(ind)
            grid[ind] = 2
            ind = next_point(dir,ind)
            count = -2
        move(dir,1,0.2)
        count+=1
        time.sleep(0.4)
        bug_counter = 0
    elif grid[next_point(dir,ind)] !=0:
        dir = change_dir(dir)

    elif (empty_check(dir) == True or face_detect() == 2) and bug_counter==0 :
        print('geri bas')
        grid[next_point(dir, ind)] = 1
        r = revert_direction(dir)
        for i in range(count):
            move(r, 1, 0.2)
            time.sleep(0.1)
        dir = change_dir(dir)
        if next_point(dir,ind) == 2:
            dir = change_dir(dir)
        count = 0
        bug_counter+=1
    elif bug_counter != 0:
            print('patladi')
            pyautogui.press(dir)
            pyautogui.press(revert_direction(dir))


#TODO 1. MERKEZI KALIBRE ET 2. CIKMAZ SOKAK EKLE