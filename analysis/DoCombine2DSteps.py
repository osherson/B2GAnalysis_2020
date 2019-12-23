import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

print "RUNNING COMBINE CARDS: (if not blinded)"
if not Blind:
	for Sigs in SIG:
		for VAR in EstVars2D:
			if not VAR[6]: continue
			cardname = VAR[0]+"_vs_"+VAR[3]+"_"+Sigs[3]
			os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M FitDiagnostics --saveShapes --saveWithUncertainties --ignoreCovWarning " + EXTRACOMBINEOPTION)
			FDFile = ROOT.TFile("fitDiagnostics.root")
			fit_b = ROOT.RooFitResult(FDFile.Get("fit_b"))
			fit_s = ROOT.RooFitResult(FDFile.Get("fit_s"))
			Nuis = ["lumi", "trig", "BBSF", "TTA", "TTNorm"]
			for i in range(NFITPAR):
				Nuis.append("P"+str(i))
			for i in SysWeighted:
				Nuis.append(i[0])
			for i in SysComputed:
				Nuis.append(i[0])
			NuisSPulls = ROOT.TH1F("NuisSPulls", "Post-Fit Nuissance Parameters;;#sigma", len(Nuis), 0, len(Nuis))
			NuisBPulls = ROOT.TH1F("NuisBPulls", "Post-Fit Nuissance Parameters;;#sigma", len(Nuis), 0, len(Nuis))
			NuisSPulls.SetStats(0)
			NuisSPulls.GetYaxis().CenterTitle(True)
			for b in range(NuisSPulls.GetNbinsX()):
				N = fit_s.floatParsFinal().find(Nuis[b])
				NuisSPulls.GetXaxis().SetBinLabel(b+1, Nuis[b])
				n = N.getVal()
				e = N.getError()
				NuisSPulls.SetBinContent(b+1, n)
				NuisSPulls.SetBinError(b+1, e)
				N = fit_b.floatParsFinal().find(Nuis[b])
				n = N.getVal()
				e = N.getError()
				NuisBPulls.SetBinContent(b+1, n)
				NuisBPulls.SetBinError(b+1, e)
			GoodPlotFormat(NuisBPulls, "markers", ROOT.kBlue, 20)
			GoodPlotFormat(NuisSPulls, "markers", ROOT.kRed, 20)

			Leg = ROOT.TLegend(0.2,0.8,0.8,0.89)
			Leg.SetLineColor(0)
			Leg.SetFillColor(0)
			Leg.AddEntry(NuisBPulls, "background only", "PL")
			Leg.AddEntry(NuisSPulls, "signal + background", "PL")

			C_nuis = ROOT.TCanvas()
			C_nuis.cd()
			C_nuis.SetGridy()
			NuisSPulls.Draw("e")
			NuisSPulls.GetYaxis().SetRangeUser(-5.5,5.5)
			NuisSPulls.Draw("samee")
			NuisBPulls.Draw("samee")
			Leg.Draw("same")
			C_nuis.Print("../results/"+NAME+"/NuisPull_"+cardname+".root")
			C_nuis.Print("../results/"+NAME+"/NuisPull_"+cardname+".png")

			# Make re-rolled proof plots:

			# MAKE PRE-POST FIT (B only) PLOTS:

			rrDATA = FDFile.Get("shapes_prefit/SigReg/data")
			rBKG_PREFIT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/total_background"), VAR)
			rBKG_PRETT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/ttbar"), VAR)
			rSIGNAL_PREFIT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/signal"), VAR)
			rBKG_S = RerollCombined(FDFile.Get("shapes_fit_b/SigReg/total_background"), VAR)
			rBKG_STT = RerollCombined(FDFile.Get("shapes_fit_b/SigReg/ttbar"), VAR)
			rDATA = RerollCombined(convertAsymGraph(rrDATA, FDFile.Get("shapes_fit_b/SigReg/ttbar"), "data_"+cardname), VAR)

			for axis in [0,1]: ## fit_b
				DATA = rDATA[axis]
				BKG_PREFIT = rBKG_PREFIT[axis]
				BKG_PRETT = rBKG_PRETT[axis]
				SIGNAL_PREFIT = rSIGNAL_PREFIT[axis]
				BKG_S = rBKG_S[axis]
				BKG_STT = rBKG_STT[axis]

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

				L = ROOT.TLegend(0.53,0.56,0.89,0.89)
				L.SetLineColor(0)
				L.SetFillColor(0)
				L.AddEntry(DATA, "Data", "PE")
				L.AddEntry(BKG_PREFIT, "Total Background (Pre-Fit)", "L")
				L.AddEntry(ErrOldDown, "Total Background Uncertainty (Pre-Fit)", "F")
				L.AddEntry(BKG_S, "Total Background (background only)", "L")
				L.AddEntry(ErrNewDown, "Total Background Uncertainty (background only)", "F")
				L.AddEntry(BKG_PRETT, "t#bar{t} component (Pre-Fit)", "L")
				L.AddEntry(BKG_STT, "t#bar{t} component (background only)", "L")

				BKG_S.SetFillColorAlpha(ROOT.kWhite, 0.0)
				FindAndSetMax(DATA, BKG_PREFIT, BKG_S)

				C_CombWork = ROOT.TCanvas()
				C_CombWork.cd()
				BKG_S.Draw("hist")
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

				C_CombWork.Print("../results/"+NAME+"/CombResult"+str(axis)+"_B_"+cardname+".root")
				C_CombWork.Print("../results/"+NAME+"/CombResult"+str(axis)+"_B_"+cardname+".png")

				# MAKE MONEY PLOTS:

				A = DATA.Clone("A")
				B = BKG_S.Clone("B")
				Att = BKG_STT.Clone("Att")

				pull = A.Clone("pull")
				pull.Add(B, -1.)
				for i in range(pull.GetNbinsX()):
					if not A.GetBinContent(i+1) == 0:
						pull.SetBinContent(i+1, pull.GetBinContent(i+1)/A.GetBinError(i+1))
						pull.SetBinError(i+1, 1)		
					else:
						pull.SetBinContent(i+1, 0)
						pull.SetBinError(i+1, 0)

				E = []
				EP = []
				for i in range(1,A.GetNbinsX()+1):
					print "bin = "+str(i)+"-----------"
					print str(A.GetBinContent(i)) + " < A Content"
					print str(B.GetBinContent(i)) + " < B Content"
					Err = ErrNewUp.GetBinContent(i) - B.GetBinContent(i)
					print str(Err) + " < Bin error"
					blX = B.GetBinLowEdge(i)
					blY = B.GetBinContent(i) - Err
					trX = B.GetBinWidth(i) + blX
					trY = B.GetBinContent(i) + Err
					tBox = ROOT.TBox(blX,blY,trX,trY)
					if  A.GetBinError(i) > 0:
						ue = Err/A.GetBinError(i)
					else:
						ue = Err/2.7
					print str(A.GetBinError(i)) + " < A Error"
					ue = min(5.0, ue)
					tPBox = ROOT.TBox(blX, -1*ue, trX, ue)
					tBox.SetFillColor(25)
					tBox.SetFillStyle(3144)
					tPBox.SetFillColor(25)
					tPBox.SetFillStyle(3144)
					tBox.SetLineColor(ROOT.kWhite)
					tPBox.SetLineColor(ROOT.kWhite)
					E.append(tBox)
					EP.append(tPBox)

				## ALL THE PRETTY PARTS:
				cheapline = A.Clone("cheapline")
				cheapline.Add(A,-1.)
				GoodPlotFormat(A, "markers", ROOT.kBlack, 20)
				GoodPlotFormat(pull, "markers", ROOT.kBlack, 20)
				GoodPlotFormat(B, "thickline", ROOT.kMagenta, 1)
				GoodPlotFormat(Att, "thickline", ROOT.kRed, 2)
				GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
				cheapline.GetXaxis().SetTitle(VAR[2+ (3*axis)])
				cheapline.GetYaxis().SetTitle("")
				B.GetYaxis().SetTitle("Events")
				B.GetYaxis().SetTitleOffset(0.5)
				B.GetYaxis().SetTitleSize(0.075)
				cheapline.GetYaxis().SetTitle("#frac{data - bkg}{#sigma_{data}}")
				cheapline.GetYaxis().SetTitleSize(0.175)
				cheapline.GetYaxis().SetNdivisions(6)
				cheapline.GetYaxis().SetLabelSize(0.145)
				cheapline.GetYaxis().SetTitleOffset(0.225)
				cheapline.GetXaxis().SetTitleSize(0.1925)
				cheapline.GetXaxis().SetLabelSize(0.16)
				cheapline.GetXaxis().SetTitleOffset(0.84)
				cheapline.GetYaxis().CenterTitle(True)
				B.GetXaxis().SetLabelSize(0)
				FindAndSetMax(A, B)

				L = ROOT.TLegend(0.48,0.6,0.86,0.86)
				L.SetFillColor(0)
				L.SetLineColor(0)
				L.AddEntry(A, "Data", "PE")
				L.AddEntry(B, "Total background", "L")
				L.AddEntry(Att, "t#bar{t} component", "L")
				L.AddEntry(E[0], "Background uncertainty", "F")
			
				C_CombMoney = ROOT.TCanvas()
				C_CombMoney.cd()
				p12 = ROOT.TPad("pad1", "tall",0,0.165,1,1)
				p22 = ROOT.TPad("pad2", "short",0,0.0,1.0,0.23)
				p22.SetBottomMargin(0.35)
				p12.Draw()
				p22.Draw()
				p12.cd()
				ROOT.gPad.SetTicks(1,1)

				B.Draw("hist")
				Att.Draw("histsame")
				for e in E:
					e.Draw("same")
				A.Draw("esame")
				L.Draw("same")
				ROOT.TGaxis.SetMaxDigits(3)
				p12.RedrawAxis()
				AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)
				p22.cd()
				ROOT.gPad.SetTicks(1,1)
				cheapline.Draw("hist")
				cheapline.GetYaxis().SetRangeUser(-5.,5.)
				for e in EP:
					e.Draw("same")
				pull.Draw("esame")
				C_CombMoney.Print("../results/"+NAME+"/Money"+str(axis)+"_"+cardname+".root")
				C_CombMoney.Print("../results/"+NAME+"/Money"+str(axis)+"_"+cardname+".png")

			# MAKE PRE-POST FIT (B+S) PLOTS:

			rrDATA = FDFile.Get("shapes_prefit/SigReg/data")
			rBKG_PREFIT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/total_background"), VAR)
			rBKG_PRETT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/ttbar"), VAR)
			rSIGNAL_PREFIT = RerollCombined(FDFile.Get("shapes_prefit/SigReg/signal"), VAR)
			rBKG_S = RerollCombined(FDFile.Get("shapes_fit_s/SigReg/total_background"), VAR)
			rBKG_STT = RerollCombined(FDFile.Get("shapes_fit_s/SigReg/ttbar"), VAR)
			rDATA = RerollCombined(convertAsymGraph(rrDATA, FDFile.Get("shapes_fit_b/SigReg/ttbar"), "data_"+cardname), VAR)
			rSIGNAL = RerollCombined(FDFile.Get("shapes_fit_s/SigReg/signal"), VAR)


			for axis in [0,1]: ## fit_s
				DATA = rDATA[axis]
				BKG_PREFIT = rBKG_PREFIT[axis]
				BKG_PRETT = rBKG_PRETT[axis]
				SIGNAL_PREFIT = rSIGNAL_PREFIT[axis]
				BKG_S = rBKG_S[axis]
				BKG_STT = rBKG_STT[axis]
				SIGNAL = rSIGNAL[axis]

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

				L = ROOT.TLegend(0.53,0.56,0.89,0.89)
				L.SetLineColor(0)
				L.SetFillColor(0)
				L.AddEntry(DATA, "Data", "PE")
				L.AddEntry(BKG_PREFIT, "Total Background (Pre-Fit)", "L")
				L.AddEntry(ErrOldDown, "Total Background Uncertainty (Pre-Fit)", "F")
				L.AddEntry(BKG_S, "Total Background (signal + background)", "L")
				L.AddEntry(ErrNewDown, "Total Background Uncertainty (signal + background)", "F")
				L.AddEntry(BKG_PRETT, "t#bar{t} component (Pre-Fit)", "L")
				L.AddEntry(BKG_STT, "t#bar{t} component (signal + background)", "L")
				L.AddEntry(SIGNAL, Sigs[4] + " (signal + background)", "F")

				SIGNAL.Add(BKG_S)
				BKG_S.SetFillColorAlpha(ROOT.kWhite, 0.)
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

				C_CombWork.Print("../results/"+NAME+"/CombResult"+str(axis)+"_S_"+cardname+".root")
				C_CombWork.Print("../results/"+NAME+"/CombResult"+str(axis)+"_S_"+cardname+".png")

			os.system("rm higgsCombineTest.FitDiagnostics.mH120.root")
			os.system("rm combine_logger.out")
			os.system("rm fitDiagnostics.root")