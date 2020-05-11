#!/usr/bin/env python
import random
import rospy
from nav_msgs.msg import OccupancyGrid, Odometry
from tf import TransformListener

class PositionGenerator:
    PositionGenerator.MapX = 0
    MapY = 0
    Resolution = 0.0
    Occupancy = []

    def __init__(self):
        self.tf = TransformListener()
        rospy.Subscriber("findBaseSet", OccupancyGrid, self.callMap)
	
	
    def callOdom(self, odo, x, y):
        x = odo.pose.pose.position.x
        y = odo.pose.pose.position.y

    def callMap(self, data):
        PositionGenerator.MapX = data.info.origin.position.x
        PositionGenerator.MapY = data.info.origin.position.y
        PositionGenerator.Resolution = data.info.resoluiton
        PositionGenerator.Occupancy = [(x,y) for y in range(data.info.height) 
        for x in range(data.info.height) if(data.data[y*data.info.width + x] == -1)]
	rospy.loginfo(PositionGenerator.Occupancy)
        rospy.loginfo(PositionGenerator.MapX)
        #for x in range(data.info.width):
        #    for y in range(data.info.width):

    def calculatePosition(self):
        """ Reads Position from Transform data and Calculates its position relative to the map. Does not use any innate Corrections"""
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, _ = self.tf.lookupTransform("/base_link", "/map", t)
            return (abs((position[0] - PositionGenerator.MapX)/PositionGenerator.Resolution),
            abs((position[1] - PositionGenerator.MapY)/PositionGenerator.Resolution))
        return (0,0)
    

    def RandomPosition(self, seed = 1):
        """ Selects a Random Value from the list and Returns a distance to it from the robots current Position"""
        random.seed(seed)
        for x in random.randrange(0, PositionGenerator.MapY* PositionGenerator.MapX):
            basex, basey = self.calculatePosition()
            SelectedX = abs((PositionGenerator.Occupancy[x][0] - PositionGenerator.MapX)/PositionGenerator.Resolution)
            SelectedY = abs((PositionGenerator.Occupancy[x][1] - PositionGenerator.MapY)/PositionGenerator.Resolution)
            yield SelectedX - basex , SelectedY - basey




