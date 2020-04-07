#!/bin/bash    

export SCRAM_ARCH="slc7_amd64_gcc700"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`

echo "--------------------   --------------------   --------------------"
mkdir /cms/xaastorage/PicoTrees/$4/April2020v6/$1
mkdir /cms/xaastorage/NanoToolOutput/SKIM_$1
FILES=$2*.root
for f in $FILES
do
    filename=$(basename -- "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo $filename
    echo "------------------> Pre-Processing $f"

    python preprocess.py $f /cms/xaastorage/NanoToolOutput/SKIM_$1 $4 $5 $6 # input output year run triglist json
    echo "------------------> Processing $f"
    python treemaker.py $filename /cms/xaastorage/NanoToolOutput/SKIM_$1/$filename"_Skim.root" $7 /cms/xaastorage/PicoTrees/$4/April2020v6/$1 $5 $4
done
cd /cms/xaastorage/PicoTrees/$4/April2020v6/$1
hadd -f $1.root *root	
