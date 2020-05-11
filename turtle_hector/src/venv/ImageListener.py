#!/usr/bin/env python
#uses ros_deep_learning can be found at https://github.com/dusty-nv/ros_deep_learning

from vision_msgs.msg import Detection2DArray #check import
from threading import Lock
import rospy

class ImageListener:
    #to debug run
    # rosrun image_publisher image_publisher __name:=image_publisher ~/jetson-inference/data/images/dog_0.jpg 
    # rosrun ros_deep_learning detectnet /detectnet/image_in:=/image_publisher/image_raw _model_name:=coco-dog
    # model will configure itself (TFT msgs) then publish
    # then look for print msg
    def __init__(self, minConf = 0.50):
        #start
        rospy.init_node('listener', anonymous=True)

        #set variables
        self.PoseLock = Lock()
        self.minConf = minConf #lowest value to trust a result
        self.timeStamp = rospy.get_rostime()
        self.validRes = []
        self.ImgNode = rospy.Subscriber('/detectnet/detections', Detection2DArray, self.DetectionCb) #subscriber to topic detections


    def DetectionCb(self, msg): # msg definition at http://docs.ros.org/api/vision_msgs/html/msg/Detection2DArray.html
        """ Simple Callback with ROS timestamp and list of Results above a certain confidence"""
        with self.PoseLock:
            self.timeStamp = msg.header.stamp
            self.validRes = (detect for detections in msg.detections for detect in detections.results if detect.score >= self.minConf)
	rospy.loginfo(msg.detections[0].results[0].pose.pose)

     # func could be replaced with rospy.sleep or loop while not rospy.core.is_shutdown(): ... some code ... rospy.rostime.wallsleep(0.5)
     # if not working

    
    def getPosQuat(self): #call with go_to() to move to an image
        """ returns msg as pos and orientation"""
        with self.PoseLock:
            if(self.validRes == []):
                rospy.loginfo("List is empty")
            else:
                Most_Confident = max(self.validRes, key = lambda item: item.score)
                return Most_Confident.pose.pose.position, Most_Confident.pose.pose.orientation
            return None, None

    def getTimeStamp(self):
        return timeStamp
        
#if __name__ == '__main__':# debugging loop. not for final use
#    image = ImageListener()
#    while not rospy.is_shutdown():
#        rospy.loginfo(image.getPosQuat())
#        rospy.sleep(0.5)
