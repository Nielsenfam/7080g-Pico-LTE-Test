# 7080g-Pico-LTE-Test
 Micro Python Test Code for RPi Pico Waveshare 7080g LTE board
with Thingspeak

Raspberry Pi Pico (MicroPython)
SIM7080G Cat-M/NBIoT Module
Thingspeak communications

This program generates a random number between 0 and 20 (a psudo measurement)
then uploads it to Thingspeak using MQTT protocol
then goes to sleep for a period of time and wakes up and repeats the process

Setup:

Copy tsconfig-template.py to tsconfig.py and edit to include Thingspeak secrets and other configurations