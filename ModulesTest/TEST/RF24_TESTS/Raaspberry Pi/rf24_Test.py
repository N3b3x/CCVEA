#!/usr/bin/env python3

from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
send_payload = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ789012'

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md
# Radio CE Pin, CSN Pin, SPI Speed
# CE Pin uses GPIO number with BCM and SPIDEV drivers, other platforms use their own pin numbering
# CS Pin addresses the SPI bus number at /dev/spidev<a>.<b>
# ie: RF24 radio(<ce_pin>, <a>*10+<b>); spidev1.0 is 10, spidev1.1 is 11 etc..
# Generic:
radio = RF24(22,0);

radio.begin()
radio.setAutoAck(False)
radio.setChannel(2)
radio.enableDynamicPayloads()
radio.setRetries(15, 15)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.setPALevel(RF24_PA_MIN)
radio.stopListening()

radio.printDetails()


while(1):
    radio.write(b'Your Button State is HIGH\n')
