import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

print "RUNNING COMBINE CARDS: "
for Sigs in SIG:
	for VAR in EstVars:
		if not VAR[3]: continue
		cardname = VAR[0]+"_"+Sigs[3]
		os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M GoodnessOfFit --algo=saturated")
		KS_Fs = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH120.root")
		KS_Ts = KS_Fs.Get("limit")
		KS_Vs = []
		for i in range(0,KS_Ts.GetEntries()):
			KS_Ts.GetEntry(i)
			KS_Vs.append(KS_Ts.limit)
		os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M GoodnessOfFit --algo=saturated -t "+str(NTOYS))
		KS_F = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH120.123456.root")	
		KS_T = KS_F.Get("limit")
		KS_V = []
		for i in range(0,KS_T.GetEntries()):
			KS_T.GetEntry(i)
			KS_V.append(KS_T.limit)
		minKS = min(min(KS_V),min(KS_Vs))
		maxKS = max(max(KS_V),max(KS_Vs))
		rangeKS = maxKS - minKS
		KS_plot = ROOT.TH1F(cardname+"_KS_plot", ";Goodness Of Fit Statistic (Saturated);toys", 50, minKS-(rangeKS/10), maxKS+(rangeKS/10))
		KS_plot.SetStats(0)
		for i in KS_V: KS_plot.Fill(i)
		GoodPlotFormat(KS_plot, "markers", ROOT.kBlack, 20)
		KS_mk = ROOT.TLine(KS_Vs[0], 0., KS_Vs[0], KS_plot.GetMaximum()*0.333333)
		KS_mk.SetLineColor(ROOT.kBlue)
		KS_mk.SetLineWidth(3)

		C_KS = ROOT.TCanvas()
		C_KS.cd()
		KS_plot.Draw("e")
		KS_mk.Draw("same")
		ROOT.gPad.SetTicks(1,1)
		ROOT.gPad.RedrawAxis()
		AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)

		C_KS.Print("../results/"+NAME+"/KS_"+cardname+".root")
		C_KS.Print("../results/"+NAME+"/KS_"+cardname+".png")
