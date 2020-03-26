import TEMPPAYLOAD
from TEMPPAYLOAD import *

text_file = open("results/"+NAME+"/LIMITS.txt", "w")
for Sigs in SIG:
	for VAR in EstVars:
		name = VAR[0]+"_"+VAR[3]
		C = "CARD_"+Sigs[3]+name+".txt"
		os.system("combine "+C+" -M AsymptoticLimits ")
		F = ROOT.TFile("higgsCombineTest.AsymptoticLimits.mH120.root")
		T = F.Get("limit")
		T.GetEntry(5)
		obs = T.limit
		T.GetEntry(0)
		m2 = T.limit
		T.GetEntry(1)
		m1 = T.limit
		T.GetEntry(2)
		exp = T.limit
		T.GetEntry(3)
		p1 = T.limit
		T.GetEntry(4)
		p2 = T.limit
		l = [Sigs[3]+name, obs, m2, m1, exp, p1, p2]
		text_file.write(l[0] + ", %f ,%f, %f ,%f, %f ,%f\n"%(l[1],l[2],l[3],l[4],l[5],l[6]))
		
		os.system("combine -M GoodnessOfFit -d "+Sigs[3]+name+"FitWorkspace.root --snapshotName "+Sigs[3]+name+"BOFit --algo=saturated")
		KS_Fs = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH120.root")
		KS_Ts = KS_Fs.Get("limit")
		KS_Vs = []
		for i in range(0,KS_Ts.GetEntries()):
			KS_Ts.GetEntry(i)
			KS_Vs.append(KS_Ts.limit)
		os.system("combine -M GoodnessOfFit -d "+Sigs[3]+name+"FitWorkspace.root --snapshotName "+Sigs[3]+name+"BOFit --algo=saturated -t 100")
		KS_F = ROOT.TFile("higgsCombineTest.GoodnessOfFit.mH120.123456.root")	
		KS_T = KS_F.Get("limit")
		KS_V = []
		for i in range(0,KS_T.GetEntries()):
			KS_T.GetEntry(i)
			KS_V.append(KS_T.limit)
		minKS = min(min(KS_V),min(KS_Vs))
		maxKS = max(max(KS_V),max(KS_Vs))
		rangeKS = maxKS - minKS
		KS_plot = ROOT.TH1F(Sigs[3]+name+"_KS_plot", ";Goodness Of Fit Statistic (Saturated);toys", 50, minKS-(rangeKS/10), maxKS+(rangeKS/10))
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
		AddCMSLumi(ROOT.gPad, LUMI, cmsextra)

		C_KS.Print("results/"+NAME+"/GoF_"+Sigs[3]+name+".root")
		C_KS.Print("results/"+NAME+"/GoF_"+Sigs[3]+name+".png")
		
		INJ = [0., 1., 2.]
		for i in INJ:
			os.system("combine -M GenerateOnly -d "+Sigs[3]+name+"FitWorkspace.root --snapshotName "+Sigs[3]+name+"BOFit -t 75 --saveToys --toysFrequentist  --expectSignal "+str(i*l[4])+" -n "+NAME+str(i)+" --bypassFrequentistFit")
			os.system("combine -M FitDiagnostics -d "+Sigs[3]+name+"FitWorkspace.root --snapshotName "+Sigs[3]+name+"BOFit --bypassFrequentistFit --skipBOnlyFit -t 75 --toysFile higgsCombine"+NAME+str(i)+".GenerateOnly.mH120.123456.root --rMin -10 --rMax 10 --saveWorkspace -n "+NAME+str(i))
			F = ROOT.TFile("../analysis/fitDiagnostics"+NAME+str(i)+".root")
			T = F.Get("tree_fit_sb")
			H = ROOT.TH1F("Bias Test, injected r="+str(int(i)), ";(#mu_{measured} - #mu_{injected})/#sigma_{#mu};toys", 40, -5., 5.)
			T.Draw("(r-%f)/rErr>>Bias Test, injected r="%(i*l[4])+str(int(i)), "fit_status == 0")
			G = ROOT.TF1("f"+NAME+str(i), "gaus(0)", -5.,5.)
			H.Fit(G)
			ROOT.gStyle.SetOptFit(1111)
			C_B = ROOT.TCanvas()
			C_B.cd()
			H.Draw("e0")
			C_B.Print("results/"+NAME+"/BIAS"+str(int(i))+"_"+Sigs[3]+name+".root")
			C_B.Print("results/"+NAME+"/BIAS"+str(int(i))+"_"+Sigs[3]+name+".png")
		

