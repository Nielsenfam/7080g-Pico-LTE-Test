# Internet of Things (IoT) Sky Quality Meter
Micro Python Code for RPi Pico Waveshare 7080g LTE board
with TLS2591 Sensor data upload to Thingspeak

# Hardware Bill of Materials:
1.  [Waveshare SIM7080G Cat-M/NBIoT Module](https://www.waveshare.com/pico-sim7080g-cat-m-nb-iot.htm)
1.  [Raspberry Pi Pico](https://www.adafruit.com/product/5525)
1.  [SIM card](https://store.simbase.com/)
1.  [Headers](https://www.adafruit.com/product/5582)
1.  [STEMMA QT Cable](https://www.adafruit.com/product/4210)
1.  [PiCowbell Proto for Pico](https://www.adafruit.com/product/5200)
1.  [TSL2591 Light Sensor Module](https://www.adafruit.com/product/1980)

# Software:
Micropython
Waveshare SIM7080G python libraries
Thingspeak communications using MQTT

# Description:
This program reads data from a TSL2591 Light Sensor and
then uploads it to Thingspeak using MQTT protocol
then goes to sleep for a period of time and wakes up and repeats the process

# Setup:
Copy tsconfig-template.py to tsconfig.py and edit to include Thingspeak secrets and other configurations
