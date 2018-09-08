#!/bin/bash
#
# ATTENTION! RUN THIS SCRIPT ONLY INSIDE ITS ORIGINAL DIRECTORY
#
# Script Name: printer.sh
#
# Author: Lucas Gomes Dantas (dantaslucas@ufrn.edu.br)
# Date: August 20th - 2018

finish()
{
    printf "\nMy time to serve has now reached its end.\n"
    kill -s SIGTERM $!
    exit 0
}

if [ $# -ne 1  ]; then
    finish
fi

PARENT_DIR=`cd ../../results && pwd`
pstree -p -A $1 > $PARENT_DIR/$1.txt
printf "\nCheckout for a file named $1.txt inside the directory results. There lies your tree!\n"