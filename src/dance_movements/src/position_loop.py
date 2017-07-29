#! /home/nkdhny/Documents/bahnem/devel/env.sh python

import rospy
from geometry_msgs.msg import PoseStamped, Pose, Quaternion, Point
import tf
from std_msgs.msg import Header

class Loop(object):
    def __init__(self):
        self._target_local_pose = PoseStamped(
            pose=Pose(
                position=Point(), 
                orientation=Quaternion(*tf.transformations.quaternion_from_euler(0, 0, 0))
            ), header=Header(stamp=rospy.get_rostime(), frame_id='local_origin')
        )

        self._set_position_local = rospy.Publisher(
            '/mavros/setpoint_position/local', PoseStamped, queue_size=10)

    def __call__(self, pose):
        self._target_local_pose = pose

    def publish(self):
        self._target_local_pose.header.stamp = rospy.get_rostime()
        self._set_position_local.publish(self._target_local_pose)

if __name__ == '__main__':
    rospy.init_node('position_loop')
    loop = Loop()
    rospy.Subscriber('/bahnem/setpoint_position/local', PoseStamped, loop)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        loop.publish()
        rate.sleep()
