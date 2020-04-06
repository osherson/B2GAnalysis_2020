#!/bin/bash
cluster=$1
process=$2
cd ../treemaker
export SCRAM_ARCH="slc7_amd64_gcc900"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh
cmsenv
source MakePico.sh #NAME# #INPUT# /cms/xaastorage/NanoToolOutput #YEAR# #RUN# triglist.txt #WEIGHT# >& condor_logfiles_#NAME#_$1_$2.log
cd -
