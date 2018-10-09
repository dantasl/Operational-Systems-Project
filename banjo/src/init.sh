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
	printf "====================================================="
    printf "Initializing components... OK"
    printf "BUTTON AT $BUTTON\nPHOTORESISTOR AT $PHOTORESISTOR\n"
    printf "POTENTIOMETER AT $POTENTIOMETER\nSAVING INSTRUCTIONS AT $ADC_FILE\n"
    printf "====================================================="
}

#######################################################################

# Section 2 - The main loop, where the magic happens
#######################################################################

POTCHANGE=0

while [ 1 ]; do
    echo '' > $ADC_FILE
    if [ `cat $PHOTORESISTOR` -lt 500 ]; then
        echo 'UP' > $ADC_FILE
    fi

    if [ `cat $GPIO_DIR$BUTTON/value` -eq 1 ]; then
        echo 'DOWN' >> $ADC_FILE
    fi

    POTCHANGE=$(check_pot_change $POTCHANGE)
done

#######################################################################

# Section 3 - {}
#######################################################################

# Add comment
check_pot_change()
{
    CHECK_CURRENT=`cat $POTENTIOMETER`
    DIFF=$(($CHECK_CURRENT-$1))
    if [ `echo $DIFF | tr -d -` -gt 200 ]; then
        if [ $CHECK_CURRENT -lt 2048 ]; then
            echo 'LEFT' >> $ADC_FILE
        else
            echo 'RIGHT' >> $ADC_FILE
        fi
    fi
    echo $CHECK_CURRENT
}

#######################################################################