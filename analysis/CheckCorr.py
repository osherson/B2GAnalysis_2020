from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")

DATA = outF.Get("presel_ABCD_data")
TTBAR = outF.Get("presel_ABCD_ttbar")

DATASUB = DATA.Clone("presel_ABCD_sub")
DATASUB.Add(TTBAR, -1.)

CutsD = []
CutsS = []
for i in [0.1, 0.25, 0.5, 0.75, 0.9]:
	CutsD.append(GetQuantileProfiles(DATA, i))
	CutsS.append(GetQuantileProfiles(DATASUB, i))
for i in CutsD:
	GoodPlotFormat(i, "thinline", ROOT.kRed, 1)
for i in CutsS:
	GoodPlotFormat(i, "thinline", ROOT.kRed, 1)

DATA.SetStats(0)
DATASUB.SetStats(0)

C = TCanvas()
C.Divide(2,1)
C.cd(1)
DATA.Draw("col")
for i in CutsD:
	i.Draw("histsame")
C.cd(2)
DATASUB.Draw("col")
for i in CutsS:
	i.Draw("histsame")


outF.Close()
