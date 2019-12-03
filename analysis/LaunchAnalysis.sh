#!/bin/bash
start=`date +%s`
RED='\033[0;31m'
NC='\033[0m'
echo -e "${RED}==========================================${NC}"
echo -e "${RED}                   START                  ${NC}"



echo -e " ${RED}> Using "$1" as payload${NC}"
cp $1 TEMPPAYLOAD.py

echo -e " ${RED}> Setting things up... ${NC}"
python AnalysisSetup.py

echo -e " ${RED}> Filling regions ABC&D... ${NC}"
python GetRegions.py

echo -e " ${RED}> Checking correlations... ${NC}"
python CheckCorr.py

echo -e " ${RED}> Fitting those regions... ${NC}"
python GetFits.py

echo -e " ${RED}> Using those fits for estimations... ${NC}"
python GetEst.py

echo -e " ${RED}> Filling the signal histograms, computing systematics... ${NC}"
python DoSig.py

echo -e " ${RED}> Using those estimations to do physics in 1D! ${NC}"
python UseEst.py
echo -e " ${RED}> Using those estimations to do physics in 2D! ${NC}"
python UseEst2D.py

echo -e " ${RED}> Making the data card! ${NC}"
python MakeCards.py

echo -e " ${RED}> Using combine to run fits! ${NC}"
python DoCombineSteps.py
python DoCombineSteps2.py

echo -e " ${RED}> Cleaning up... ${NC}"
python Cleanup.py
rm TEMPPAY*

end=`date +%s`
echo -e "${RED}                    time = $((end-start)) seconds${NC}"
echo -e "${RED}                    END                   ${NC}"
echo -e "${RED}==========================================${NC}"