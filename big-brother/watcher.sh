#!/bin/bash
#
# Script Name: watcher.sh
#
# Author: Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
# Date: August 20th - 2018

TIMER=5
if [ $# -ne 0 ]; then
    TIMER=$1
fi

printf "Big Brother is now watching your processes every $TIMER seconds.\n\n"

countAll()
{
    printf "\nNumber of processes currently running: "
    ps aux | wc -l
}

countByUser()
{
    printf "\nNumber of processes running by user: \n"
    ps -eo user=|sort|uniq -c
}

finish()
{
    printf "\nBig Brother now rests at peace.\n"
    kill -s SIGTERM $!
    exit 0
}

trap finish SIGINT SIGTERM

while [ 1 ]; do
    printf "\n==============================================="
    countAll
    countByUser
    printf "===============================================\n"
    sleep $TIMER
done