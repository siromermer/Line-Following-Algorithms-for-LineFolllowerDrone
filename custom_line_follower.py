import cv2
import numpy as np 
import matplotlib.pyplot as plt
import time 
import math

"""
    IMPORTANT !!!!!!!!!!
    
    Follow lines without any opencv Line Detector function using only image matrix

    It is all about slope . you decide y1 and y2 . After choosing them you are gonna find index of  most right 255  for y1 andy2x2 seperately<br>
    In this way you are gonna obtain x1 y1 x2 y2 . You can find slope and use it for acceleration
"""

"""
    WARNING : OpenCV coordinate system in little bit weird . Y values increasing when you go down  
"""

#  background path image
# for different angles background = cv2.imread("resources/mix.png")

background = cv2.imread("resources/bg_hard.png")

# initial coordiantes of drone
x=165
y=640

# velocity parameters
vx=0
vy=1

# slope degree , random value in beginning 
slope_angle_degrees=9999
 

while True : 
    # consider roi as drones camera    
    roi = background[y-100:y+100,x-50:x+150]
    # convert gray scale
    gray_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    # create binary image
    ret ,thresh = cv2.threshold(gray_roi,50,255,cv2.THRESH_BINARY)
 
    
  
    # !!!!!!!!! if it can not find points (it means road become horizontal it will give error in that case it will go except block)
    try:
    
        """
            here try to find most right 255's index in y=100  
        """

        # find most right 255 values index
        """
            if there is not any 255 values  np.where(thresh[100][::-1] == 255)[0][0] this gives error , that means it is going horizontal , so it goes except block
        """
        index = np.where(thresh[100][::-1] == 255)[0][0]
        # find most right 255 index in 100th column
        first_index = len(thresh[100]) - 1 - index

        """
            here try to find most right 255's index in y=110  
        """
        # find most right 255 values index
        index = np.where(thresh[110][::-1] == 255)[0][0]
        # find most right 255 index in 110th column
        second_index = len(thresh[110]) - 1 - index
        
        # define points
        x1,y1,x2,y2=first_index , 110 , second_index , 100
        # draw line 
        
        cv2.line(roi,(x2,y2),(x1,y1),(255,0,0),2)

    except:
        # this part is for horizontal roads
        
        # give random values
        x1,y1,x2,y2=1,2,1,4
     
    # if road is not horizontal or vertical(we understant x1!=x2  if it is vertical)
    if x1!=x2:  
        slope=(y2-y1)/(x2-x1)
        slope_angle_radians = math.atan(slope)
        slope_angle_degrees = math.degrees(slope_angle_radians)
        

        if slope_angle_degrees<0:
            slope_angle_degrees=180+slope_angle_degrees # it will be negative when you use this angle with cosinus
            radian = math.radians(slope_angle_degrees)
            sin_angle = math.sin(radian)
            cos_angle=math.cos(radian)
            vx=3*cos_angle
            vy=3*sin_angle
            
            
        else:
            radian = math.radians(slope_angle_degrees)
            sin_angle = math.sin(radian)
            cos_angle=math.cos(radian)
            vx=3*cos_angle
            vy=3*sin_angle
    
    # if road is horizontal or vertical
    else:
        # horizontal 
        if np.all(thresh[100] == 0) and np.all(thresh[90] == 0):
            if vx<0:
                slope_angle_degrees=180
                vx=-4
                vy=0
            else:
                slope_angle_degrees=0
                vx=4
                vy=0

        # vertical
        else:
            vx=0
            vy=3
            slope_angle_degrees=90
        

    if slope_angle_degrees is not None:
        text=f"degree :{str(slope_angle_degrees)} - vx = {str(vx)} - vy = {str(vy)}"
        cv2.putText(background,text, org = (15, 30), fontFace = cv2.FONT_HERSHEY_DUPLEX,fontScale = 0.4,color = (125, 246, 55), thickness = 1)
    else:
        cv2.putText(background,"cant find angle", org = (15, 30), fontFace = cv2.FONT_HERSHEY_DUPLEX,fontScale = 0.4,color = (125, 246, 55), thickness = 1)

    

    if vx>0:
        # go right horizontally
        if vx==4:
            y-=0
            x+=int(vx)-1
        # go right with angle 
        else:
            y-=int(vy)+1
            x+=int(vx)+1

    elif vx<0:
        # go left horizontally
        if vx==-4:
            y-=0
            x+=int(vx)-1
        # go left with angle 
        else:
            y-=int(vy)+1
            x+=int(vx)-1
    else:
        y-=int(vy)+1
        x+=0
        
    cv2.circle(background,(x,y),3,(255,0,0),3)

    time.sleep(0.05)
   

    cv2.imshow("roi",roi)
    cv2.imshow("thresh",thresh)
    cv2.imshow("background",background)
     
    k=cv2.waitKey(27)
    if k==27:
        break
        
    # refresh background
    background = cv2.imread("resources/bg_hard.png")
    #background=background[554:1200,:600,:3]
    
cv2.destroyAllWindows()