import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "update")
def GetFits(reg, sys):
	A_data = outF.Get(reg+"A_fitvar_data")
	B_data = outF.Get(reg+"B_fitvar_data")
	C_data = outF.Get(reg+"C_fitvar_data")
	D_data = outF.Get(reg+"D_fitvar_data")

	A_ttbar = outF.Get(reg+"A_fitvar_ttbar"+sys)
	B_ttbar = outF.Get(reg+"B_fitvar_ttbar"+sys)
	C_ttbar = outF.Get(reg+"C_fitvar_ttbar"+sys)
	D_ttbar = outF.Get(reg+"D_fitvar_ttbar"+sys)

	A_tot = A_data.Clone(reg+"A_tot"+sys)
	A_tot.Add(A_ttbar, -1.)
	B_tot = B_data.Clone(reg+"B_tot"+sys)
	B_tot.Add(B_ttbar, -1.)
	C_tot = C_data.Clone(reg+"C_tot"+sys)
	C_tot.Add(C_ttbar, -1.)
	D_tot = D_data.Clone(reg+"D_tot"+sys)
	D_tot.Add(D_ttbar, -1.)

	AB = A_tot.Clone(reg+"AoverB"+sys)
	AB.Divide(B_tot)
	CD = C_tot.Clone(reg+"CoverD"+sys)
	CD.Divide(D_tot)
	return (AB, CD)

CompareFits = []
CompareLeg = ROOT.TLegend(0.5,0.6,0.89,0.89)

