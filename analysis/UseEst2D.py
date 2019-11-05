from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")



for VAR in EstVars2D:
	print "Working on "+VAR[0] + "_vs_" + VAR[3]

	A2 = outF.Get("rA_data_"+VAR[0]+"_"+VAR[3])
	Att2 = outF.Get("rA_ttbar_"+VAR[0]+"_"+VAR[3])
	B2 = outF.Get("rB_nom_data_"+VAR[0]+"_"+VAR[3])
	B_up2 = outF.Get("rB_up_data_"+VAR[0]+"_"+VAR[3])
	B_down2 = outF.Get("rB_down_data_"+VAR[0]+"_"+VAR[3])
	B_stat2 = outF.Get("rB_stat_data_"+VAR[0]+"_"+VAR[3])
	Btt2 = outF.Get("rB_nom_ttbar_"+VAR[0]+"_"+VAR[3])
	Btt_stat2 = outF.Get("rB_stat_ttbar_"+VAR[0]+"_"+VAR[3])
	Btt_up2 = outF.Get("rB_up_ttbar_"+VAR[0]+"_"+VAR[3])
	Btt_down2 = outF.Get("rB_down_ttbar_"+VAR[0]+"_"+VAR[3])

	B2.Add(Btt2, -1.)
	B2.Add(Att2, 1.)
	B_up2.Add(Btt_up2, -1.)
	B_up2.Add(Att2, 1.)
	B_down2.Add(Btt_down2, -1.)
	B_down2.Add(Att2, 1.)
	B_stat2.Add(Btt_stat2, -1.)

	A = Unroll(A2)
	Att = Unroll(Att2)
	B = Unroll(B2)
	B_up = Unroll(B_up2)
	B_down = Unroll(B_down2)
	B_stat = Unroll(B_stat2)

	## SET UP THE PULL:
	pull = A.Clone("pull")
	pull2 = A2.Clone("pull2")

	pull.Add(B, -1.)
	pull2.Add(B2, -1.)
	pull.GetXaxis().SetTitle("unrolled: " + VAR[2] + ", " + VAR[5])

	for i in range(pull.GetNbinsX()):
		if not A.GetBinContent(i+1) == 0:
			pull.SetBinContent(i+1, pull.GetBinContent(i+1)/A.GetBinError(i+1))
			pull.SetBinError(i+1, 1)		
		else:
			pull.SetBinContent(i+1, 0)
			pull.SetBinError(i+1, 0)
	for i in range(pull2.GetNbinsX()):
		if not A2.GetBinContent(i+1) == 0:
			pull2.SetBinContent(i+1, pull2.GetBinContent(i+1)/A2.GetBinError(i+1))
			pull2.SetBinError(i+1, 1)		
		else:
			pull2.SetBinContent(i+1, 0)
			pull2.SetBinError(i+1, 0)
	pull2.GetZaxis().SetRangeUser(-5.,5.)

	E = []
	EP = []
	for i in range(1,A.GetNbinsX()+1):
		Err2 = math.fabs(B_up.GetBinContent(i) - B.GetBinContent(i))*math.fabs(B_up.GetBinContent(i) - B.GetBinContent(i))
		try:
			ErrStat2 = B.GetBinContent(i)*(B_stat.GetBinError(i)/B_stat.GetBinContent(i))*B.GetBinContent(i)*(B_stat.GetBinError(i)/B_stat.GetBinContent(i))
		except:
			ErrStat2 = 0.
		Err = math.sqrt(Err2 + ErrStat2)
		blX = B.GetBinLowEdge(i)
		blY = B.GetBinContent(i) - Err
		trX = B.GetBinWidth(i) + blX
		trY = B.GetBinContent(i) + Err
		tBox = ROOT.TBox(blX,blY,trX,trY)
		if  A.GetBinError(i) > 0:
			ue = Err/A.GetBinError(i)
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

	## ALL THE PRETTY PARTS:
	cheapline = A.Clone("cheapline")
	cheapline.Add(A,-1.)
	GoodPlotFormat(A, "markers", ROOT.kBlack, 20)
	GoodPlotFormat(pull, "markers", ROOT.kBlack, 20)
	GoodPlotFormat(B, "thickline", ROOT.kMagenta, 1)
	GoodPlotFormat(Att, "thickline", ROOT.kRed, 2)
	GoodPlotFormat(cheapline, "thinline", ROOT.kGray, 4)
	cheapline.GetXaxis().SetTitle(VAR[2])
	cheapline.GetYaxis().SetTitle("")
	B.GetYaxis().SetTitle("Events")
	B.GetYaxis().SetTitleOffset(0.5);
	B.GetYaxis().SetTitleSize(0.075);
	cheapline.GetYaxis().SetTitle("#frac{data - bkg}{#sigma_{data}}")
	cheapline.GetYaxis().SetTitleSize(0.175);
	cheapline.GetYaxis().SetNdivisions(6);
	cheapline.GetYaxis().SetLabelSize(0.145);
	cheapline.GetYaxis().SetTitleOffset(0.225);
	cheapline.GetXaxis().SetTitleSize(0.1925);
	cheapline.GetXaxis().SetLabelSize(0.16);
	cheapline.GetXaxis().SetTitleOffset(0.84);
	cheapline.GetYaxis().CenterTitle(True)
	B.GetXaxis().SetLabelSize(0)

	L = ROOT.TLegend(0.48,0.6,0.86,0.86)
	L.SetFillColor(0)
	L.SetLineColor(0)
	if not Blind: L.AddEntry(A, "Data", "PE")
	L.AddEntry(B, "Total background", "L")
	L.AddEntry(Att, "t#bar{t} component", "L")
	L.AddEntry(E[0], "Background uncertainty", "F")

	SigFills = [3003, 3004, 3005, 3006, 3007]
	SigFillIndex = 0
	plot_sig = []
	plot_sig2 = []
	for S in SIG:
		S_temp2 = outF.Get("rA_"+S[3]+"_"+VAR[0]+"_"+VAR[3])
		plot_sig2.append(S_temp2)
		S_temp = Unroll(S_temp2)
		GoodPlotFormat(S_temp, "fill", ROOT.kBlue, SigFills[SigFillIndex])
		L.AddEntry(S_temp, S[4], "F")
		plot_sig.append(S_temp)
		SigFillIndex += 1
	plot_sig_pulls = []
	for s in plot_sig:
		s_pull = s.Clone("pull"+str(len(plot_sig_pulls)))
		for i in range(pull.GetNbinsX()):
			try: s_pull.SetBinContent(i+1,s_pull.GetBinContent(i+1)/A.GetBinError(i+1))
			except: s_pull.SetBinContent(i+1,0)


	C_var_tmp = ROOT.TCanvas()
	C_var_tmp.cd()
	p12 = ROOT.TPad("pad1", "tall",0,0.165,1,1)
	p22 = ROOT.TPad("pad2", "short",0,0.0,1.0,0.23)
	p22.SetBottomMargin(0.35)
	p12.Draw()
	p22.Draw()
	p12.cd()
	ROOT.gPad.SetTicks(1,1)
	# DRAW IN TOP PAD:
	B.Draw("hist")
	Att.Draw("histsame")
	for e in E:
		e.Draw("same")
	for s in plot_sig: s.Draw("samehist")
	if not Blind:
		A.Draw("esame")
	L.Draw("same")
	ROOT.TGaxis.SetMaxDigits(3)
	p12.RedrawAxis()
	AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)
	p22.cd()
	ROOT.gPad.SetTicks(1,1)
	# DRAW IN BOTTOM PAD:
	cheapline.Draw("hist")
	cheapline.GetYaxis().SetRangeUser(-5.,5.)
	for e in EP:
		e.Draw("same")
	for s in plot_sig_pulls: s.Draw("samehist")
	if not Blind:
		pull.Draw("esame")
	C_var_tmp.Print("../results/"+NAME+"/VAREST_"+NAME+"_"+VAR[0] + "_vs_" + VAR[3]+".root")
	C_var_tmp.Print("../results/"+NAME+"/VAREST_"+NAME+"_"+VAR[0] + "_vs_" + VAR[3]+".png")

	pull2.SetStats(0)
	GoodPlotFormat(A2, "markers", ROOT.kBlack, 20)
	GoodPlotFormat(B2, "thinline", ROOT.kMagenta, 1)

	C_var_2D_tmp = ROOT.TCanvas()
	C_var_2D_tmp.Divide(2,1)
	C_var_2D_tmp.cd(1)
	A2.Draw("E")
	B2.Draw("sameSURF")
	AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)
	C_var_2D_tmp.cd(2)
	pull2.Draw("colz")
	AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)
	C_var_2D_tmp.Print("../results/"+NAME+"/VAREST2D_"+NAME+"_"+VAR[0] + "_vs_" + VAR[3]+".root")
	C_var_2D_tmp.Print("../results/"+NAME+"/VAREST2D_"+NAME+"_"+VAR[0] + "_vs_" + VAR[3]+".png")

outF.Close()