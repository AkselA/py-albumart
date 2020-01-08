#!/bin/bash

co="albumart.py"
lc="/usr/local/bin/"

ex="${lc}${co%.*}"

cd "$( dirname "${BASH_SOURCE[0]}" )"

chmod a+x "$co"

if cp "$co" "$ex"
then
    printf "%s\n" "Successfully installed '$ex'"
    exit 0
else
    printf "%s\n" "Something seems to have gone wrong while trying to install '$ex'" \
                  "Does '$co' exist in the same directory as this install script?" \
                  "Is '$lc' a valid directory?"
                  "Doe you have the required permission (maybe try 'sudo')?"
    exit 1
fi

sleep 2
