import ROOT
from ROOT import *
import numpy
import math
import sys
import array

RDF = ROOT.ROOT.RDataFrame

# -------------------------- #
# Takes either one array or histograms or a set of histograms as input.
# Will calculate the maximum across all histograms and sets the max to 35% more than that for all histograms.
# returns this maximum (as a float)
def FindAndSetMax(*args):
	if len(args) == 1: args = args[0]
	maximum = 0.0
	for i in args:
		i.SetStats(0)
		t = i.GetMaximum()
		if t > maximum:
			maximum = t
	for j in args:
		j.GetYaxis().SetRangeUser(0,maximum*1.35)#should be 1.35 (below as well)
		j.SetLineWidth(2)
	return maximum*1.35
# -------------------------- #

# -------------------------- #
# Takes either one array or histograms or a set of histograms as input.
# Will calculate the minimum and maximum across all histograms and sets them to 35% more than that for all histograms.
# returns this maximum (as a float)
def FindAndSetMinAndMax(*args):
	if len(args) == 1: args = args[0]
	maximum = 0.0
	minimum = 9999999999.
	for i in args:
		i.SetStats(0)
		t = i.GetMaximum()
		tm = i.GetMinimum()
		if t > maximum:
			maximum = t
		if tm < minimum:
			minimum = tm
	for j in args:
		if minimum < 0.: newmin = minimum * 1.35
		else: newmin = 0.65 * minimum
		j.GetYaxis().SetRangeUser(newmin,maximum*1.35)#should be 1.35 (below as well)
		j.SetLineWidth(2)
	return (newmin, maximum*1.35)
# -------------------------- #

# -------------------------- #
# Handy little script for color/line/fill/point/etc...
def GoodPlotFormat(H, *args):
	try: H.SetStats(0)
	except: print " ------------ [  No stats box found!  ]"
	if args[0] == 'thickline':
		H.SetLineColor(args[1])
		H.SetLineWidth(2)
	if args[0] == 'thinline':
		H.SetLineColor(args[1])
		H.SetLineWidth(1)
		H.SetLineStyle(args[2])
	if args[0] == 'fill':
		H.SetLineColor(args[1])
		H.SetFillColor(args[1])
		H.SetFillStyle(args[2])
	if args[0] == 'markers':
		H.SetLineColor(args[1])
		H.SetMarkerColor(args[1])
		H.SetMarkerStyle(args[2])
	H.GetXaxis().SetTitleSize(0.04)
# -------------------------- #

# -------------------------- #
# Takes a 2D histogram as input and converts it to a 1D histogram.
# X-axis will be the "bin number" spanning all bins in the 2D histogram
# Bin numbering goes according to ROOTs internal bin numbers
# Returns the 1D histogram
def Unroll(H):
	nxb = H.GetNbinsX()
	nyb = H.GetNbinsY()
	oH = TH1F(H.GetName()+"_1d", ";bin # ; events", nxb*nyb, 0.5, (nxb*nyb)+0.5)
	oH.SetStats(0)
	for i in range(0,(nyb)):
		for j in range(0,(nxb)):
			k = H.GetBin(i+1,j+1)
			index = oH.FindBin(1 + j + i*nxb)
			oH.SetBinContent(index, H.GetBinContent(k))
			oH.SetBinError(index, H.GetBinError(k))

	return oH
# -------------------------- #

# -------------------------- #
# Returns the profile at a given cut from a given TH2F.
def GetQuantileProfiles(Th2f, cut):
		q1 = []
		nxbins = Th2f.GetXaxis().GetNbins();
		xlo = Th2f.GetXaxis().GetBinLowEdge(1);
		xhi = Th2f.GetXaxis().GetBinUpEdge(Th2f.GetXaxis().GetNbins() );
		for i in range(nxbins):
				H = Th2f.ProjectionY("ProjY"+str(i),i+1,i+1)
				probSum = array.array('d', [cut])
				q = array.array('d', [0.0]*len(probSum))
				H.GetQuantiles(len(probSum), q, probSum)
				q1.append(q[0])
		H1 = TH1F("Qprof"+str(cut), "", nxbins,xlo,xhi)
		for i in range(nxbins):
				H1.SetBinContent(i+1,q1[i])
		return H1
# -------------------------- #

# -------------------------- #
# Adds the CMS luminosity to the gPad
def AddCMSLumi(pad, fb, extra):
	cmsText     = "CMS " + extra;
	cmsTextFont   = 61  
	lumiTextSize     = 0.45
	lumiTextOffset   = 0.15
	cmsTextSize      = 0.5
	cmsTextOffset    = 0.15
	H = pad.GetWh()
	W = pad.GetWw()
	l = pad.GetLeftMargin()
	t = pad.GetTopMargin()
	r = pad.GetRightMargin()
	b = pad.GetBottomMargin()
	e = 0.025
	pad.cd()
	lumiText = str(fb)+" fb^{-1} (13 TeV)"
	latex = TLatex()
	latex.SetNDC()
	latex.SetTextAngle(0)
	latex.SetTextColor(kBlack)	
	extraTextSize = 0.76*cmsTextSize
	latex.SetTextFont(42)
	latex.SetTextAlign(31) 
	latex.SetTextSize(lumiTextSize*t)	
	latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
	pad.cd()
	latex.SetTextFont(cmsTextFont)
	latex.SetTextSize(cmsTextSize*t)
	latex.SetTextAlign(11)
	latex.DrawLatex(0.1265, 0.825, cmsText)
	pad.Update()
# -------------------------- #

# -------------------------- #
# Turns a ROOT.TGraphAsym (TG) into a histogram for easier plotting an manipulation. The template can be used to convet to bins in some
# other value (instead of just point number). Needs a name for root bookkeeping.
def convertAsymGraph(TG, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,0.)
	for i in range(TG.GetN()):
		Hist.SetBinContent(i+1,TG.GetY()[i]*(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
	Hist.Sumw2()
	return Hist
# -------------------------- #

# -------------------------- #
# Turns a histogram with n bins into a similar histogram with n bins, but uses the binning values of tempalte. Needs a name for root bookkeeping.
def convertBinNHist(H, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,H.GetBinContent(i))
		Hist.SetBinError(i,H.GetBinError(i))
	return Hist
# -------------------------- #

# -------------------------- #
# Takes a histogram and returns two histograms which are the up and down errors. Needs a name to ensure no root funky business.
def GetErrHists(H, name):
	Up = H.Clone(name+"_up")
	Down = H.Clone(name+"_down")
	for i in range(1,H.GetNbinsX()+1):
		Up.SetBinContent(i, H.GetBinContent(i)+H.GetBinError(i))
		Down.SetBinContent(i, max(0.,H.GetBinContent(i)-H.GetBinError(i)))
	return Up, Down
# -------------------------- #

# -------------------------- #
# A series of nice combinations of lines/colors for plotting multiple lines in situations where I don't know how many I'm going to have:
ColLine = 	[
				[2,1],[4,2],[6,3],[8,1],[12,2],[28,3],
				[2,2],[4,3],[6,1],[8,2],[12,3],[28,1],
				[2,3],[4,1],[6,2],[8,3],[12,1],[28,2]
			]
# -------------------------- #