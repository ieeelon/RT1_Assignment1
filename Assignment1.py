from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver). 
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py solutions/exercise3_solution.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
# grabbed_code = 41
# code_old = 0
# code = 0
# grabbed = 0
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=2
    rot_y = 90
    for token in R.see():
        if (token.dist < dist and -rot_y < token.rot_y < rot_y) and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            rot_y=token.rot_y
    if dist>=2:
        return -1, -1
    else:
        return dist, rot_y

# def mark_grabbed():
#     """
#     Function to find the grabbed silver token

#     Returns:
# 	dist (float): distance of the closest silver token (-1 if no silver token is detected)
# 	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
#     """
#     dist=2
#     for token in R.see():
#         if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
#             dist=token.dist
#             rot_y=token.rot_y
#             setattr(token.info, "code" , token.info.offset + 1)
#             new_code = token.info.code
#     if dist==2:
# 	    return -1, -1, -1
#     else:
#    	    return dist, rot_y, token.info.code

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    g_dist=0.6
    rot_y = 91
    for token in R.see():
        if token.dist < g_dist and -rot_y < token.rot_y < rot_y and token.info.marker_type is MARKER_TOKEN_GOLD:
            g_dist=token.dist
            g_rot_y=token.rot_y
            g_code=token.info.code
    if g_dist==0.6:
        return -1, -1, -1
    else:
        return g_dist, g_rot_y, g_code

def find_golden_token_left():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    g_dist=100
    rot_y = 10
    for token in R.see():
        if token.dist < g_dist and -90-rot_y < token.rot_y < -90+rot_y and token.info.marker_type is MARKER_TOKEN_GOLD:
            g_dist=token.dist
            g_rot_y=token.rot_y
            g_code=token.info.code
    if g_dist==100:
        return -1, -1, -1
    else:
        return g_dist, g_rot_y, g_code

def find_golden_token_right():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    g_dist=100
    rot_y = 10
    for token in R.see():
        if token.dist < g_dist and 90-rot_y < token.rot_y < 90+rot_y and token.info.marker_type is MARKER_TOKEN_GOLD:
            g_dist=token.dist
            g_rot_y=token.rot_y
            g_code=token.info.code
    if g_dist==100:
        return -1, -1, -1
    else:
        return g_dist, g_rot_y, g_code


while 1:

    # markers = R.see()
    # print ("I can see", len(markers), "markers:")

    # for m in markers:
    #     if m.info.marker_type in (MARKER_TOKEN_GOLD):
    #         print (" - Token {0} is {1} metres away".format( m.info.code, m.dist ))


# if grabbed_code > code:
    dist, rot_y = find_silver_token()
    print("FOUND SILVER COIN IN", dist)
    g_dist, g_rot_y, g_code = find_golden_token()
    print("CLOSEST DANGER is ", g_code, "IN", g_dist)
# else:
#     dist, rot_y, code = find_silver_token(grabbed)
#     print("LOOKING FOR A NEW TOKEN")
#     g_dist, g_rot_y, g_code = find_golden_token()
#     print("CLOSEST DANGER is ", g_code, "IN", g_dist)
# print(g_rot_y)

    if (dist==-1 or dist > 1.5) and (g_dist > 0.6 or g_dist == -1):
        print("I don't see any token!!")
        drive(25, 0.5)
    # elif dist!=-1 and grabbed_code == code and (g_dist > 1.5 or g_dist == -1):
    # elif dist <d_th and grabbed_code != code and (g_dist > 1.5 or g_dist == -1): # if we are close to the token, we try grab it.
    elif -1 < dist < d_th: # if we are close to the token, we try grab it.    
        print("Found it!")
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial positio
            print("Gotcha!")
            turn(27, 2)
            R.release()
            # grabbed +=1
            # grabbed_distance, grabbed_rot_y, grabbed_code = mark_grabbed()
            turn(-27, 2)
            drive(10, 0.5)
            # code_old = grabbed_code
            # print("THE TOKEN PLACED IS:", code_old)
        # else:
            # print("Aww, I'm not close enough.")

    elif -a_th<= rot_y <= a_th and (g_dist > 0.6 or g_dist == -1) and  dist < 1.5: # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(25, 0.5)
    elif (rot_y < -a_th) and dist < 1.5: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif (rot_y > a_th) and dist < 1.5:
        print("Right a bit...")
        turn(2, 0.5)
    elif (-90 < g_rot_y < -30) and (-1< g_dist < 0.6): # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Obstacle on the left")
        turn(5, 2)
        drive(25, 1)
    elif (30 < g_rot_y < 90) and (-1< g_dist < 0.6):
        print("Obstacle on the right")
        turn(-5, 2)
        drive(25, 1)
    elif (-30 <= g_rot_y <= 30) and (-1< g_dist < 0.6):
        print("Obstacle in front")
        dleft, aleft, cleft = find_golden_token_left()
        dright, aright, cright = find_golden_token_right()
        if dleft > dright:
            drive(-30, 2)
            turn(-8, 2)     
        else:
            drive(-30, 2)
            turn(8, 2)







    

