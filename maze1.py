#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
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

'''Tell Cozmo to find a cube, and then drive up to it

This is a test / example usage of the robot.go_to_object call which creates a
GoToObject action, that can be used to drive within a given distance of an
object (e.g. a LightCube).
'''

import asyncio
import random

import cozmo
from cozmo.util import degrees, distance_mm,time,distance_inches,speed_mmps
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.behavior import BehaviorTypes

isHex5 = [ False ]
isHex4 = [ False ]
isDiamond2 = [ False ]

def default_position_upon_start(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(0)).wait_for_completed()
    robot.set_lift_height(height=0).wait_for_completed()


def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, CustomObject):
        #if the object is a diamond 2
        if(evt.obj.object_type == CustomObjectTypes.CustomType00):
            isDiamond2[0] = True
        #if the object is hexagon 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
            isHex5[0] = True
        #if the object is hexagon 4
        elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
            isHex4[0] = True

def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    #if the object is a diamond 2
    if(evt.obj.object_type == CustomObjectTypes.CustomType00):
        isDiamond2[0] = False
    #if the object is hexagon 5
    elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
        isHex5[0] = False
    #if the object is hexagon 4
    elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
        isHex4[0] = False

def custom_objects(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)


    default_position_upon_start(robot)

    # define a unique wall (150mm x 120mm (x10mm thick for all walls)
    # with a 38mm x 38mm Circles2 image on front and back
    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Hexagons5,
                                              38, 38,
                                              38, 38,True)
    #wall_obj1.object_id = 123456

    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                CustomObjectMarkers.Diamonds2,
                                                38, 38,
                                                38, 38,True)
    wall_obj3 = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                               CustomObjectMarkers.Hexagons4,
                                               150, 120,
                                               50, 30,True)
    cube_obj4 = robot.world.define_custom_cube(CustomObjectTypes.CustomType03,
                                              CustomObjectMarkers.Diamonds4,
                                              57,
                                              25, 25,True)

    if ((wall_obj1 is not None) and (wall_obj2 is not None)) and (wall_obj3 is not None):
        print("All objects defined successfully!")

    else:
        print("One or more object definitions failed!")

    print("Press CTRL-C to quit")
    while True:
        #time.sleep(0.1)
        action_on_seeing_object(robot)

def action_on_seeing_object(robot: cozmo.robot.Robot):

        if isHex4[0]:
                rand = random.randint(0,2)
                print("This is the random value")
                print(rand)
                wall = robot.world.wait_until_observe_num_objects(num=1,
                                                              object_type=cozmo.objects.CustomObject,
                                                              timeout=1)
                if wall:
                    robot.go_to_pose(wall[0].pose, relative_to_robot=False, in_parallel=False, num_retries=0).wait_for_completed()
                    robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()
                    robot.say_text("What the????").wait_for_completed()
                    robot.drive_straight(distance_inches(-3.5), speed_mmps(30)).wait_for_completed()
                    if(rand == 0):
                        robot.turn_in_place(degrees(90)).wait_for_completed()
                    else:
                        robot.turn_in_place(degrees(-90)).wait_for_completed()


                    #robot.drive_straight(distance_inches(-3), speed_mmps(70)).wait_for_completed()
                    #robot.drive_straight(distance_inches(3), speed_mmps(35)).wait_for_completed()
                    #robot.drive_straight(distance_inches(1), speed_mmps(85)).wait_for_completed()
                    #robot.say_text("You gotta be kidding me!").wait_for_completed()
                    #robot.turn_in_place(degrees(90)).wait_for_completed()
                    default_position_upon_start(robot);
        if isDiamond2[0]:
            wall = robot.world.wait_until_observe_num_objects(num=1,
                                                          object_type=cozmo.objects.CustomObject,
                                                          timeout=1)
            if wall:
                robot.go_to_pose(wall[0].pose, relative_to_robot=False, in_parallel=False, num_retries=0).wait_for_completed()
                robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()
                robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession, ignore_body_track=True).wait_for_completed()
                #robot.say_text("Ugh.").wait_for_completed()
                #robot.say_text("Careful Cozmo....").wait_for_completed()
                #robot.turn_in_place(degrees(180)).wait_for_completed()
                default_position_upon_start(robot);

        if isHex5[0]:
            wall = robot.world.wait_until_observe_num_objects(num=1,
                                                          object_type=cozmo.objects.CustomObject,
                                                          timeout=1)
            if wall:
                robot.go_to_pose(wall[0].pose, relative_to_robot=False, in_parallel=False, num_retries=0).wait_for_completed()
                robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()
                #robot.turn_in_place(degrees(-90)).wait_for_completed()
                #robot.say_text("How do I get out of here!?").wait_for_completed()
                #robot.drive_straight(distance_inches(2), speed_mmps(25)).wait_for_completed()
                #robot.turn_in_place(degrees(-180)).wait_for_completed()
                #robot.say_text("It's gotta be around here somewhere").wait_for_completed()
                #robot.drive_straight(distance_inches(8), speed_mmps(35)).wait_for_completed()
                #robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinSession, ignore_body_track=True).wait_for_completed()
                default_position_upon_start(robot);


cozmo.run_program(custom_objects, use_3d_viewer=True, use_viewer=True)
