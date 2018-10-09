#!/bin/bash
#
# Script Name: init.sh
#
# Author: Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
# Author: Lucas Aléssio Anunciado Silva (lucas.alessio@live.com)
# Date: October 9th - 2018

# Section 0 - Constants declaration
#######################################################################

GPIO_DIR=/sys/class/gpio/gpio
EXPORT_DIR=/sys/class/gpio/export
ADC_FOLDER=/sys/bus/iio/devices/iio:device0
ADC_FILE=instructions.txt
BUTTON=7
PHOTORESISTOR=$ADC_FOLDER/in_voltage4_raw
POTENTIOMETER=$ADC_FOLDER/in_voltage3_raw

#######################################################################

# Section 1 - {}
#######################################################################

# Add comment
init()
{
    # Init the analog components
    echo cape-bone-iio > /sys/devices/bone_capemgr.9/slots
    # Init button
    echo $BUTTON > $EXPORT_DIR
    echo in > $GPIO_DIR$BUTTON/direction
}

init

printf "=====================================================\n"
printf "Initializing components... OK\n"
printf "BUTTON AT $BUTTON\nPHOTORESISTOR AT $PHOTORESISTOR\n"
printf "POTENTIOMETER AT $POTENTIOMETER\nSAVING INSTRUCTIONS AT $ADC_FILE\n"
printf "=====================================================\n"

#######################################################################

# Section 3 - {}
#######################################################################

# Add comment
checkPotentiometerChange()
{
    if cat $POTENTIOMETER ; then
	CHECK_CURRENT=`cat $POTENTIOMETER`
        DIFF=$(($CHECK_CURRENT-$POTCHANGE))
        if [ `echo $DIFF | tr -d -` -gt 200 ]; then
            if [ $CHECK_CURRENT -lt 2048 ]; then
                echo 'LEFT' >> $ADC_FILE
            else
                echo 'RIGHT' >> $ADC_FILE
            fi
        fi
        POTCHANGE=$CHECK_CURRENT
    fi
}

# Add comment
checkPhotoresistorChange()
{
    if cat $PHOTORESISTOR ; then
	    CURRENT_PHOTO=`cat $PHOTORESISTOR`
        if [ $CURRENT_PHOTO -lt 500 ]; then
            echo 'UP' >> $ADC_FILE
        fi
        PHOTOCHANGE=$CURRENT_PHOTO
    fi
}

# Add comment
checkButtonChange()
{
    if cat $GPIO_DIR$BUTTON/value ; then
	    CURRENT_BUTTON=`cat $GPIO_DIR$BUTTON/value`
        if [ $CURRENT_BUTTON -eq 1 ]; then
            echo 'DOWN' >> $ADC_FILE
        fi
        BUTTONCHANGE=$CURRENT_BUTTON
    fi
}

#######################################################################

# Section 2 - The main loop, where the magic happens
#######################################################################

POTCHANGE=0
PHOTOCHANGE=0
BUTTONCHANGE=0

while [ 1 ]; do
    echo '' > $ADC_FILE
    checkButtonChange || true
    checkPhotoresistorChange || true
    checkPotentiometerChange || true
    sleep 1
done

#######################################################################