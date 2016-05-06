import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# read image and thresholding
img = cv.imread('office.jpg',0)
columes,rows=img.shape
for i in range(columes):
  for j in range(rows):
      if img[i,j]>128:
          img[i,j]=255
      else:
          img[i,j]=0

# list out the original position and goal position
robot_pos_start=(100,100)
margin_len=2
goal_pos=(100,171)
img2=np.copy(img)
        
def countingCostMap(original,image):
    image1=np.copy(image)
    image_c,image_r=image1.shape
    costmap=np.zeros((image_c,image_r),np.float)
    # img[original[0],original[1]]=254
    seed_l=[original]
    costmap_count=sum(sum(image>128))
    # print costmap_count
    cost=1
    # print seed_l[0]
    allseed=1
    while allseed<costmap_count-1:
        seed_t=[]
        for i in range(len(seed_l)):
            for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if((image1[seed_l[i][0]+j,seed_l[i][1]+k]==255)&(j!=k)&((j+k)!=0)):
                        image1[seed_l[i][0]+j,seed_l[i][1]+k]=255-cost
                        costmap[seed_l[i][0]+j,seed_l[i][1]+k]=cost
                        seed_t.append((seed_l[i][0]+j,seed_l[i][1]+k))
        seed_l=seed_t
        allseed+=len(seed_t)
        cost+=1
        # if cost>250:
        #     cost=250
        if len(seed_t)==0:
            break

    return costmap

def findPath():
    robot_pos_now=robot_pos_start
    costmap_now=countingCostMap(robot_pos_start,img)
    
    while costmap_now[goal_pos[0],goal_pos[1]]>1:
        costmap_near=[]
        for j in [-1,0,1]:
                for k in [-1,0,1]:
                    if img[robot_pos_now[0]+j,robot_pos_now[1]+k]==255:
                        costmap_temp=countingCostMap((robot_pos_now[0]+j,robot_pos_now[1]+k),img)
                        costmap_near.append([robot_pos_now[0]+j,robot_pos_now[1]+k,costmap_temp[goal_pos[0],goal_pos[1]]])

        costmap_temp_min=np.argmin(costmap_near,axis=0)
        robot_pos_now=(costmap_near[costmap_temp_min[2]][0],costmap_near[costmap_temp_min[2]][1])
        print robot_pos_now
        costmap_now=countingCostMap(robot_pos_now,img)
        print costmap_now[goal_pos[0],goal_pos[1]]
        costmap_max=np.amax(costmap_now)
        costmap_min=np.amin(costmap_now)
        costmap_start=255*(costmap_now-costmap_min)/(costmap_max-costmap_min)
        img_costmap=costmap_start.astype(np.uint8)
        for i in range(columes):
            for j in range(rows):
                if img_costmap[i,j]!=0:
                    img_costmap[i,j]=255-img_costmap[i,j]
        
        cv.imshow('costmap_now',img_costmap)
        cv.waitKey(10)

def findPathQuick():
    robot_pos_now=robot_pos_start
    costmap=countingCostMap(goal_pos,img)
    costmap_max=np.amax(costmap)
    costmap_min=np.amin(costmap)
    costmap_union=255*(costmap-costmap_min)/(costmap_max-costmap_min)
    img_costmap=costmap_union.astype(np.uint8)        
    for i in range(columes):
        for j in range(rows):
            if img_costmap[i,j]!=0:
                img_costmap[i,j]=255-img_costmap[i,j]
    
    #cv.imwrite('costmap_goal.png',img_costmap)

    while costmap[robot_pos_now[0],robot_pos_now[1]]>1:
        costmap_near=[]
        for j in [-1,0,1]:
                for k in [-1,0,1]:
                    # print img2[robot_pos_now[0]+j,robot_pos_now[1]+k]
                    if (img2[robot_pos_now[0]+j,robot_pos_now[1]+k]==255)&((j!=0)|(k!=0)):
                        costmap_temp=costmap[robot_pos_now[0]+j,robot_pos_now[1]+k]
                        # img2[robot_pos_now[0]+j,robot_pos_now[1]+k]=0
                        costmap_near.append([robot_pos_now[0]+j,robot_pos_now[1]+k,costmap_temp])
        costmap_temp_min=np.argmin(costmap_near,axis=0)
        print costmap_near
        robot_pos_now=(costmap_near[costmap_temp_min[2]][0],costmap_near[costmap_temp_min[2]][1])
        print robot_pos_now
        print costmap[robot_pos_now[0],robot_pos_now[1]]
        cv.circle(img_costmap,(robot_pos_now[1],robot_pos_now[0]),2,(0,0,255),1)
        cv.imshow('costmap_show',img_costmap)
        cv.waitKey(100)




    

findPathQuick()







        







    
