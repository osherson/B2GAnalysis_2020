#!/bin/bash
start=`date +%s`
RED='\033[0;31m'
NC='\033[0m'
echo -e "${RED}__START__${NC}"
echo -e "${RED}> Using "$1" as payload${NC}"
cp $1 TEMPPAYLOAD.py
echo -e "${RED}> Setting up... ${NC}"
python Setup.py
echo -e "${RED}> Getting regions for fits... ${NC}"
python GetFitRegions.py
echo -e "${RED}> Doing the ABCD fits... ${NC}"
python GetFits.py
echo -e "${RED}> Building shape templates... ${NC}"
python BuildShapes.py
echo -e "${RED}> Building signal models... ${NC}"
python ProcessSignals.py
echo -e "${RED}> Building combine card... ${NC}"
python MakeCards.py
echo -e "${RED}> Running combine steps... ${NC}"
python CombineStep1.py
#python CombineGetBOF.py
#python CombineStep2.py

echo -e "${RED}> Cleaning up... ${NC}"
python Cleanup.py
end=`date +%s`
echo -e "${RED}> total time = $((end-start)) seconds${NC}"
echo -e "${RED}__END__${NC}"
