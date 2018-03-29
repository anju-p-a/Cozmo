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

'''This Program creates two custom wall objects and cozmo will  on recognizing those custom objects
will move as programmed"
.

You can adjust the markers, marker sizes, and object sizes to fit whatever
object you have and the exact size of the markers that you print out.
'''

import time
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps
isLeft = [ False ]# these variables are set unset when the objects appear /dissapear
isRight = [ False ]

#will set the default position cozmo's head upon start
def default_position_upon_start(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(0)).wait_for_completed()

def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        #if the object is a diamond 2
        if(evt.obj.object_type == CustomObjectTypes.CustomType00):
            isLeft[0] = True
        #if the object is hexagon 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
            isRight[0] = True



def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    #if the object is a diamond 2
    if(evt.obj.object_type == CustomObjectTypes.CustomType00):
        isLeft[0] = False
    #if the object is hexagon 5
    elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
        isRight[0] = False


def action_on_seeing_object(robot: cozmo.robot.Robot):
    if(isLeft[0] == True):
        robot.drive_straight(distance_mm(100), speed_mmps(70)).wait_for_completed()
        robot.turn_in_place(degrees(90)).wait_for_completed()

    if(isRight[0] == True):
        robot.drive_straight(distance_mm(100), speed_mmps(70)).wait_for_completed()
        robot.turn_in_place(degrees(-90)).wait_for_completed()



def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    default_position_upon_start(robot)



    # define a unique wall (150mm x 120mm (x10mm thick for all walls)
    # with a 50mm x 30mm Circles2 image on front and back
    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Hexagons5,
                                              150, 120,
                                              50, 30, True)
    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                CustomObjectMarkers.Diamonds2,
                                                150, 120,
                                                50, 30, True)

    if ((wall_obj1 is not None) and (wall_obj2 is not None)):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")

    print("Press CTRL-C to quit")
    while True:
        #time.sleep(0.1)
        action_on_seeing_object(robot)


cozmo.run_program(custom_objects, use_3d_viewer=False, use_viewer=True)
