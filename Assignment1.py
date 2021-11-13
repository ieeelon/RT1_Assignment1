from __future__ import print_function

import time
from sr.robot import *

"""
	$ python run.py Assignment1.py

"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
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

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	g_dist (float): distance of the closest golden token (-1 if no golden token is detected)
	g_rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    g_code (int): return a token's code value (-1 if no golden token is detected)
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
    Function to find the closest golden token to the left of the robot

    Returns:
	g_dist (float): distance of the closest golden token (-1 if no golden token is detected)
	g_rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    g_code (int): return a token's code value (-1 if no golden token is detected)
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
    Function to find the closest golden token to the right of the robot

    Returns:
	g_dist (float): distance of the closest golden token (-1 if no golden token is detected)
	g_rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    g_code (int): return a token's code value (-1 if no golden token is detected)
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

    dist, rot_y = find_silver_token() # the purpose of the assignment is to find the silver boxes
    print("FOUND SILVER COIN IN", dist)
    g_dist, g_rot_y, g_code = find_golden_token() # however, the robot also should avoid crashing into the golden boxes
    print("CLOSEST DANGER is ", g_code, "IN", g_dist)

    if (dist==-1 or dist > 1.5) and (g_dist > 0.6 or g_dist == -1): # no silver token seen to be close and it is safe as there are no golden boxes close as well
        print("I don't see any token close!")
        drive(25, 0.5)
    elif -1 < dist < d_th: # if we are close to the token, we try grab it.    
        print("Found it!")
        if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            turn(27, 2)
            R.release()
            turn(-27, 2)
            drive(10, 0.5)

    elif -a_th<= rot_y <= a_th and (g_dist > 0.6 or g_dist == -1) and  dist < 1.5: # silver token is locaeted and can be approached safely as the golden boxes don't block the way
        print("Ah, that'll do.")
        drive(25, 0.5)
    elif (rot_y < -a_th) and dist < 1.5: # helps robot to grab the silver box precisely if it is not alighned properply and robot should be rotated to the left
        print("Left a bit...")
        turn(-2, 0.5)
    elif (rot_y > a_th) and dist < 1.5: # helps robot to grab the silver box precisely if it is not alighned properply and robot should be rotated to the right
        print("Right a bit...")
        turn(2, 0.5)
    elif (-90 < g_rot_y < -30) and (-1< g_dist < 0.6): # avoiding obstacles appearing from the left side of the robot
        print("Obstacle on the left")
        turn(5, 2)
        drive(25, 1)
    elif (30 < g_rot_y < 90) and (-1< g_dist < 0.6): # avoiding obstacles appearing from the right side of the robot
        print("Obstacle on the right")
        turn(-5, 2)
        drive(25, 1)
    elif (-30 <= g_rot_y <= 30) and (-1< g_dist < 0.6): # this feature considers distances to the golden boxes to the left and to the right of the robot, when there is another golden box blocking the robot from the front
        print("Obstacle in front")
        dleft, aleft, cleft = find_golden_token_left() # look for the closest left golden box
        dright, aright, cright = find_golden_token_right() # look for the closest right golden box
        if dleft > dright: # if left golden box is farther, then the direction towards it is safer
            drive(-30, 2)
            turn(-8, 2)     
        else:
            drive(-30, 2) # if right golden box is farther, then the direction towards it is safer
            turn(8, 2)







    

