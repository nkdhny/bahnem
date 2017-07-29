#! /home/nkdhny/Documents/bahnem/devel/env.sh python

import rospy
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from std_msgs.msg import Header
import tf

class Copter(object):

    ARMING_SERVICE = "/mavros/cmd/arming"
    TAKOFF_SERVICE = "/mavros/cmd/takeoff"
    SET_POINT_LOCAL_POSITION = "/bahnem/setpoint_position/local"

    def _wait_services(self):
        rospy.wait_for_service(Copter.ARMING_SERVICE)
        rospy.wait_for_service(Copter.TAKOFF_SERVICE)

    def __init__(self):
        self._is_armed = False

        self._wait_services()
        self._arming_service = rospy.ServiceProxy(Copter.ARMING_SERVICE, CommandBool)
        self._takoff_service = rospy.ServiceProxy(Copter.TAKOFF_SERVICE, CommandTOL)        
        self._set_position_local = rospy.Publisher(
            Copter.SET_POINT_LOCAL_POSITION, PoseStamped, queue_size=10)

        self._set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)

        self.arm()

    def arm(self):
        assert not self._is_armed
        assert self._set_mode(custom_mode="OFFBOARD").success
        self._is_armed = self._arming_service(True).success

        if self._is_armed:
            rospy.loginfo("Copter armed")
        else:
            rospy.logwarn("Copter arming failed")


    def disarm(self):
        assert self._is_armed
        if self._arming_service(False).success:
            self._is_armed = False
            rospy.loginfo("Copter disarmed")
        else:
            rospy.logwarn("Copter disarming failed")
        

def takeoff(copter, altitude=2.5):
    assert copter._is_armed
    target_local_pose = PoseStamped(
        pose=Pose(
            position=Point(z=altitude), 
            orientation=Quaternion(*tf.transformations.quaternion_from_euler(0, 0, 0))
        ), header=Header(stamp=rospy.get_rostime(), frame_id='local_origin')
    )
    copter._set_position_local.publish(target_local_pose)
    
if __name__ == '__main__':
    rospy.init_node('test_movements')
    rospy.sleep(2)
    copter = Copter()
    rospy.sleep(1)
    takeoff(copter)
    rospy.spin()

    
    

