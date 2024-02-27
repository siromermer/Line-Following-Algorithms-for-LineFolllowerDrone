import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time 
import math
import random

#  background path image
background = cv2.imread("resources/clearred.png")

# initial coordiantes of drone
x=80
y=640

# velocity parameters
vx=0
vy=3

# slope degree , random value in beginning 
slope_angle_degrees=9999


while True : 
    
    # consider roi as drones camera     
    roi = background[y-100:y+100,x-75:x+100]
    # convert gray scale
    gray_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    # create binary image
    ret ,thresh = cv2.threshold(gray_roi,50,255,cv2.THRESH_BINARY)

    # Apply edge detection method on the image
    canny = cv2.Canny(gray_roi, 200, 255, apertureSize=3)
    #plt.imshow(canny,cmap="gray")

    # find lines
    linesP = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, None, 50, 20)
    
    line_list=[]
    if linesP is not None:
        for i in range(0, len(linesP)):
            lines = linesP[i][0]
            cv2.line(gray_roi, (lines[0],lines[1]), (lines[2],lines[3]), (255,0,0), 3, cv2.LINE_AA)

            x1,y1,x2,y2 = lines[0],lines[1],lines[2],lines[3]

            line_list.append([x1,y1,x2,y2])
    
  
    
    # follow right side of the road 
    if len(line_list)!=0:
        smallest_list=line_list[0]
        for line in line_list:
            if line[0]>smallest_list[0]:
                smallest_list=line
    
    x1,y1,x2,y2=smallest_list[0],smallest_list[1],smallest_list[2],smallest_list[3]
    try:
        slope= (y1-y2)/(x2-x1)
        slope = math.atan(slope)
        slope = math.degrees(slope)
        slope_angle_degrees=slope
    except:
        slope_angle_degrees=90
     

    cv2.line(roi,(x1,y1),(x2,y2),(100,100,0),4)

    print(slope_angle_degrees)
    
    if slope_angle_degrees<0:
        slope_angle_degrees=180+slope_angle_degrees # it will be negative when you use this angle with cosinus
        radian = math.radians(slope_angle_degrees)
        sin_angle = math.sin(radian)
        cos_angle=math.cos(radian)
         
        vx=3*cos_angle
        vy=3*sin_angle
        
        
    elif slope_angle_degrees>0 :
        radian = math.radians(slope_angle_degrees)
        sin_angle =(math.sin(radian))
        cos_angle=(math.cos(radian))

        if cos_angle<0.1:
            cos_angle=0
         
        vx=3*cos_angle
        vy=3*sin_angle
    else:
        print("horizontal")
        vy=0
        vx=1*vx_former


    if slope_angle_degrees is not None:
        text=f"degree :{str(slope_angle_degrees)} - vx = {str(vx)} - vy = {str(vy)}"
        cv2.putText(background,text, org = (15, 30), fontFace = cv2.FONT_HERSHEY_DUPLEX,fontScale = 0.4,color = (125, 246, 55), thickness = 1)
    else:
        cv2.putText(background,"cant find angle", org = (15, 30), fontFace = cv2.FONT_HERSHEY_DUPLEX,fontScale = 0.4,color = (125, 246, 55), thickness = 1)

     

    if vx>0 and vy!=0:
        y-=int(vy)+1
        x+=int(vx)+1
        vx_former=1
    elif vx>0 and vy==0:
        y-=0
        x+=int(vx)+1
        vx_former=1

    elif vx<0 and vy!=0:
        y-=int(vy)+1
        x+=int(vx)-1
        vx_former=1
    
    elif vx<0 and vy==0:
        y-=0
        x+=int(vx)-1
        vx_former=-1
    
    else:
        y-=1
        x+=0
        
    cv2.circle(background,(x,y),3,(255,0,0),3)

    time.sleep(0.05)
   

    cv2.imshow("gray_roi",gray_roi)
    cv2.imshow("roi",roi)
    cv2.imshow("thresh",thresh)
    cv2.imshow("background",background)
     
    k=cv2.waitKey(27)
    if k==27:
        break
        
    # refresh background
    background = cv2.imread("resources/clearred.png")
    #background=background[554:1200,:600,:3]
    
cv2.destroyAllWindows()