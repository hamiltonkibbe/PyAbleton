#!/bin/bash
# Simple bash script to unzip a preset file and save it as <filename>.xml
FILE="$1"
GZ="${FILE%.adv}.gz"
UNZIPPED="${GZ%.gz}"

#
cp "$FILE" "$GZ"
gunzip "$GZ"

mv "$UNZIPPED" "${UNZIPPED}.xml"
