#!/bin/bash
#
# Script Name: semaphore.sh
#
# Author: Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
# Author: Lucas Aléssio
# Date: September 4th - 2018

# Section 0 - Constants declaration
#######################################################################

GPIO_DIR=/sys/class/gpio/gpio
EXPORT_DIR=/sys/class/gpio/export
LED_RED=50
LED_YELLOW=2
LED_GREEN=112
PANIC_BUTTON=115

#######################################################################

# Section 1 - First configuration that the GPIO needs
#######################################################################

initButton()
{
	echo $1 > $EXPORT_DIR
	echo $1 exported

	echo in > $GPIO_DIR$1/direction
	cat $GPIO_DIR$1/direction
}

initLed()
{
	echo $1 > $EXPORT_DIR
	echo $1 exported

	echo out > $GPIO_DIR$1/direction
	cat $GPIO_DIR$1/direction

	echo 0 > $GPIO_DIR$1/value
	cat $GPIO_DIR$1/value
}

initLed $LED_RED
initLed $LED_YELLOW
initLed $LED_GREEN
initButton $PANIC_BUTTON

#######################################################################

# Function that treats the ending of this script
finish()
{
    printf "\nBig Brother now rests at peace.\n"
    kill -s SIGTERM $!
    exit 0
}

# Change the state of a given LED - e.g. Put RED_LED to 1 (turn on)
updateLed()
{
	echo $2 > $GPIO_DIR$1/value
	echo $1 to $2
}

# Here we can check which process is consuming more memory and get its PID
getTopMemoryUsagePID()
{
    BAD_PID=`ps -eo pid --no-headers --sort=-%mem | head -1`
    echo $BAD_PID
}

# Here we will check how much % the resource is being used
checkResourceStatus()
{
    PERCENTAGE=`ps -eo %mem --no-headers --sort=-%mem | head -1`
    echo $PERCENTAGE
}

# Here we will check if the panic button was pressed
checkPanicButtonPressed()
{
    PRESSED=`cat $GPIO_DIR$PANIC_BUTTON/value`
    echo $PRESSED
}

# Updates how the system will behave depending on the percentage
updateState()
{
    if [ "${1%%.*}" -lt 25 ]; then
        updateLed $LED_GREEN 1
        updateLed $LED_RED 0
        updateLed $LED_YELLOW 0
    elif [ "${1%%.*}" -gt 25 ] && [ "${1%%.*}" -lt 50 ];then
        updateLed $LED_GREEN 0
        updateLed $LED_RED 0
        updateLed $LED_YELLOW 1
    elif [ "${1%%.*}" -gt 50 ] && [ "${1%%.*}" -lt 75 ]; then
        updateLed $LED_GREEN 0
        updateLed $LED_RED 1
        updateLed $LED_YELLOW 0
    else
        initiatePanic
    fi
}

# Here the LEDs go berserk and we must check if user pressed the button
initiatePanic()
{
    LOOP_KILL=1
    while [ $LOOP_KILL -eq 1 ]; do
        # Leds are now blinking
        updateLed $LED_GREEN 1
        updateLed $LED_RED 1
        updateLed $LED_YELLOW 1
        sleep 0.5
        updateLed $LED_GREEN 0
        updateLed $LED_RED 0
        updateLed $LED_YELLOW 0
        sleep 0.5

        # Check if button is being pressed
        PRESSED=$(checkPanicButtonPressed)
        if [ $PRESSED -eq 1 ]; then
            # Kill process
            kill SIGTERM getTopMemoryUsagePID
            # LEDs are turnd off for 3 seconds
            updateLed $LED_GREEN 0
            updateLed $LED_RED 0
            updateLed $LED_YELLOW 0
            sleep 3
            # Breaks loop and goes back to previous logic
            LOOP_KILL=0
        fi
    done
}

trap finish SIGINT SIGTERM

printf "Big Brother is now watching your processes every 2 seconds.\n\n"

while [ 1 ]; do
    printf "\n===============================================\n"
    PERCENTAGE=$(checkResourceStatus)
    printf "Maximum memory usage goes by $PERCENTAGE."
    updateState $PERCENTAGE
    printf "\n===============================================\n"
    sleep 2
done