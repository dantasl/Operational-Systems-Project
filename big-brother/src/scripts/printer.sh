#!/bin/bash
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

ls | awk ' BEGIN { ORS = ""; print "["; } { print "\/\@"$0"\/\@"; } END { print "]"; }' | sed "s^\"^\\\\\"^g;s^\/\@\/\@^\", \"^g;s^\/\@^\"^g"