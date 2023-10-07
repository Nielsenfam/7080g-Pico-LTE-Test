"""
Raspberry Pi Pico (MicroPython)
SIM7080G Cat-M/NBIoT Module
"""
import machine
import utime
import random

import tsconfig

# Sim APM
sim_apn = tsconfig.sim_apn
# Thingspeak
ts_url = tsconfig.ts_url
ts_port = tsconfig.ts_port
ts_channel = tsconfig.ts_channel
ts_clientid = tsconfig.ts_clientid
ts_username = tsconfig.ts_username
ts_password = tsconfig.ts_password

# Setup
sample_min = tsconfig.sample_min

global mqtt_msg
global mqtt_msg_len

# using pin defined
pwr_en = 14  # pin to control the power of the module

# uart setting
uart_port = 0
uart_baud = 115200
Pico_SIM7080G = machine.UART(uart_port, uart_baud)

# LED indicator on Raspberry Pi Pico
led_pin = 25  # onboard led
led_onboard = machine.Pin(led_pin, machine.Pin.OUT)

def led_blink():
    for i in range(1, 4):
        led_onboard.value(1)
        utime.sleep(1)
        led_onboard.value(0)
        utime.sleep(1)
    led_onboard.value(0)

# power on/off the module
def module_power():
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
    pwr_key.value(1)
    utime.sleep(2)
    pwr_key.value(0)

def module_power_on():
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
    pwr_key.value(0)

def module_power_off():
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
    pwr_key.value(1)



# Send AT command
def send_at(cmd, back, timeout=1000):
    rec_buff = b''
    Pico_SIM7080G.write((cmd + '\r\n').encode())
    prvmills = utime.ticks_ms()
    while (utime.ticks_ms() - prvmills) < timeout:
        if Pico_SIM7080G.any():
            rec_buff = b"".join([rec_buff, Pico_SIM7080G.read(1)])
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(cmd + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())
            return 1
    else:
        print(cmd + ' no response')

# Send AT command and return response information
def send_at_wait_resp(cmd, back, timeout=2000):
    rec_buff = b''
    # Pico_SIM7080G.write((cmd + '\r\n').encode())
    Pico_SIM7080G.write((cmd + '\r').encode())
    prvmills = utime.ticks_ms()
    while (utime.ticks_ms() - prvmills) < timeout:
        if Pico_SIM7080G.any():
            rec_buff = b"".join([rec_buff, Pico_SIM7080G.read(1)])
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(cmd + ' back:\t' + rec_buff.decode())
        else:
            print(rec_buff.decode())
    else:
        print(cmd + ' no responce')
    print("Response information is: ", rec_buff)
    return rec_buff

# Module startup detection
def check_start():
    # simcom module uart may be fool,so it is better to send much times when it starts.
    utime.sleep(5)
    send_at("AT", "OK")
    utime.sleep(5)
    send_at("AT+CFUN=0", "OK")
    utime.sleep(5)
    send_at("AT", "OK")
    for i in range(1, 7):
        if send_at("AT", "OK",3000) == 1:
            print('------SIM7080G is ready------\r\n')
            break
        else:
            module_power()
            print('------SIM7080G is starting up, please wait------\r\n')
            Pico_SIM7080G = machine.UART(uart_port, 9600)
            utime.sleep(20)
            send_at("AT+CFUN=0", "OK")

def set_network():
    print("Setting up Network:\n")
    send_at("AT+CFUN=0", "OK")
    send_at("AT+CNCFG=0,1,\""+sim_apn+"\"","OK")
    send_at("AT+CNMP=38", "OK")  # Select LTE mode
    send_at("AT+CMNB=1", "OK")  # Select NB-IoT mode,if Cat-M，please set to 1
    send_at("AT+CFUN=1", "OK")
    utime.sleep(5)

# Check the network status
def check_network():
    if send_at("AT+CPIN?", "READY",2000) != 1:
        print("------Please check whether the sim card has been inserted!------\n")
    for i in range(1, 5):
        if send_at("AT+CGATT?", "1",2000):
            print('------SIM7080G is online------\r\n')
            break
        else:
            print('------SIM7080G is offline, please wait...------\r\n')
            utime.sleep(10)
            continue
    send_at("AT+CSQ", "OK")
    send_at("AT+CPSI?", "OK")
    send_at("AT+COPS?", "OK")
    send_at('AT+CNACT=0,1', 'OK')
    send_at('AT+CNACT?', 'OK')
    #time_str = send_at_wait_resp('AT+CCLK?', 'OK')
    #print( 'time =', time_str )

def mqtt_test():
    
    global mqtt_msg
    global mqtt_msg_len
    
    send_at('AT+SMCONF=\"URL\",\"' +ts_url+ '\",'+str(ts_port) ,'OK')
    send_at('AT+SMCONF=\"KEEPTIME\",600','OK')
    send_at('AT+SMCONF=\"CLIENTID\",\"'+ts_clientid+'\"','OK',2000)
    send_at('AT+SMCONF=\"USERNAME\",\"'+ts_username+'\"','OK',2000)
    send_at('AT+SMCONF=\"PASSWORD\",\"'+ts_password+'\"','OK',2000)
    utime.sleep(2)
    send_at('AT+SMCONN','OK',5000)
    send_at('AT+SMPUB=\"channels/'+str(ts_channel)+'/publish\",' + str(mqtt_msg_len) + ',1,1','OK',2000)
    Pico_SIM7080G.write(mqtt_msg.encode())
    utime.sleep(2);
    send_at('AT+SMDISC','OK',2000)

def input_test():
    global mqtt_msg
    global mqtt_msg_len
    
    print("---------------------------SIM7080G INPUT TEST---------------------------")
    while True:
        try:
            command_input = str(input('Please input a measurement,press Ctrl+C to exit:\000'))
            mqtt_msg = 'field1=' + command_input
            mqtt_msg_len = len(mqtt_msg)
            print ("Message length:", mqtt_msg_len, "\nMessage:", mqtt_msg)
            mqtt_test()
        except KeyboardInterrupt:
            print('\n------Exit Measurment Input Command Test!------\r\n')
            module_power()
            print("------The module is power off!------\n")
            break

def data_sim_test():
    global mqtt_msg
    global mqtt_msg_len
    
    datapt = random.randrange(2000)/100
    
    print( 'datapt =', str(datapt))
    mqtt_msg = 'field1=' + str(datapt)
    mqtt_msg_len = len(mqtt_msg)
    mqtt_test()

def sync_ntp_time():
    ret_str = b''
    send_at('AT+CNTPCID=0',"OK")
    send_at('AT+CNTP=\"time1.google.com\"',"OK")
    send_at('AT+CNTP',"OK")
    ret_str = send_at_wait_resp('AT+CCLK?',"OK")
    return ret_str

def at_test():
    print("---------------------------SIM7080G AT TEST---------------------------")
    while True:
        try:
            command_input = str(input('Please input the AT command,press Ctrl+C to exit:\000'))
            send_at(command_input, 'OK', 2000)
        except KeyboardInterrupt:
            print('\n------Exit AT Command Test!------\r\n')
            module_power()
            print("------The module is power off!------\n")
            break


# SIM7080G main program

led_blink()

while True:
    # attempt to take N readings per sample period
    for i in range(1, 3):
    
        module_power_on()
        check_start()
        set_network()
        check_network()
        # get date/time from ntp server:
        time_str = sync_ntp_time().decode('utf-8')
        print( "date/time from ntp:", time_str )
        
        # get simulated data
        data_sim_test()
    
    # sleep for mins
    module_power_off()
    utime.sleep(sample_min*60)

# input_test()
at_test()