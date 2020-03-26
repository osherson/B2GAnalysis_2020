import ROOT
from ROOT import *
import numpy
import math
import sys
import array
import os
RDF = ROOT.ROOT.RDataFrame

def MakeNBinsFromMinToMax(N,Min,Max): # helper for making large bin arrays makes N bins between Min and Max (same as you're feed to a TH1F)
	BINS = []
	for i in range(N+1):
		BINS.append(Min+(i*(Max-Min)/N))
	return BINS
def convertAsymGraph(TG, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,0.)
	for i in range(TG.GetN()):
		Hist.SetBinContent(i+1,TG.GetY()[i]*(TG.GetErrorXlow(i)+TG.GetErrorXhigh(i)))
		Hist.SetBinError(i+1, TG.GetErrorY(i))
	return Hist
def convertBinNHist(H, template, name):
	Hist = template.Clone(name)
	for i in range(1,Hist.GetNbinsX()+1):
		Hist.SetBinContent(i,H.GetBinContent(i))
		Hist.SetBinError(i,H.GetBinError(i))
	return Hist
def GoodPlotFormat(H, *args): # Handy little script for color/line/fill/point/etc...
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
def AddCMSLumi(pad, fb, extra):
	cmsText     = "CMS " + extra
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
def Template_Replace(F, O, R):
	with open(F, 'r') as file :
		filedata = file.read()
	filedata = filedata.replace(O, R)
	with open(F, 'w') as file:
		file.write(filedata)
def Unroll(H, name):
	nxb = H.GetNbinsX()
	nyb = H.GetNbinsY()
	oH = TH1F(name, ";bin # ; events", nxb*nyb, 1, (nxb*nyb)+1)
	oH.SetStats(0)
	for i in range(0,(nxb)):
		for j in range(0,(nyb)):
			k = H.GetBin(i+1,j+1)
			index = oH.FindBin(1 + j + i*nyb)
			oH.SetBinContent(index, H.GetBinContent(k))
			oH.SetBinError(index, H.GetBinError(k))

	return oH
def Reroll(H, VARS):
	X = TH1F("x_"+H.GetName(), ";"+VARS[2], len(VARS[1])-1, numpy.array(VARS[1]))
	Y = TH1F("y_"+H.GetName(), ";"+VARS[5], len(VARS[4])-1, numpy.array(VARS[4]))
		
	XY = TH2F("xy_"+H.GetName(), ";"+VARS[2]+";"+VARS[5], len(VARS[1])-1, numpy.array(VARS[1]), len(VARS[4])-1, numpy.array(VARS[4]))
	XYe = TH2F("xye_"+H.GetName(), ";"+VARS[2]+";"+VARS[5], len(VARS[1])-1, numpy.array(VARS[1]), len(VARS[4])-1, numpy.array(VARS[4]))

	X.SetStats(0)
	Y.SetStats(0)
	XY.SetStats(0)

	nxb = X.GetNbinsX()
	nyb = Y.GetNbinsX()

	for i in range(0,(nxb)):
		for j in range(0,(nyb)):
			k = XY.GetBin(i+1,j+1)
			index = H.FindBin(1 + j + i*nyb)
			XY.SetBinContent(k, H.GetBinContent(index))
			XY.SetBinError(k, (H.GetBinError(index)))
			XYe.SetBinContent(k, (H.GetBinError(index)))
	X = XY.ProjectionX("px_"+H.GetName(),1,nxb,"e")
	Y = XY.ProjectionY("py_"+H.GetName(),1,nyb,"e")
	return [X,Y,XY, XYe]
def DBBW(H):
	for i in range(1,H.GetNbinsX()+1):
		C = H.GetBinContent(i)
		E = H.GetBinError(i)
		W = H.GetBinWidth(i)
		H.SetBinContent(i, C/W)
		H.SetBinError(i, E/W)	
	return H
