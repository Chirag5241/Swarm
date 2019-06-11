import numpy as np
import cv2
import cv2.aruco as aruco
import math
import serial
import paho.mqtt.client as paho

print("00000")
#initialising lists
bot_ini_pos = np.zeros((20,3))#to be provided by localization team in format (x_coord,y_coord,0). Bots then sorted according to priority 

bot_ini_pos[0][0]= 200
bot_ini_pos[0][1]= 400
bot_ini_pos[0][2]= 0
bot_ini_pos[1][0]= 100
bot_ini_pos[1][1]= 300
bot_ini_pos[1][2]= 0

bot_final_pos = np.zeros((20,2))#calculated using dynamic allocation of setpoints (x_coord,y_coord)

bot_ini_pos[0][0]= 300
bot_ini_pos[0][1]= 100
bot_ini_pos[0][2]= 0
bot_ini_pos[1][0]= 300
bot_ini_pos[1][1]= 500
bot_ini_pos[1][2]= 0

all_path = []
path = []

gittest = 0
t=0
z=0
i=0
g=0
h=0
f=0
f_min=0
total_bots = 2
obs_len = 0

obstacles = []

avoid_crossing = []
reject = 0

#cap = cv2.VideoCapture(0)

cam_units = 10
cam_grid = 1

while(i<total_bots):
    
    #take particular bot information
    start_node = bot_ini_pos[i] #(x_coord,y_coord,0)
    #print(start_node)
    end_node = bot_final_pos[i]
    x_end = end_node[0]
    y_end = end_node[1]
    curr_node = start_node
    x = curr_node[0]
    y = curr_node[1]
    #print(x)
    
    while(curr_node[0] != end_node[0] and curr_node[1] != end_node[1]): #checking that goal has not been reached
        #print("True")
        next_options = [[x,y],[x+1,y+1],[x-1,y+1],[x-1,y-1],[x+1,y-1],[x+1,y],[x-1,y],[x,y-1],[x,y+1]]#possible spaces to move ignoring time co-ordinate
        print(next_options)
        g=g+1#bot can travel only one unit in one unit of time
        obs_len = len(obstacles)
        #print("True")
        while(z<9):#checking best possible next option

            while(obs_len>0):#checking that next_move is not in the obstacle list
                #print("True")
                if next_options[z][0] == obstacles[obs_len][0] and next_options[z][1] == obstacles[obs_len][1]:
                    reject = 1
                obs_len = obs_len-1
                       
            if reject == 0 :   
                #print("false")         
                possible_x = next_options[z][0]
                possible_y = next_options[z][1]
                h = math.sqrt ((x_end-possible_x)*(x_end-possible_x) + (y_end-possible_y)*(y_end-possible_y))#calculation of heuristic#########################
                f=g+h
                if z==0: #checking best next node
                    f_min = f
                    z=z+1

                elif z!=0:
                    if f<f_min:
                        f_min = f
                        curr_node = next_options[z]#current node of bot
                        z=z+1
            elif reject == 1:
                z=z+1

        curr_node[2] = curr_node[2] + t#adding time co-ordinate to bot
        t = t+1
        path.append(curr_node)
        
    all_path.append(path)
    

    #adding obstacles according to priority . The ith path is now declared as an obstacle for the remaining bots
    
    obstacles.append(all_path[i])
    avoid_crossing = all_path[i]#adding list for avoiding head on collisions
    p = len(all_path[i])-1
    while(p>=0):#incrementing time co ordinate
        avoid_crossing[p][2] = avoid_crossing[p][2] + 1
        p = p-1

    obstacles.append(avoid_crossing)#final obstacle list

    #reinitialising the parameters for the next bot
    path = []
    i = i+1
    f=0
    g=0
    h=0
    reject = 0

#Printing all paths
bot_num = 2
while(bot_num>0):
    printf("The respective path of bot_number" + bot_num + "is :" + all_path[bot_num])
    bot_num = bot_num - 1
