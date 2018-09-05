#!/bin/bash

GPIO_DIR=/sys/class/gpio/gpio
LED_RED=50
LED_YELLOW=2
LED_GREEN=112
PANIC_BUTTON=115

printf "Big Brother is now watching your processes every 2 seconds.\n\n"

updateLed()
{
	echo $2 > $GPIO_DIR$1/value
	echo $1 to $2
}

finish()
{
    printf "\nBig Brother now rests at peace.\n"
    kill -s SIGTERM $!
    exit 0
}

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
        printf "Fuck!"
    fi
}

trap finish SIGINT SIGTERM

while [ 1 ]; do
    printf "\n===============================================\n"
    PERCENTAGE=$(checkResourceStatus)
    printf "Maximum memory usage goes by $PERCENTAGE."
    updateState $PERCENTAGE
    printf "\n===============================================\n"
    sleep 2
done