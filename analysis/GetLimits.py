import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

LIM = []

for Sigs in SIG:
	for VAR in EstVars:
		if not VAR[3]: continue
		cardname = VAR[0]+"_"+Sigs[3]
		os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M AsymptoticLimits " + EXTRACOMBINEOPTION)
		F = ROOT.TFile("higgsCombineTest.AsymptoticLimits.mH120.root")
		T = F.Get("limit")
		T.GetEntry(5)
		if not Blind:
			obs = T.limit*Sigs[5]
		else: obs = -1.0
		T.GetEntry(0)
		m2 = T.limit*Sigs[5]
		T.GetEntry(1)
		m1 = T.limit*Sigs[5]
		T.GetEntry(2)
		exp = T.limit*Sigs[5]
		T.GetEntry(3)
		p1 = T.limit*Sigs[5]
		T.GetEntry(4)
		p2 = T.limit*Sigs[5]
		print [cardname, obs, m2, m1, exp, p1, p2]
		LIM.append([cardname, obs, m2, m1, exp, p1, p2])
		os.system("rm *.out")
		os.system("rm *.root")
	for VAR in EstVars2D:
		if not VAR[6]: continue
		cardname = VAR[0]+"_vs_"+VAR[3]+"_"+Sigs[3]
		os.system("combine ../results/"+NAME+"/Card_"+cardname+".txt -M AsymptoticLimits " + EXTRACOMBINEOPTION)
		F = ROOT.TFile("higgsCombineTest.AsymptoticLimits.mH120.root")
		T = F.Get("limit")
		T.GetEntry(5)
		if not Blind:
			obs = T.limit*Sigs[5]
		else: obs = -1.0
		T.GetEntry(0)
		m2 = T.limit*Sigs[5]
		T.GetEntry(1)
		m1 = T.limit*Sigs[5]
		T.GetEntry(2)
		exp = T.limit*Sigs[5]
		T.GetEntry(3)
		p1 = T.limit*Sigs[5]
		T.GetEntry(4)
		p2 = T.limit*Sigs[5]
		print [cardname, obs, m2, m1, exp, p1, p2]
		LIM.append([cardname, obs, m2, m1, exp, p1, p2])
		os.system("rm *.out")
		os.system("rm *.root")

text_file = open("../results/"+NAME+"/LIMITS.txt", "w")
LimUGLYm2 = ROOT.TH1F("LimUGLYm2"+NAME, "", len(LIM), 0, len(LIM))
LimUGLYm1 = ROOT.TH1F("LimUGLYm1"+NAME, "", len(LIM), 0, len(LIM))
LimUGLYp1 = ROOT.TH1F("LimUGLYp1"+NAME, "", len(LIM), 0, len(LIM))
LimUGLYp2 = ROOT.TH1F("LimUGLYp2"+NAME, "", len(LIM), 0, len(LIM))
LimUGLYe = ROOT.TH1F("LimUGLYe"+NAME, "", len(LIM), 0, len(LIM))
LimUGLYo = ROOT.TH1F("LimUGLYo"+NAME, "", len(LIM), 0, len(LIM))


for l in LIM:
	i = LIM.index(l)+1
	text_file.write(l[0] + ", %f ,%f, %f ,%f, %f ,%f\n"%(l[1],l[2],l[3],l[4],l[5],l[6]))
	LimUGLYp2.GetXaxis().SetBinLabel(i, l[0])
	LimUGLYp2.SetBinContent(i, l[6])
	LimUGLYp1.SetBinContent(i, l[5])
	LimUGLYe.SetBinContent(i, l[4])
	LimUGLYm1.SetBinContent(i, l[3])
	LimUGLYm2.SetBinContent(i, l[2])
	LimUGLYo.SetBinContent(i, l[1])
	LimUGLYo.SetBinError(i, 0.00001)

FindAndSetMax(LimUGLYo, LimUGLYp2)





LimUGLYp2.GetYaxis().SetTitle("#sigma (fb)")
LimUGLYp2.SetFillColor(ROOT.kYellow)
LimUGLYp2.SetLineColor(ROOT.kYellow)
LimUGLYp1.SetFillColor(ROOT.kGreen)
LimUGLYp1.SetLineColor(ROOT.kGreen)
LimUGLYe.SetLineColor(ROOT.kBlack)
LimUGLYe.SetFillColor(ROOT.kGreen)
LimUGLYe.SetLineStyle(2)
LimUGLYm1.SetFillColor(ROOT.kYellow)
LimUGLYm1.SetLineColor(ROOT.kYellow)
LimUGLYm2.SetFillColorAlpha(ROOT.kWhite, 0.0)
LimUGLYm2.SetLineColor(ROOT.kWhite)
LimUGLYo.SetMarkerStyle(20)


C_Lim = ROOT.TCanvas()
C_Lim.cd()
ROOT.gStyle.SetErrorX(0.00001)
LimUGLYp2.Draw("hist")
LimUGLYp1.Draw("histsame")
LimUGLYe.Draw("histsame")
LimUGLYm1.Draw("histsame")
LimUGLYm2.Draw("histsame")
LimUGLYo.Draw("esame")
ROOT.gPad.RedrawAxis()
C_Lim.Print("../results/"+NAME+"/"+"LIMITS.root")
C_Lim.Print("../results/"+NAME+"/"+"LIMITS.png")

