#! /usr/bin/env python

import rospy
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion, \
                                TwistStamped, Twist, Vector3
from std_msgs.msg import Header
import tf
import math
from marker_navigator.srv import SetPosition, \
    SetPositionYawRate, \
    SetVelocity, \
    SetVelocityYawRate, \
    SetAttitude, \
    SetAttitudeYawRate, \
    SetRatesYaw, \
    SetRates

set_position = rospy.ServiceProxy('/set_position', SetPosition)
set_position_yaw_rate = rospy.ServiceProxy('/set_position/yaw_rate', SetPositionYawRate)

set_velocity = rospy.ServiceProxy('/set_velocity', SetVelocity)
set_velocity_yaw_rate = rospy.ServiceProxy('/set_velocity/yaw_rate', SetVelocityYawRate)

set_attitude = rospy.ServiceProxy('/set_attitude', SetAttitude)
set_attitude_yaw_rate = rospy.ServiceProxy('/set_attitude/yaw_rate', SetAttitudeYawRate)

set_rates_yaw = rospy.ServiceProxy('/set_rates/yaw', SetRatesYaw)
set_rates = rospy.ServiceProxy('/set_rates', SetRates)

#release = rospy.ServiceProxy('/release', Trigger)
set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        
def land():
    assert set_mode(custom_mode="AUTO.LAND").success
        
def takeoff(altitude=2.5):
    set_position(z=altitude, frame_id='local_origin')

def twist(rate=0.1):
    rospy.loginfo("Twist vs rate {}".format(rate))
    set_velocity_yaw_rate(yaw_rate=rate, frame_id='local_origin')

def ring(rad=1, angular=1):
    set_velocity_yaw_rate(
        vx=rad*angular, vy=0.0, vz=0, yaw_rate=angular, 
        frame_id='fcu_horiz', update_frame=True)

if __name__ == '__main__':
    rospy.init_node('test_movements')
    rospy.sleep(1)
    takeoff()
    rospy.sleep(5)
    tilt(rate=1)
    #land()
    #rospy.sleep(1)
    rospy.spin()

    
    

