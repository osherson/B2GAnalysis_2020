from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")

DATA = outF.Get("presel_ABCD_data")
DATA.SetTitle("preselection with no further cuts")
TTBAR = outF.Get("presel_ABCD_ttbar")

DATASUB = DATA.Clone("presel_ABCD_sub")
DATASUB.Add(TTBAR, -1.)
DATASUB.SetTitle("preselection with t#bar{t} subtracted")

D = []
S = []
for i in [0.5, 0.75, 0.9, 0.95]:
	HD = GetQuantileProfiles(DATA, i)
	D.append(HD)
	HS = GetQuantileProfiles(DATASUB, i)
	S.append(HS)
for i in D:
	GoodPlotFormat(i, "thinline", ROOT.kRed, 1)
for i in S:
	GoodPlotFormat(i, "thinline", ROOT.kRed, 1)

DATA.SetStats(0)
DATASUB.SetStats(0)

C = ROOT.TCanvas("C", "", 1000, 450)
C.Divide(2,1)
C.cd(1)
ROOT.gPad.SetLeftMargin(0.25)
DATA.Draw("col")
for i in D:
	i.Draw("histsame")
C.cd(2)
ROOT.gPad.SetLeftMargin(0.25)
DATASUB.Draw("col")
for i in S:
	i.Draw("histsame")
C.Print("../results/"+NAME+"/CorrCheck.root")
C.Print("../results/"+NAME+"/CorrCheck.png")

outF.Close()
