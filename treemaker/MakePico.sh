#!/bin/bash    
echo "--------------------   --------------------   --------------------"
mkdir PICO_$1
cd $3
mkdir SKIM_$1
cd -
FILES=$2*.root
for f in $FILES
do
    filename=$(basename -- "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo $filename
    echo "------------------> Pre-Processing $f"

    python preprocess.py $f $3/SKIM_$1 $4 $5 $6 # input output year run triglist json
    echo "------------------> Processing $f"
    python treemaker.py $filename $3/SKIM_$1/$filename"_Skim.root" $7 PICO_$1 $5 $4
done
cd PICO_$1
hadd -f $1.root *root
mv $1.root ..
cd ..
rm -rf PICO_$1