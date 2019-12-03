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
		# MAKE NUIS PULL PLOT:
		print "Running combine for:   " + cardname
		os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M FitDiagnostics --saveShapes --saveWithUncertainties")
		FDFile = ROOT.TFile("fitDiagnostics.root")
		#fit_b = RooFitResult(FDFile.Get("fit_b"))
		fit_s = ROOT.RooFitResult(FDFile.Get("fit_s"))
		Nuis = ["lumi", "trig", "BBSF", "TTA", "TTNorm"]
		for i in range(NFITPAR):
			Nuis.append("P"+str(i))
		for i in SysWeighted:
			Nuis.append(i[0])
		for i in SysComputed:
			Nuis.append(i[0])
		NuisPulls = ROOT.TH1F("NuisPulls", "Post-Fit Nuissance Parameters;;#sigma", len(Nuis), 0, len(Nuis))
		NuisPulls.SetStats(0)
		NuisPulls.GetYaxis().CenterTitle(True)
		for b in range(NuisPulls.GetNbinsX()):
			N = fit_s.floatParsFinal().find(Nuis[b])
			NuisPulls.GetXaxis().SetBinLabel(b+1, Nuis[b])
			n = N.getVal()
			e = N.getError()
			NuisPulls.SetBinContent(b+1, n)
			NuisPulls.SetBinError(b+1, e)
		GoodPlotFormat(NuisPulls, "markers", ROOT.kBlack, 20)

		C_nuis = ROOT.TCanvas()
		C_nuis.cd()
		C_nuis.SetGridy()
		NuisPulls.Draw("e")
		NuisPulls.GetYaxis().SetRangeUser(-5.5,5.5)
		NuisPulls.Draw("samee")
		C_nuis.Print("../results/"+NAME+"/NuisPull_"+cardname+".root")
		C_nuis.Print("../results/"+NAME+"/NuisPull_"+cardname+".png")

		# MAKE PRE-POST FIT PLOTS:

		rDATA = FDFile.Get("shapes_prefit/SigReg/data")
		rBKG_PREFIT = FDFile.Get("shapes_prefit/SigReg/total_background")
		rBKG_PRETT = FDFile.Get("shapes_prefit/SigReg/ttbar")
		rBKG_S = FDFile.Get("shapes_fit_s/SigReg/total_background")
		rBKG_STT = FDFile.Get("shapes_fit_s/SigReg/ttbar")
		rSIGNAL = FDFile.Get("shapes_fit_s/SigReg/signal")
		template = ROOT.TH1F("template", ";"+VAR[2],len(VAR[1])-1, numpy.array(VAR[1]))
		DATA = convertAsymGraph(rDATA, template, "data_"+cardname)
		BKG_PREFIT = convertBinNHist(rBKG_PREFIT, template, "bkg_pre_"+cardname)
		BKG_PRETT = convertBinNHist(rBKG_PRETT, template, "tt_pre_"+cardname)
		BKG_S  = convertBinNHist(rBKG_S, template, "bkg_fit_"+cardname)
		BKG_STT = convertBinNHist(rBKG_STT, template, "tt_fit_"+cardname)
		SIGNAL = convertBinNHist(rSIGNAL, template, "signal_"+cardname)

		ErrOldUp, ErrOldDown = GetErrHists(BKG_PREFIT,"old_"+cardname)
		ErrNewUp, ErrNewDown = GetErrHists(BKG_S,"new_"+cardname)

		GoodPlotFormat(DATA, "markers", ROOT.kBlack, 20)
		GoodPlotFormat(BKG_PREFIT, "thickline", ROOT.kBlue, 1)
		GoodPlotFormat(ErrOldDown, "thinline", ROOT.kBlue, 3)
		GoodPlotFormat(ErrOldUp, "thinline", ROOT.kBlue, 3)
		GoodPlotFormat(BKG_S, "thickline", ROOT.kRed, 1)
		GoodPlotFormat(ErrNewDown, "thinline", ROOT.kRed, 2)
		GoodPlotFormat(ErrNewUp, "thinline", ROOT.kRed, 2)
		GoodPlotFormat(BKG_PRETT, "thinline", ROOT.kGreen, 2) 
		GoodPlotFormat(BKG_STT, "thickline", ROOT.kGreen, 2) 
		GoodPlotFormat(SIGNAL, "fill", ROOT.kRed, 3003)

		L = ROOT.TLegend(0.56,0.56,0.89,0.89)
		L.SetLineColor(0)
		L.SetFillColor(0)
		L.AddEntry(DATA, "Data", "PE")
		L.AddEntry(BKG_PREFIT, "Total Background (Pre-Fit)", "L")
		L.AddEntry(ErrOldDown, "Total Background Uncertainty (Pre-Fit)", "F")
		L.AddEntry(BKG_S, "Total Background (Post-Fit)", "L")
		L.AddEntry(ErrNewDown, "Total Background Uncertainty (Post-Fit)", "F")
		L.AddEntry(BKG_PRETT, "t#bar{t} component (Pre-Fit)", "L")
		L.AddEntry(BKG_STT, "t#bar{t} component (Post-Fit)", "L")
		L.AddEntry(SIGNAL, Sigs[4] + " (Post-Fit)", "F")

		SIGNAL.Add(BKG_S)
		BKG_S.SetFillColorAlpha(ROOT.kWhite, 0.0)
		#BKG_S.SetFillStyle()
		FindAndSetMax(DATA, BKG_PREFIT, BKG_S, SIGNAL)

		C_CombWork = ROOT.TCanvas()
		C_CombWork.cd()
		SIGNAL.Draw("hist")
		BKG_S.Draw("histsame")
		BKG_PREFIT.Draw("histsame")
		ErrOldUp.Draw("histsame")
		ErrOldDown.Draw("histsame")
		ErrNewUp.Draw("histsame")
		ErrNewDown.Draw("histsame")
		BKG_PRETT.Draw("histsame")
		BKG_STT.Draw("histsame")
		DATA.Draw("esame")
		L.Draw("same")
		ROOT.gPad.SetTicks(1,1)
		ROOT.gPad.RedrawAxis()
		AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)

		C_CombWork.Print("../results/"+NAME+"/CombResult_S_"+cardname+".root")
		C_CombWork.Print("../results/"+NAME+"/CombResult_S_"+cardname+".png")

		# MAKE MONEY PLOTS:

		os.system("rm higgsCombineTest.FitDiagnostics.mH120.root")
		os.system("rm combine_logger.out")
		os.system("rm fitDiagnostics.root")
