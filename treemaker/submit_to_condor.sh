#!/bin/bash
cmsenv
source /condor/HTCondor/current/condor.sh
python condor_helper.py $1 $USER $PWD
