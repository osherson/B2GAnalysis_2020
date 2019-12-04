import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

if not Blind:
	for Sigs in SIG:
		for VAR in EstVars:
			if not VAR[3]: continue
			cardname = VAR[0]+"_"+Sigs[3]
			######################## Goodness of Fit test:
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

			C_KS.Print("../results/"+NAME+"/GoF_"+cardname+".root")
			C_KS.Print("../results/"+NAME+"/GoF_"+cardname+".png")

			########################## Now bias tests:
			INJ = [0., 1., 2., 5., 10.]
			for i in INJ:
				os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M GenerateOnly -t "+str(NTOYS)+" --saveToys --toysFrequentist  --expectSignal "+str(i)+" -n "+NAME+str(i)+" --bypassFrequentistFit")
				os.system("combine -M FitDiagnostics -d ../results/"+NAME+"/Card_"+cardname+".txt --bypassFrequentistFit --skipBOnlyFit -t "+str(NTOYS)+" --toysFile higgsCombine"+NAME+str(i)+".GenerateOnly.mH120.123456.root --rMin -5 --rMax "+str(max(i*5., 5))+" --saveWorkspace -n "+NAME+str(i))
				F = ROOT.TFile("../analysis/fitDiagnostics"+NAME+str(i)+".root")
				T = F.Get("tree_fit_sb")
				H = ROOT.TH1F("Bias Test, injected r="+str(int(i)), ";(#mu_{measured} - #mu_{injected})/#sigma_{#mu};toys", 40, -5., 5.)
				T.Draw("(r-%f)/rErr>>Bias Test, injected r="%i+str(int(i)), "fit_status == 0")
				G = ROOT.TF1("f"+NAME+str(i), "gaus(0)", -5.,5.)
				H.Fit(G)
				ROOT.gStyle.SetOptFit(1111)
				C_B = ROOT.TCanvas()
				C_B.cd()
				H.Draw("e0")
				C_B.Print("../results/"+NAME+"/BIAS"+str(int(i))+"_"+cardname+".root")
				C_B.Print("../results/"+NAME+"/BIAS"+str(int(i))+"_"+cardname+".png")