for R in ["CR", "SR"]:
	print "working on" + R
	AB_nom, CD_nom = GetFits(R, "")
	AB_au, CD_au = GetFits(R, "_au")
	AB_ad, CD_ad = GetFits(R, "_ad")
	AB_nu, CD_nu = GetFits(R, "_nu")
	AB_nd, CD_nd = GetFits(R, "_nd")
	
	F_AB_nom = FIT(R+"ABnomfit")
	AB_nom.Fit(F_AB_nom, "EM0R")
	F_CD_nom = FIT(R+"CDnomfit")
	CD_nom.Fit(F_CD_nom, "EM0R")
	
	F_CD_au = FIT(R+"aufit")
	CD_au.Fit(F_CD_au, "EM0R")
	F_CD_ad = FIT(R+"adfit")
	CD_ad.Fit(F_CD_ad, "EM0R")
	F_CD_nu = FIT(R+"nufit")
	CD_nu.Fit(F_CD_nu, "EM0R")
	F_CD_nd = FIT(R+"ndfit")
	CD_nd.Fit(F_CD_nd, "EM0R")
	
	GoodPlotFormat(CD_au, "markers", ROOT.kRed, 26)
	GoodPlotFormat(CD_ad, "markers", ROOT.kRed, 32)
	GoodPlotFormat(CD_nu, "markers", ROOT.kTeal+2, 26)
	GoodPlotFormat(CD_nd, "markers", ROOT.kTeal+2, 32)
	GoodPlotFormat(F_CD_au, "thinline", ROOT.kBlack, 2)
	GoodPlotFormat(F_CD_ad, "thinline", ROOT.kBlack, 3)
	GoodPlotFormat(F_CD_nu, "thinline", ROOT.kBlack, 4)
	GoodPlotFormat(F_CD_nd, "thinline", ROOT.kBlack, 5)
	
	CD_HEFit = ROOT.TGraphErrors(2500)
	for i in range(2500):
		CD_HEFit.SetPoint(i, FitVar[1][0] + i*(FitVar[1][-1] - FitVar[1][0])/2500., 0.)
	ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(CD_HEFit)
	F_CD_fit_up = ROOT.TH1F(R+"F_CD_fit_up", "", 2499, FitVar[1][0], FitVar[1][-1])
	F_CD_fit_down = ROOT.TH1F(R+"F_CD_fit_down", "", 2499, FitVar[1][0], FitVar[1][-1])
	Np = CD_HEFit.GetN()
	for i in range(Np):
		x = ROOT.Double(0.)
		y = ROOT.Double(0.)
		ey = CD_HEFit.GetErrorY(i)
		CD_HEFit.GetPoint(i,x,y)
		b = F_CD_fit_up.GetXaxis().FindBin(x)
		F_CD_fit_up.SetBinContent(b, y+ey)
		F_CD_fit_down.SetBinContent(b, y-ey)
		
	CD_nom.GetYaxis().SetTitle("pass-to-fail ratio")
	CD_nom.GetYaxis().SetTitleOffset(1.265);

	GoodPlotFormat(CD_nom, "markers", ROOT.kBlue, 20)
	GoodPlotFormat(AB_nom, "markers", ROOT.kBlack, 20)
	GoodPlotFormat(F_CD_nom, "thickline", ROOT.kMagenta, 1)
	GoodPlotFormat(F_AB_nom, "thickline", ROOT.kRed, 1)
	GoodPlotFormat(F_CD_fit_up, "thinline", ROOT.kMagenta, 2)
	GoodPlotFormat(F_CD_fit_down, "thinline", ROOT.kMagenta, 2)

	CompareFits.append(F_CD_nom)
	CompareLeg.AddEntry(F_CD_nom, "C over D ("+R+")", "L")
	CompareFits.append(F_AB_nom)
	CompareLeg.AddEntry(F_AB_nom, "A over B ("+R+")", "L")

	# PLOT FOR FIT
	FindAndSetMax(CD_nom, AB_nom)
	C_fit = ROOT.TCanvas()
	C_fit.cd()
	ROOT.gPad.SetTicks(1,1)
	CD_nom.Draw("e")
	F_CD_nom.Draw("same")
	if not Blind:
		F_AB_nom.Draw("same")
	F_CD_fit_up.Draw("same")
	F_CD_fit_down.Draw("same")
	if not Blind:
		AB_nom.Draw("esame")
	CD_nom.Draw("esame")
	L_fit = ROOT.TLegend(0.5,0.6,0.89,0.89)
	L_fit.SetLineColor(0)
	L_fit.SetFillColor(0)
	L_fit.AddEntry(CD_nom, "PF-ratio in regions C and D", "PE")
	if not Blind:
		L_fit.AddEntry(AB_nom, "PF-ratio in regions A and B", "PE")
	L_fit.AddEntry(F_CD_nom, "Fit to PF ratio in C and D", "L")
	L_fit.AddEntry(F_CD_fit_up, "Fit uncertainty", "F")
	if not Blind:
		L_fit.AddEntry(F_AB_nom, "Fit to PF ratio in A and B", "L")
	L_fit.Draw("same")
	AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
	C_fit.Print("results/"+NAME+"/FIT_"+R+"_nom.root")
	C_fit.Print("results/"+NAME+"/FIT_"+R+"_nom.png")

	outF.cd()
	F_CD_fit_up.Write()
	F_CD_fit_down.Write()

	# PLOT FOR TTBAR PARTS:
	FindAndSetMax(CD_nom, CD_au, CD_ad, CD_nu, CD_nd)
	GoodPlotFormat(CD_nom, "markers", ROOT.kBlue, 24)
	GoodPlotFormat(F_CD_fit_up, "thinline", ROOT.kMagenta, 1)
	GoodPlotFormat(F_CD_fit_down, "thinline", ROOT.kMagenta, 1)
	C_ttbar = ROOT.TCanvas()
	C_ttbar.cd()
	ROOT.gPad.SetTicks(1,1)
	CD_nom.Draw("e")
	CD_au.Draw("esame")
	CD_ad.Draw("esame")
	CD_nu.Draw("esame")
	CD_nd.Draw("esame")

	F_CD_au.Draw("same")
	F_CD_ad.Draw("same")
	F_CD_nu.Draw("same")
	F_CD_nd.Draw("same")
	CD_nom.Draw("esame")
	L_ttbar = ROOT.TLegend(0.5,0.6,0.89,0.89)
	L_ttbar.SetLineColor(0)
	L_ttbar.SetFillColor(0)
	L_ttbar.AddEntry(CD_nom, "PF ratio for nominal t#bar{t}", "PE")
	L_ttbar.AddEntry(CD_au, "PF ratio for low #alpha t#bar{t}", "PE")
	L_ttbar.AddEntry(F_CD_au, "Fit to PF for low #alpha t#bar{t}", "L")
	L_ttbar.AddEntry(CD_ad, "PF ratio for  high #alpha t#bar{t}", "PE")
	L_ttbar.AddEntry(F_CD_ad, "Fit to PF for high #alpha t#bar{t}", "L")
	L_ttbar.AddEntry(CD_nu, "PF ratio for high normalization t#bar{t}", "PE")
	L_ttbar.AddEntry(F_CD_nu, "Fit to PF for high normalization t#bar{t}", "L")
	L_ttbar.AddEntry(CD_nd, "PF ratio for  low normalization t#bar{t}", "PE")
	L_ttbar.AddEntry(F_CD_nd, "Fit to PF for low normalization t#bar{t}", "L")
	L_ttbar.Draw("same")

	AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
	C_ttbar.Print("results/"+NAME+"/FIT_"+R+"ttbar.root")
	C_ttbar.Print("results/"+NAME+"/FIT_"+R+"ttbar.png")

	outF.cd()

	F_CD_nom.Write()
	F_CD_au.Write()
	F_CD_ad.Write()
	F_CD_nu.Write()
	F_CD_nd.Write()

	#### 
	# Now we need to save the +/- uncertainty versions of all these fits!
	# First we will need to create a bunch of weird firts:
	U_fits = []
	D_fits = []
	L_unc = ROOT.TLegend(0.5,0.6,0.89,0.89)
	L_unc.SetLineColor(0)
	L_unc.SetFillColor(0)
	L_unc.AddEntry(CD_nom, "PF ratio in regions C and D", "PE")
	L_unc.AddEntry(F_CD_nom, "Fit to PF ratio in C and D", "L")
	for p in range(F_CD_nom.GetNpar()):
		tmp_fit = FIT(R+"uncfit_"+str(p))
		CD_nom.Fit(tmp_fit, "EM0R")
		tmp_fit_u = FIT(R+"uncfit_u_"+str(p))
		tmp_fit_d = FIT(R+"uncfit_d_"+str(p))
		for pp in range(tmp_fit.GetNpar()):
			if pp != p:
				tmp_fit_u.FixParameter(pp, tmp_fit.GetParameter(pp))
				tmp_fit_d.FixParameter(pp, tmp_fit.GetParameter(pp))
		tmp_fit_u.FixParameter(p, tmp_fit.GetParameter(p) + tmp_fit.GetParError(p))
		tmp_fit_d.FixParameter(p, tmp_fit.GetParameter(p) - tmp_fit.GetParError(p))
		CD_nom.Fit(tmp_fit_u, "EM0R")
		CD_nom.Fit(tmp_fit_d, "EM0R")
		GoodPlotFormat(tmp_fit_u, "thinline", ROOT.kRed+p, 2+p)
		GoodPlotFormat(tmp_fit_d, "thinline", ROOT.kRed+p, 2+p)
		L_unc.AddEntry(tmp_fit_u, "#pm#sigma on par "+str(p+1)+" (correlations ignored)", "F")
		U_fits.append(tmp_fit_u)
		D_fits.append(tmp_fit_d)

	GoodPlotFormat(CD_nom, "markers", ROOT.kBlue, 20)

	C_unc = ROOT.TCanvas()
	C_unc.cd()
	ROOT.gPad.SetTicks(1,1)
	CD_nom.Draw("e")
	F_CD_nom.Draw("same")
	for f in U_fits:
		f.Draw("same")
	for f in D_fits:
		f.Draw("same")

	L_unc.Draw("same")
	AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
	C_unc.Print("results/"+NAME+"/FIT_"+R+"_unc.root")
	C_unc.Print("results/"+NAME+"/FIT_"+R+"_unc.png")
	####

	# Save for future use:
	outF.cd()

	for f in U_fits:
		f.Write()
	for f in D_fits:
		f.Write()
	outF.Save()
	outF.Write()

GoodPlotFormat(CompareFits[0], "thickline", ROOT.kBlue, 1)
GoodPlotFormat(CompareFits[1], "thickline", ROOT.kGreen, 1)
GoodPlotFormat(CompareFits[2], "thickline", ROOT.kBlack, 1)
GoodPlotFormat(CompareFits[3], "thickline", ROOT.kRed, 1)


C_cmp = ROOT.TCanvas()
C_cmp.cd()
CompareFits[0].Draw("")
for f in CompareFits: f.Draw("same")
ROOT.gPad.SetTicks(1,1)
CompareLeg.Draw("same")
AddCMSLumi(ROOT.gPad, LUMI, cmsextra)
C_cmp.Print("results/"+NAME+"/FIT_comp.root")
C_cmp.Print("results/"+NAME+"/FIT_comp.png")

outF.Close()


		
		
		
		
		
		
		
