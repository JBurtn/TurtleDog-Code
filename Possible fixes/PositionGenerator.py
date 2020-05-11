import random
import rospy
from nav_msgs import OccupancyGrid, Odometry
from tf import TransformListener

class PositionGenerator:
    def __init__(self):
        self.tf = TransformListener()
        self.Position = 0
        self.Quarternion = 0
        self.Position = 0
        self.Occupancy = 0
        self.sub_once = rospy.Subscriber("/map", OccupancyGrid, self.callMap)
        

    def callMap(self, data):
        self.MapX = data.info.origin.position
        self.MapY = data.info.origin.orientation
        self.Resolution = data.info.resoluiton
        self.Occupancy = [(x,y) for y in range(data.info.height) 
        for x in range(data.info.height) if(data.data[y*data.info.width + x]) == 0 ]
        
        #for x in range(data.info.width):
        #    for y in range(data.info.width):

    def calculatePosition(self):
        """ Reads Position from Transform data and Calculates its position relative to the map. Does not use any innate Corrections"""
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, _ = self.tf.lookupTransform("/base_link", "/map", t)
            return (abs((position[0] - self.MapX)/self.Resolution),
            abs((position[1] - self.MapY)/self.Resolution))
        return (0,0)
    

    def RandomPosition(self, seed = 1):
        """ Selects a Random Value from the list and Returns a distance to it from the robots current Position"""
        random.seed(seed)
        while True:
            if not self.Resolution == None:
                x = random.choice(self.Occupancy)
                basex, basey = self.calculatePosition()
                SelectedX = abs((x[0] - self.MapX)/self.Resolution)
                SelectedY = abs((x[1] - self.MapY)/self.Resolution)
                yield SelectedX - basex , SelectedY - basey




