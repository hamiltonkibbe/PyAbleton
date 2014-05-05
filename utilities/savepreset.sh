#!/bin/bash
# Simple bash script to zip up an xml preset file and save with ableton extension

FILE="$1"
ZIPPED="${FILE%.xml}.gz"
NAME="${FILE%.xml}"

cp "$FILE" "$NAME"
gzip "$NAME"
mv "$ZIPPED" "${ZIPPED%.gz}.adv"


