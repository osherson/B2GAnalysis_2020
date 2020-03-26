import TEMPPAYLOAD
from TEMPPAYLOAD import *

for Sigs in SIG:
	for VAR in EstVars:
		name = VAR[0]+"_"+VAR[3]
		os.system("combine CARD_"+Sigs[3]+name+".txt -M FitDiagnostics --saveShapes --saveWithUncertainties --ignoreCovWarning --saveWorkspace --setParameters SRP0=0.1")
		refF = ROOT.TFile("SHAPES_"+Sigs[3]+name+".root")
		refH = refF.Get("SR"+NAME+"_data_obs")
		CbnF = ROOT.TFile("fitDiagnostics.root")
		for P in ["prefit", "fit_b", "fit_s"]:
			for R in ["SR", "CR"]:
				cDATA = CbnF.Get("shapes_"+P+"/"+R+NAME+"/data")
				cTT = CbnF.Get("shapes_"+P+"/"+R+NAME+"/ttbar"+NAME)
				cTBKG = CbnF.Get("shapes_"+P+"/"+R+NAME+"/total_background")
				cSIG = CbnF.Get("shapes_"+P+"/"+R+NAME+"/total_signal")
				cDATA = convertAsymGraph(cDATA, cTT, "data"+R+P)
				Hvec = []
				for i in [cDATA, cTT, cTBKG, cSIG]:
					Hvec.append(Reroll(convertBinNHist(i, refH, i.GetName()+"new"+P+R), VAR))
				
				Pull2D = Hvec[0][2].Clone("pull"+R+P)
				Pull2D.Add(Hvec[2][2], -1.)
				Pull2D.Divide(Hvec[0][3])
				Hvec[2][3].Divide(Hvec[0][3])
				Pull2D.GetZaxis().SetRangeUser(-3.,3.)
				
				
				C2 = ROOT.TCanvas()
				C2.cd()
				Pull2D.Draw("colz")
				C2.Print("results/"+NAME+"/Pull2D_"+P+"_"+R+".png")
				
				C2e = ROOT.TCanvas()
				C2e.cd()
				Hvec[3][2].Draw("colz")
				C2e.Print("results/"+NAME+"/Sig2D_"+P+"_"+R+".png")
				
				for W in [0, 1]:
					data = DBBW(Hvec[0][W])
					GoodPlotFormat(data, "markers", ROOT.kBlack, 20)
					bkg = DBBW(Hvec[2][W])
					GoodPlotFormat(data,"thickline", ROOT.kBlue, 1)
					ttbar = DBBW(Hvec[1][W])
					GoodPlotFormat(ttbar,"thickline", ROOT.kRed, 1)
					sig = DBBW(Hvec[3][W])
					GoodPlotFormat(sig, "fill", ROOT.kGreen+1, 3003)
					cheapline = data.Clone("cheapline")
					cheapline.Add(data,-1.)
					cheapline.GetYaxis().SetTitle("#frac{data - bkg}{#sigma_{data}}")
					cheapline.GetYaxis().SetTitleSize(0.175);
					cheapline.GetYaxis().SetNdivisions(6);
					cheapline.GetYaxis().SetLabelSize(0.145);
					cheapline.GetYaxis().SetTitleOffset(0.225);
					cheapline.GetYaxis().CenterTitle(True)
					cheapline.GetYaxis().SetRangeUser(-5.,5.)
					GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
					bkg.GetYaxis().SetTitle("Events / GeV")
					bkg.GetYaxis().SetTitleOffset(0.5);
					bkg.GetYaxis().SetTitleSize(0.075);
					FindAndSetMax(data, bkg)
					
					E = []
					EP = []
					for i in range(1,data.GetNbinsX()+1):
						Err = bkg.GetBinError(i)
						
						blX = bkg.GetBinLowEdge(i)
						blY = bkg.GetBinContent(i) - Err
						trX = bkg.GetBinWidth(i) + blX
						trY = bkg.GetBinContent(i) + Err
						tBox = ROOT.TBox(blX,blY,trX,trY)
						if  data.GetBinError(i) > 0:
							ue = Err/data.GetBinError(i)
						else:
							ue = Err/2.7
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
										
					bkg.GetXaxis().SetLabelSize(0)
					
					pull = data.Clone("pull")
					pull.Add(bkg, -1.)
					GoodPlotFormat(pull, "markers", ROOT.kBlack, 20)
					for i in range(pull.GetNbinsX()):
						if not data.GetBinContent(i+1) == 0:
							pull.SetBinContent(i+1, pull.GetBinContent(i+1)/data.GetBinError(i+1))
							pull.SetBinError(i+1, 1)		
						else:
							pull.SetBinContent(i+1, 0)
							pull.SetBinError(i+1, 0)
					
					L = ROOT.TLegend(0.48,0.6,0.86,0.86)
					L.SetFillColor(0)
					L.SetLineColor(0)
					if not Blind: L.AddEntry(data, "data", "PE")
					L.AddEntry(bkg, "total background", "L")
					L.AddEntry(ttbar, "t#bar{t} component", "L")
					L.AddEntry(E[0], "background uncertainty", "F")
					if P != "fit_b":  L.AddEntry(sig, Sigs[4], "F")
					
					C = ROOT.TCanvas()
					C.cd()
					p12 = ROOT.TPad("pad1", "tall",0,0.165,1,1)
					p22 = ROOT.TPad("pad2", "short",0,0.0,1.0,0.23)
					p22.SetBottomMargin(0.35)
					p12.Draw()
					p22.Draw()
					p12.cd() # top
					ROOT.gPad.SetTicks(1,1)
					bkg.Draw("hist")
					ttbar.Draw("histsame")
					if P != "fit_b": sig.Draw("histsame")
					for e in E: e.Draw("same")
					data.Draw("esame")
					L.Draw("same")
					ROOT.TGaxis.SetMaxDigits(3)
					p12.RedrawAxis()
					AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
					p22.cd() # bottom
					ROOT.gPad.SetTicks(1,1)
					cheapline.GetXaxis().SetTitleSize(0.1925);
					cheapline.GetXaxis().SetLabelSize(0.16);
					cheapline.GetXaxis().SetTitleOffset(0.84);
					cheapline.Draw("hist")
					for e in EP: e.Draw("same")
					pull.Draw("esame")
					p22.RedrawAxis()
					C.Print("results/"+NAME+"/"+P+R+VAR[3*W]+".root")
					C.Print("results/"+NAME+"/"+P+R+VAR[3*W]+".png")
