#!/usr/bin/env bash

FILES="./Scan/*.pdf"
TEMP="./Splitted"
OUTPUT_DIR="./Output/"

mkdir -p $TEMP
mkdir -p $OUTPUT_DIR

for f in $FILES
do
    echo "Processing $f"
    python splitpdf.py $f $TEMP
done

echo "Merging files..."

python mergepdfs.py $TEMP $OUTPUT_DIR/Scan.pdf -r 90

rm -r $TEMP

echo "Done!"