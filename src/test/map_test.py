#!/usr/bin/env python

from nav_msgs.msg import OccupancyGrid
import rospy
import math
from PIL import Image
from PIL.ImageOps import flip, grayscale, invert

topic = "moving_map"
publisher = rospy.Publisher(topic, OccupancyGrid, queue_size=1)

rospy.init_node("map_test")

grid = OccupancyGrid()

t = 0

image = flip(grayscale(Image.open("../../images/splash.png")))

while not rospy.is_shutdown():
    grid.header.frame_id = "map"
    grid.header.stamp = rospy.Time.now()
    grid.info.map_load_time = rospy.Time.now()
    grid.info.resolution = 0.02
    grid.info.width = image.width
    grid.info.height = image.height
    grid.info.origin.position.x = math.cos(t)
    grid.info.origin.position.y = math.sin(t)
    grid.info.origin.orientation.w = 1.0

    image = invert(image)
    grid.data = [x - 128 for x in image.getdata()]

    # Publish the OccupancyGrid
    publisher.publish(grid)

    rospy.sleep(2)
    t += 1
