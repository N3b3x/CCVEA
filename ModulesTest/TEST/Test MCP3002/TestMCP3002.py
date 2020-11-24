'''
Datasheet: http://www.farnell.com/datasheets/1599363.pdf
One of the things mentioned here is that the input must have low impedance or have a buffering
and Filtering circuit in order to decrease the impedance. However, due to what I am making being
powered by a battery, I don't want to just waste power thru heat by the resistors just to read the
voltage continuously and thus I will be using quite high resistors for the voltage divider that comes
before channel 0. However, due to constraints in the box and equipments, i didn't want to add
a buffering and Filtering Stage. Therefore, in order to achieve correct conversions of the voltage
I will reduce the SPI frequency in order to give the input capacitance inside the MCP3002
more time to charge. High frequencies cause incorrect readings and gets worse as voltage goes down.
Thus, a low frequency will be used to give accurate readings of the voltage.
'''
import time
import spidev

spi_ch = 1   # I'm using channel 1 (CE1) for the MCP3002 since CE0 is taken by the nRF24L01+

# Enable SPI
spi = spidev.SpiDev(0, spi_ch)
#spi.max_speed_hz = 1200000 # 1.2 MHz
spi.max_speed_hz = 100000 #10 kHz

def read_adc(adc_ch, vref = 3.3):

    # Make sure ADC channel is 0 or 1
    if adc_ch != 0:
        adc_ch = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + adc_ch) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 1024

    return voltage

# Report the channel 0 and channel 1 voltages to the terminal
try:
    while True:
        adc_0 = read_adc(0)
        adc_1 = read_adc(1)
        print("Ch 0:", round(adc_0, 2), "V Ch 1:", round(adc_1, 2), "V")
        time.sleep(0.2)

finally:
    GPIO.cleanup()