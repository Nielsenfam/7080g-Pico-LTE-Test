# 7080g-Pico-LTE-Test
 Micro Python Test Code for RPi Pico Waveshare 7080g LTE board
with TLS2591 Sensor data upload to Thingspeak

Raspberry Pi Pico (MicroPython)
SIM7080G Cat-M/NBIoT Module
Thingspeak communications
TSL2591 Light Sensor

This program reads data from a TSL2591 Light Sensor and
then uploads it to Thingspeak using MQTT protocol
then goes to sleep for a period of time and wakes up and repeats the process

Setup:

Copy tsconfig-template.py to tsconfig.py and edit to include Thingspeak secrets and other configurations