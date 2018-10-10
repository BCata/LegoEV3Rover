#!/usr/bin/env python3

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from ev3dev2._platform.ev3 import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, UltrasonicSensor
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_D, SpeedPercent

SPEED = 35
TIME = 0.6

s = Sound()
leds = Leds()
cs = ColorSensor()
us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
ts_left = TouchSensor(INPUT_1)
ts_right = TouchSensor(INPUT_4)

def move_both_for_seconds(percent, seconds):
    MoveTank(OUTPUT_A, OUTPUT_D).on_for_seconds(SpeedPercent(percent),
                                                SpeedPercent(percent),
                                                seconds,
                                                brake=False,
                                                block=True)

def move_both(percent):
    MoveTank(OUTPUT_A, OUTPUT_D).on(SpeedPercent(percent),
                                    SpeedPercent(percent))

def turn_left(percent, seconds):
    LargeMotor(OUTPUT_D).on_for_seconds(SpeedPercent(percent),
                                        seconds, brake=False,
                                        block=True)

def turn_right(percent, seconds):
    LargeMotor(OUTPUT_A).on_for_seconds(SpeedPercent(percent),
                                        seconds, brake=False,
                                        block=True)

def detect_line():
    return cs.color == 1

def detect_collision():
    return ts_left.is_pressed or ts_right.is_pressed

def detect_proximity():
    return us.value()/10 < 25

def collision_protocol():
    leds.set_color("LEFT", "RED") 
    leds.set_color("RIGHT", "RED")
    move_both_for_seconds(-SPEED, TIME)
    turn_left(-SPEED, TIME)

while True:
    if detect_line() or detect_collision() or detect_proximity():
        collision_protocol()
        leds.set_color("LEFT", "GREEN")
        leds.set_color("RIGHT", "GREEN") 

    move_both(SPEED)
