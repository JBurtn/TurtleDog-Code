#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import random
from nav_msgs.msg import OccupancyGrid, Odometry
from tf import TransformListener


def callMap(data):
	MapX = data.info.origin.position.x
	MapY = data.info.origin.position.y
	Resolution = data.info.resolution
	Occupancy = [(x,y) for y in range(data.info.height) for x in range(data.info.height) if(data.data[y*data.info.width + x] == -1)]
	rospy.loginfo(MapX)
	rospy.loginfo(Occupancy[4096])
	while not rospy.is_shutdown():	    
	    x, y = next(RandomPosition(Occupancy, float(MapX), float(MapY), float(Resolution))
	    rospy.loginfo((x, y))

def calculatePosition():
     """ Reads Position from Transform data and Calculates its position relative to the map. Does not use any innate Corrections"""
     tf = TransformListener()
     if tf.frameExists("/base_link") and tf.frameExists("/map"):
	t = tf.getLatestCommonTime("/base_link", "/map")
	position, _ = tf.lookupTransform("/base_link", "/map", t)
	return (abs((position[0] - MapX)/Resolution),
	    abs((position[1] - MapY)/Resolution))
     return (0,0)


def RandomPosition(Occupancy, MapX, MapY, Resolution):
    """ Selects a Random Value from the list and Returns a distance to it from the robots current Position"""
    random.seed(10)
    x = random.choice(Occupancy)
    while True:
	basex, basey = calculatePosition()
	SelectedX = abs((x[0] - MapX)/Resolution)
	SelectedY = abs((x[1] - MapY)/Resolution)
	yield SelectedX - basex , SelectedY - basey
	x = random.choice(Occupancy)

def movebase_client(x = 0.5 , y = 1.0): 

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose_header.frame_id = "/map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def main():
    sum = 0
    Rate_of_success = 0
    try:
        rospy.init_node('movebase_client_py')
	rospy.Subscriber("/map", OccupancyGrid, callMap)
	rospy.spin()
	#result = movebase_client(x, y)
        resultDictionary = {#find correct call for result
            actionlib.GoalStatus.SUCCEEDED: (1.0, 1.0, "Goal Success"),
            actionlib.GoalStatus.ABORTED: (0.0, 1.0, "Goal Failure" ),
            actionlib.GoalStatus.PREEMPTED: (0.0, 0.0, "Preempted")
        }
        if result:
            sum += resultDictionary[result][1]
            Rate_of_success += resultDictionary[result][0]
            rospy.loginfo("Rate of success {:0.5f}".format(Rate_of_success/sum) )
            
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished")

if __name__ == "__main__":
    main()
