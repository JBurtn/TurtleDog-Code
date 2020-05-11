from gernextposition import gernextposition
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def movebase_client(x , y): 

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose_header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position = x
    goal.target_pose.pose.orientation = y

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    sum = 0
    Rate_of_success = 0
    resultDictionary = {#find correct call for result
            actionlib.GoalStatus.SUCCEEDED: (1.0, 1.0, "Goal Success"),
            actionlib.GoalStatus.ABORTED: (0.0, 1.0, "Goal Failure" ),
            actionlib.GoalStatus.PREEMPTED: (0.0, 0.0, "Preempted")
        }
    try:
        gen = gernextposition()
        rospy.init_node('movebase_client_py')
        while not rospy.is_shutdown():
            x, y = next(gen.RandomPosition())        
            if not x  == None and not y == None:
                result = movebase_client(x, y)
                sum += resultDictionary[result][1]
                Rate_of_success += resultDictionary[result][0]
                rospy.loginfo("Rate of success {:0.5f}".format(Rate_of_success/sum) )
            
                rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished")