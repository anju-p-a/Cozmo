#!/usr/bin/env python3

# Copyright (c) 2017 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''This example demonstrates how you can define custom objects.

The example defines several custom objects (2 cubes, a wall and a box). When
Cozmo sees the markers for those objects he will report that he observed an
object of that size and shape there.

You can adjust the markers, marker sizes, and object sizes to fit whatever
object you have and the exact size of the markers that you print out.
'''

import time
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps
isLeft = [ False ]
isRight = [ False ]


def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        #if the object is a diamond 2
        if(evt.obj.object_type == CustomObjectTypes.CustomType00):
            isLeft[0] = True
            print(isLeft)


        #if the object is hexagon 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
            isRight[0] = True

            #print("Cozmo started seeing a %s" % str(evt.obj.object_type))


def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    #if the object is a diamond 2
    if(evt.obj.object_type == CustomObjectTypes.CustomType00):
        isLeft[0] = False



    #if the object is hexagon 5
    elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
        isRight[0] = False


def go_to_object_test(robot: cozmo.robot.Robot):
    robot.go_to_object(CustomObjectTypes.CustomType00, distance_mm(70.0))

def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    #robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)



    # define a unique wall (150mm x 120mm (x10mm thick for all walls)
    # with a 50mm x 30mm Circles2 image on front and back
    wall_obj = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Hexagons5,
                                              150, 120,
                                              50, 30, True)
    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                CustomObjectMarkers.Diamonds2,
                                                150, 120,
                                                50, 30, True)



    if ((wall_obj is not None) and (wall_obj2 is not None)):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")



    print("Press CTRL-C to quit")
    while True:
        #time.sleep(0.1)

        if(isLeft[0] == True):
            robot.turn_in_place(degrees(90)).wait_for_completed()
            robot.drive_straight(distance_mm(100), speed_mmps(70)).wait_for_completed()
        if(isRight[0] == True):
            robot.turn_in_place(degrees(-90)).wait_for_completed()
            robot.drive_straight(distance_mm(100), speed_mmps(70)).wait_for_completed()





cozmo.run_program(custom_objects, use_3d_viewer=True, use_viewer=True)
