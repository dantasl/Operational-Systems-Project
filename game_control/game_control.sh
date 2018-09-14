#!/bin/bash
GPIO_DIR=/sys/class/gpio/gpio
EXPORT_DIR=/sys/class/gpio/export
BUTTON=7

ADC_FOLDER=/sys/bus/iio/devices/iio:device0
#Values of analog input in [0, 4095]
FOTORESISTOR=$ADC_FOLDER/in_voltage0_raw
POTENCIOMETRO=$ADC_FOLDER/in_voltage1_raw

init () {
	echo cape-bone-iio > /sys/devices/bone_capemgr.9/slots
}

initButton()
{
	echo $BUTTON > $EXPORT_DIR
	echo in > $GPIO_DIR$BUTTON/direction
}