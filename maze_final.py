#!/usr/bin/env python3

import asyncio
import random
import time
import sys

import cozmo
from cozmo.util import degrees, distance_mm,time,distance_inches,speed_mmps
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.behavior import BehaviorTypes

# global bools to set true and false depending on if it sees that particular custom object marker
isHex5 = [ False ]
isCircle5 = [False]
isDiamond5 = [False]
isTriangle5 = [False]
isHex2 = [False]
# The blocks shape
isDiamond3 = [False]
# if cozmo is busy doing something
isDoingSomething = [True]
# time tracker to keep track of idle time
time1 = [time.time()]
# bool triggers, set when idle time incrments to do diffrent actions
timeTrigger = [False,False,False,False,False]
# keep track of last turn, 0 for left 1 for right
lastTurn = [-1]
# bool for if cozmo made it to the end of the maze
isFinished = [False]

victory_reactions = ["anim_pounce_success_03",
"anim_speedtap_wingame_intensity02_02",
"anim_speedtap_wingame_intensity03_02",
"anim_speedtap_wingame_intensity03_03"]

thinking_reactions = ["anim_vc_reaction_whatwasthat_01","anim_vc_reaction_yesfaceheardyou_01","anim_codelab_getout_01"]

frustation_reactions = ["anim_dizzy_reaction_medium_02","anim_poked_01","anim_vc_reaction_nofaceheardyou_01","anim_codelab_kitchen_yucky_01"]






# list of diffrent sayings for cozmo to say
sayings = ["not again!",
           "where am I?",
           "I need help!",
           "for Pete's sake....",
           "oh no....",
           "Will I ever get out!",
           "This isn't funny!",
           "C'mon!",
           "hmmm...",
           "Why me?",
           "Maybe this way?",
           "I'll turn this way!"]

# set cozmo's head and lift to the default position
def default_position(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(0)).wait_for_completed()
    robot.set_lift_height(height=0).wait_for_completed()

# event handler for when cozmo sees a custom object marker
def handle_object_appeared(evt, **kw):
    if isinstance(evt.obj, CustomObject):
        #if the object is a diamond 5
        if(evt.obj.object_type == CustomObjectTypes.CustomType00):
            isDiamond5[0] = True
        #if the object is hexagon 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
            isHex5[0] = True
        #if the object is circle 5
        elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
            isCircle5[0] = True
        # if the object is triangle 5
        elif (evt.obj.object_type == CustomObjectTypes.CustomType03):
            isTriangle5[0] = True
        # if the object is hexagon 2
        elif (evt.obj.object_type == CustomObjectTypes.CustomType04):
            isHex2[0] = True
        elif (evt.obj.object_type == CustomObjectTypes.CustomType05):
            isDiamond3[0] = True

# event handle for when cozmo loses sight of a custom object marker
def handle_object_disappeared(evt, **kw):

    # if the object is a diamond 5
    if(evt.obj.object_type == CustomObjectTypes.CustomType00):
        isDiamond5[0] = False
    # if the object is hexagon 5
    elif(evt.obj.object_type == CustomObjectTypes.CustomType01):
        isHex5[0] = False
    # if the object is circle 4
    elif(evt.obj.object_type == CustomObjectTypes.CustomType02):
        isCircle5[0] = False
        # if the object is triangle 5
    elif (evt.obj.object_type == CustomObjectTypes.CustomType03):
        isTriangle5[0] = False
        # if the object is hexagon 2
    elif (evt.obj.object_type == CustomObjectTypes.CustomType04):
        isHex2[0] = False
    elif(evt.obj.object_type == CustomObjectTypes.CustomType05):
        isDiamond3[0] = False

def play_animations(robot: cozmo.robot.Robot, animationString):
    randomInt = random.randint(0,len(animationString)-1)
    #print(victory_reactions[randomInt])
    robot.play_anim(name=animationString[randomInt]).wait_for_completed()


# main program. starting point of execution
def mainProgram(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    # Add event handlers for whenever Cozmo loses sight of an object
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    default_position(robot)

    # define all the different walls related to shapes. Wall size: 50mm x 50mm x10mm, Shape size: 50mm x 50mm
    # hexagon 5
    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType01,
                                              CustomObjectMarkers.Hexagons5,
                                              50, 50,
                                              50, 50,True)
    # diamond 5
    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType00,
                                                CustomObjectMarkers.Diamonds5,
                                                50, 50,
                                                50, 50,True)
    # circle 5
    wall_obj3 = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                               CustomObjectMarkers.Circles5,
                                               50, 50,
                                               50, 50,True)
    # triangle 5
    wall_obj4 = robot.world.define_custom_wall(CustomObjectTypes.CustomType03,
                                              CustomObjectMarkers.Triangles5,
                                              50, 50,
                                              50, 50,True)
    # hexagon 2
    wall_obj5 = robot.world.define_custom_wall(CustomObjectTypes.CustomType04,
                                               CustomObjectMarkers.Hexagons2,
                                               50, 50,
                                               50, 50, True)
    #   diamond 3
    wall_obj6 = robot.world.define_custom_wall(CustomObjectTypes.CustomType05,
                                               CustomObjectMarkers.Diamonds3,
                                               50, 50,
                                               50, 50, True)


    # make sure the objects were defined without conflict
    if ((wall_obj1 is not None) and (wall_obj2 is not None)) and (wall_obj3 is not None) and (wall_obj4 is not None) and (wall_obj5 is not None) and (wall_obj6 is not None):
        print("All objects defined successfully!")
    else:
        print("One or more object definitions failed!")

    # if used in a console this would be helpful to print
    print("Press CTRL-C to quit")



    # main loop. loop until finished
    while not isFinished[0]:
        action_on_seeing_object(robot)


