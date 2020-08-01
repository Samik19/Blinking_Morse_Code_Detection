# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 20:14:42 2020

@author: Samik Pal
"""
import cv2
import numpy as np
import dlib
from math import hypot
from time import time 
import keyboard

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

flag = 0
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

spaces = []

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
                
        if blinking_ratio > 5.7:
            flag = 1    
        if blinking_ratio < 5.7 and flag == 1:
            flag = 0     
            spaces.append(time())
            
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

dif = [spaces[i] - spaces[i - 1] for i in range(1,len(spaces))]

df = []
morse = []

for d in dif:
    if (d <= 1 and d >= 0):
        df.append(0)
    if (d <= 3 and d >= 1):
        df.append(1)
    if (d <= 5 and d >= 3):
        df.append(3)
    
    
f = 0

for d in df:
    if d == 0:
        if f == 0:
            f = 1
            morse.append('_')
    if d == 1:
        morse.append('.')
        f = 0
    
str_code = ''.join(morse)

print(str_code)

if str_code == '...':
    print('Code 1')
elif str_code == '._.':
    print('Code 2')
elif str_code == '.__':
    print('Code 3')
elif str_code == '_._':
    print('Code 4')


