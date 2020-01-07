#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

chmod a+x "array2csv.sh"

var='"File"; "Codec"; "Sample format"; "Sample rate"
"track 1.m4a"; "aac"; "fltp"; "44100"
"track 2.mp3"; "mp3"; "fltp"; "48000"
'

arr1=("File"        "Codec" "Sample format" "Sample rate" 
      "track 1.m4a" "aac"   "fltp"          "44100"
      "track 2.mp3" "mp3"   "fltp"          "48000")

if cp "array2csv.sh" "/usr/local/bin/array2csv"
then
    if . array2csv -a arr1[@] -n 4 -q -s "; " -o /tmp/test.csv \
        && diff /tmp/test.csv <(printf "%s" "$var")
    then
        printf "%s\n" "Successfully installed '/usr/local/bin/array2csv'"
    else
        printf "%s\n" "Error trying to run test"
    fi
else
    printf "%s\n" "Failure" \
           "Error copying file, try running install script as sudo"
    sleep 
    exit 1
fi

sleep 2