# Tell cozmo to turn randomly and keep track of which way he turned
def randomlyTurn(robot):
    randBool = bool(random.getrandbits(1))
    if (randBool):
        robot.turn_in_place(degrees(90)).wait_for_completed()
        lastTurn[0] = 0
    else:
        robot.turn_in_place(degrees(-90)).wait_for_completed()
        lastTurn[0] = 1

# randomly say something from the global list of sayings
def randomlySaySomething(robot):

    randomInt = random.randint(0,len(sayings)-1)
    #print(sayings[randomInt])
    robot.say_text(sayings[randomInt]).wait_for_completed()


# main loop execution
def action_on_seeing_object(robot: cozmo.robot.Robot):

        # if it sees a hex 2, do your end game celebration
        if isHex2[0]:
            isDoingSomething[0] = True
            wall = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.CustomObject, timeout=1)
            if wall:
                robot.go_to_pose(wall[0].pose, relative_to_robot=False, in_parallel=False, num_retries=0).wait_for_completed()
                robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()
                robot.set_lift_height(1.0).wait_for_completed()
                robot.set_lift_height(0.0).wait_for_completed()
                robot.drive_straight(distance_inches(-1), speed_mmps(30)).wait_for_completed()
                play_animations(robot, victory_reactions)
                robot.say_text("I made it").wait_for_completed()
                # deletes the fake walls from cozmo's nav map. he will think there are walls in some cases and avoid invisible walls as if it could see them
                robot.world.delete_all_custom_objects()

                # robot.turn_in_place(degrees(-90)).wait_for_completed()

                # robot.drive_straight(distance_inches(2), speed_mmps(25)).wait_for_completed()
                # robot.turn_in_place(degrees(-180)).wait_for_completed()
                # robot.say_text("It's gotta be around here somewhere").wait_for_completed()
                # robot.drive_straight(distance_inches(8), speed_mmps(35)).wait_for_completed()
                # robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceWinSession, ignore_body_track=True).wait_for_completed()
                default_position(robot)
                isFinished[0] = True


        elif isHex5[0] or isCircle5[0] or isDiamond5[0] or isTriangle5[0] or isDiamond3[0]:
            isDoingSomething[0] = True
            wall = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.CustomObject, timeout=1)
            if wall:
                robot.go_to_pose(wall[0].pose, relative_to_robot=False, in_parallel=False, num_retries=0).wait_for_completed()
                robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()
                robot.set_lift_height(1.0).wait_for_completed()
                robot.set_lift_height(0.0).wait_for_completed()
                play_animations(robot, frustation_reactions)
                robot.drive_straight(distance_inches(-1), speed_mmps(30)).wait_for_completed()
                # deletes the fake walls from cozmo's nav map. he will think there are walls in some cases and avoid invisible walls as if it could see them
                robot.world.delete_all_custom_objects()
                randomlySaySomething(robot)
                default_position(robot)
                randomlyTurn(robot)


        # if it cant see any of the symbols and is set to doing something
        if not isTriangle5[0] and not isCircle5[0] and not isHex5[0] and not isDiamond5[0] and not isHex2[0] and isDoingSomething[0]:
            isDoingSomething[0] = False
            time1[0] = time.time()
            for i in range(0,len(timeTrigger)):
                timeTrigger[i] = False

        # if it cant see any of the symbols and is not doing something
        if not isTriangle5[0] and not isCircle5[0] and not isHex5[0] and not isDiamond5[0] and not isHex2[0] and not isDoingSomething[0]:
            newTime = time.time() - time1[0]
            # print(newTime)

            # if cozmo has gone some amount of time without seeing a marker
            # triggered at 5 seconds of waiting. resets time and starts counting again if it does not see a shymbol in its new view
            if newTime >= 5:
                # make this go forward in increments somewhat at random.
                isDoingSomething[0] = True
                play_animations(robot, thinking_reactions)
                robot.drive_straight(distance_inches(-1), speed_mmps(30)).wait_for_completed()

                robot.drive_straight(distance_inches(2.5), speed_mmps(30)).wait_for_completed()

                if lastTurn[0] == 0:
                    robot.turn_in_place(degrees(90)).wait_for_completed()
                elif lastTurn[0] == 1:
                    robot.turn_in_place(degrees(-90)).wait_for_completed()
                else:
                    randomlyTurn(robot)
            # triggered at 2 seconds
            elif newTime >= 2 and not timeTrigger[2]:
                timeTrigger[2] = True
                robot.turn_in_place(degrees(10)).wait_for_completed()
                robot.drive_straight(distance_inches(-1), speed_mmps(30)).wait_for_completed()
                # robot.turn_in_place(degrees(-2)).wait_for_completed()
            # triggered at 4 seconds
            elif newTime >= 4 and not timeTrigger[4]:
                timeTrigger[4] = True
                robot.turn_in_place(degrees(-10)).wait_for_completed()
                # robot.turn_in_place(degrees(2)).wait_for_completed()



cozmo.run_program(mainProgram, use_3d_viewer=True, use_viewer=True)
