#!/bin/bash
#
# Script Name: semaphore.sh
#
# Author: Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
# Author: Lucas Aléssio Anunciado Silva (lucas.alessio@live.com)
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

# Section 1 - Bootstraping GPIO and providing helper to LED's output
#######################################################################

# Export the button and set direction to "in"
initButton()
{
	echo $1 > $EXPORT_DIR
	echo in > $GPIO_DIR$1/direction
}

# Export the pin and set LED output to 0
initLed()
{
	echo $1 > $EXPORT_DIR
	echo out > $GPIO_DIR$1/direction
	echo 0 > $GPIO_DIR$1/value
}

# Change the state of a given LED - e.g. Put RED_LED to 1 (turn on)
updateLed()
{
	echo $2 > $GPIO_DIR$1/value
}

initLed $LED_RED
initLed $LED_YELLOW
initLed $LED_GREEN
initButton $PANIC_BUTTON

printf "====================================================="
printf "RED TO $LED_RED\nYELLOW TO $LED_YELLOW\nGREEN TO $LED_GREEN\nBUTTON TO $PANIC_BUTTON\n"
printf "====================================================="

#######################################################################

# Section 2 - The main loop, where the magic happens
#######################################################################

printf "Big Brother is now watching your processes every 2 seconds.\n\n"

while [ 1 ]; do
    printf "\n===============================================\n"
    PERCENTAGE=$(checkResourceStatus)
    printf "Maximum memory usage goes by $PERCENTAGE."
    updateState $PERCENTAGE
    printf "\n===============================================\n"
    sleep 2
done

# Here we will check how much % the resource is being used
checkResourceStatus()
{
    PERCENTAGE=`ps -eo %mem --no-headers --sort=-%mem | head -1`
    echo $PERCENTAGE
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

#######################################################################

# Section 3 - Handling the panic mode
#######################################################################

# Here the LEDs go berserk and we must check if user pressed the button
initiatePanic()
{
    LOOP_KILL=1
    while [ $LOOP_KILL -eq 1 ]; do
        # Leds are now blinking
        blinkLeds
        # Check if button is being pressed
        PRESSED=$(checkPanicButtonPressed)
        if [ $PRESSED -eq 1 ]; then
            # Kill process
            PID=$(getTopMemoryUsagePID)
            kill -9 $PID
            # LEDs are turned off for 3 seconds
            updateLed $LED_GREEN 0
            updateLed $LED_RED 0
            updateLed $LED_YELLOW 0
            sleep 3
            # Breaks loop and goes back to previous logic
            LOOP_KILL=0
        fi
    done
}

# Here the LEDs will start to blink
blinkLeds()
{
    updateLed $LED_GREEN 1
    updateLed $LED_RED 1
    updateLed $LED_YELLOW 1
    sleep 0.5
    updateLed $LED_GREEN 0
    updateLed $LED_RED 0
    updateLed $LED_YELLOW 0
    sleep 0.5
}

# Here we will check if the panic button was pressed
checkPanicButtonPressed()
{
    PRESSED=`cat $GPIO_DIR$PANIC_BUTTON/value`
    echo $PRESSED
}

# Here we can check which process is consuming more memory and get its PID
getTopMemoryUsagePID()
{
    BAD_PID=`ps -eo pid --no-headers --sort=-%mem | head -1`
    echo $BAD_PID
}

#######################################################################

# Section 4 - Handling SIGTERM and SIGINT
#######################################################################

# Function that treats the ending of this script
finish()
{
    printf "\nBig Brother now rests at peace.\n"
    kill -s SIGTERM $!
    exit 0
}

trap finish SIGINT SIGTERM

#######################################################################