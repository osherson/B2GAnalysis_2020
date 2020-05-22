#
import os
import ROOT
from ROOT import *
from array import array
import math
import numpy
from math import *
import sys
import glob
import csv
import XRootD
from pyxrootd import client
from FWCore.PythonUtilities.LumiList import LumiList


class picoTree:
    def __init__(self, name, inputFile, weight, folder, mc, year):
        self.year = year
        self.mc = mc == "MC"
        self.weight = weight
        self.__book__(name, folder)
        self.TrigFile = TFile("TriggerScaleFactors.root")
        self.TrigHist = self.TrigFile.Get(year)
        self.Fill(inputFile)
        self.O.cd()
        self.O.Write()
        self.O.Close()
    def __book__(self, name, folder):
        self.O = TFile(folder+"/"+name+".root", "recreate")
        self.O.cd()
        self.T_nominal = TTree("tree_nominal", "tree_nominal")
        if self.mc:
			self.T_jesCorr_up = TTree("tree_jesCorr_up", "tree_jesCorr_up")
			self.T_jesCorr_down = TTree("tree_jesCorr_down", "tree_jesCorr_down")
			self.T_jesUnCorr_up = TTree("tree_jesUnCorr_up", "tree_jesUnCorr_up")
			self.T_jesUnCorr_down = TTree("tree_jesUnCorr_down", "tree_jesUnCorr_down")
			self.T_jer_up = TTree("tree_jer_up", "tree_jer_up")
			self.T_jer_down = TTree("tree_jer_down", "tree_jer_down")
			# MC ONLY VARIABLES
			self.W = array('f', [0.0])
			self.AddBranch('weight_xsN', self.W)
			self.WbbMM = array('f', [0.0])
			self.AddBranch('weight_BBMM', self.WbbMM)
			self.WbbMMu = array('f', [0.0])
			self.AddBranch('weight_BBMM_up', self.WbbMMu)
			self.WbbMMd = array('f', [0.0])
			self.AddBranch('weight_BBMM_dn', self.WbbMMd)
			self.WbbMT = array('f', [0.0])
			self.AddBranch('weight_BBMT', self.WbbMT)
			self.WbbMTu = array('f', [0.0])
			self.AddBranch('weight_BBMT_up', self.WbbMTu)
			self.WbbMTd = array('f', [0.0])
			self.AddBranch('weight_BBMT_dn', self.WbbMTd)
			self.WbbTT = array('f', [0.0])
			self.AddBranch('weight_BBTT', self.WbbTT)
			self.WbbTTu = array('f', [0.0])
			self.AddBranch('weight_BBTT_up', self.WbbTTu)
			self.WbbTTd = array('f', [0.0])
			self.AddBranch('weight_BBTT_dn', self.WbbTTd)
			self.Wpu = array('f', [0.0])
			self.AddBranch('weight_PU', self.Wpu)
			self.Wpuu = array('f', [0.0])
			self.AddBranch('weight_PU_up', self.Wpuu)
			self.Wpud = array('f', [0.0])
			self.AddBranch('weight_PU_dn', self.Wpud)
			self.WT = array('f', [0.0])
			self.AddBranch('weight_trig', self.WT)
			self.WTup = array('f', [0.0])
			self.AddBranch('weight_trig_up', self.WTup)
			self.WTdn = array('f', [0.0])
			self.AddBranch('weight_trig_dn', self.WTdn)
			self.evt_ttRW = array('f', [0.0])
			self.AddBranch('evt_ttRW', self.evt_ttRW)
			self.PDFup = array('f', [0.0])
			self.AddBranch('weight_pdf_up', self.PDFup)
			self.PDFdn = array('f', [0.0])
			self.AddBranch('weight_pdf_dn', self.PDFdn)
        # EVENT VARIABLES
        self.evt_XM = array('f', [-1.0])
        self.AddBranch('evt_XM', self.evt_XM)
        self.evt_HT = array('f', [-1.0])
        self.AddBranch('evt_HT', self.evt_HT)
        self.evt_aM = array('f', [-1.0])
        self.AddBranch('evt_aM', self.evt_aM)
        self.evt_Masym = array('f', [-1.0])
        self.AddBranch('evt_Masym', self.evt_Masym)
        self.evt_Deta = array('f', [-1.0])
        self.AddBranch('evt_Deta', self.evt_Deta)
        self.evt_Dphi = array('f', [-1.0])
        self.AddBranch('evt_Dphi', self.evt_Dphi)
        self.evt_DR = array('f', [-1.0])
        self.AddBranch('evt_DR', self.evt_DR)
        # SINGLE JET VARIABLES	
        self.J1pt = array('f', [-1.0])
        self.AddBranch('J1pt', self.J1pt)
        self.J1eta = array('f', [-1.0])
        self.AddBranch('J1eta', self.J1eta)
        self.J1phi = array('f', [-1.0])
        self.AddBranch('J1phi', self.J1phi)
        self.J1SDM = array('f', [-1.0])
        self.AddBranch('J1SDM', self.J1SDM)
        self.J1dbtag = array('f', [-1.0])
        self.AddBranch('J1dbtag', self.J1dbtag)
        self.J1DeepBBtag = array('f', [-1.0])
        self.AddBranch('J1DeepBBtag', self.J1DeepBBtag)
        self.J1DeeptagMD_Hbb = array('f', [-1.0])
        self.AddBranch('J1DeeptagMD_Hbb', self.J1DeeptagMD_Hbb)
        self.J2pt = array('f', [-1.0])
        self.AddBranch('J2pt', self.J2pt)
        self.J2eta = array('f', [-1.0])
        self.AddBranch('J2eta', self.J2eta)
        self.J2phi = array('f', [-1.0])
        self.AddBranch('J2phi', self.J2phi)
        self.J2SDM = array('f', [-1.0])
        self.AddBranch('J2SDM', self.J2SDM)
        self.J2dbtag = array('f', [-1.0])
        self.AddBranch('J2dbtag', self.J2dbtag)
        self.J2DeepBBtag = array('f', [-1.0])
        self.AddBranch('J2DeepBBtag', self.J2DeepBBtag)
        self.J2DeeptagMD_Hbb = array('f', [-1.0])
        self.AddBranch('J2DeeptagMD_Hbb', self.J2DeeptagMD_Hbb)

    def Fill(self, inputFile):
        print "Filling from " + inputFile
        F = TFile(inputFile)
        self.T = F.Get("Events")
        for e in self.T:#range(self.T.GetEntries()):
            #self.T.GetEvent(e)
            self.e = e
            if not min(self.T.FatJet_msoftdrop_nom[0], self.T.FatJet_msoftdrop_nom[1]) > 0.: continue
            if self.year == "2016": IDCUT = 2
            if self.year == "2017": IDCUT = 5
            if self.year == "2018": IDCUT = 5
            if not min(self.T.FatJet_jetId[0], self.T.FatJet_jetId[1]) > IDCUT: continue
            self.HT = 0.
            for j in range(self.T.nJet):
                if self.T.Jet_pt[j] > 50. and math.fabs(self.T.Jet_eta[j]) < 2.4:
                    self.HT += self.T.Jet_pt[j]
            self.J1 = TLorentzVector()
            self.J2 = TLorentzVector()
            self.FillJetVars(self.T.FatJet_pt_nom, self.T.FatJet_mass_nom, self.T.FatJet_msoftdrop_nom, self.T_nominal, self.T.Jet_pt_nom)
            if self.mc:
                self.W[0] = float(self.weight)
                self.Wpu[0] = self.T.puWeight
                if self.T.puWeight > 0:
		            self.Wpuu[0] = self.T.puWeightUp/self.T.puWeight
		            self.Wpud[0] = self.T.puWeightDown/self.T.puWeight
                m1, m2, t1, t2, m1u, m1d, m2u, m2d, t1u, t1d, t2u, t2d = 0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.
                if self.year == "2016":
               		if self.T.FatJet_pt[0] > 350 and self.T.FatJet_pt[0] < 850:
               			m1 = 1.01
               			m1d = (1.01-0.06)
               			m1u = (1.01+0.10)
               			t1 = 0.95
               			t1d = (0.95-0.07)
               			t1u = (0.95+0.13)
               		else:
               			m1 = 1.01
               			m1d = (1.01-0.12)
               			m1u = (1.01+0.20)
               			t1 = 0.95
               			t1d = (0.95-0.14)
               			t1u = (0.95+0.26)
               		if self.T.FatJet_pt[1] > 350 and self.T.FatJet_pt[1] < 850:
               			m2 = 1.01
               			m2d = (1.01-0.06)
               			m2u = (1.01+0.10)
               			t2 = 0.95
               			t2d = (0.95-0.07)
               			t2u = (0.95+0.13)
               		else:
               			m2 = 1.01
               			m2d = (1.01-0.12)
               			m2u = (1.01+0.20)
               			t2 = 0.95
               			t2d = (0.95-0.14)
               			t2u = (0.95+0.26)
            	if self.year == "2017":
               		if self.T.FatJet_pt[0] > 250 and self.T.FatJet_pt[0] <= 350:
               			m1 = 0.93
               			m1d = (0.93-0.04)
               			m1u = (0.93+0.03)
               			t1 = 0.85
               			t1d = (0.85-0.04)
               			t1u = (0.85+0.04)
               		elif self.T.FatJet_pt[0] > 350 and self.T.FatJet_pt[0] < 840:
               			m1 = 0.9
               			m1d = (0.9-0.08)
               			m1u = (0.9+0.04)
               			t1 = 0.8
               			t1d = (0.8-0.07)
               			t1u = (0.8+0.04)
               		else:
               			m1 = 0.9
               			m1d = (0.9-0.16)
               			m1u = (0.9+0.08)
               			t1 = 0.8
               			t1d = (0.8-0.14)
               			t1u = (0.8+0.08)
               		if self.T.FatJet_pt[1] > 250 and self.T.FatJet_pt[1] <= 350:
               			m2 = 0.93
               			m2d = (0.93-0.04)
               			m2u = (0.93+0.03)
               			t2 = 0.85
               			t2d = (0.85-0.04)
               			t2u = (0.85+0.04)
               		elif self.T.FatJet_pt[1] > 350 and self.T.FatJet_pt[1] < 840:
               			m2 = 0.9
               			m2d = (0.9-0.08)
               			m2u = (0.9+0.04)
               			t2 = 0.8
               			t2d = (0.8-0.07)
               			t2u = (0.8+0.04)
               		else:
               			m2 = 0.9
               			m2d = (0.9-0.16)
               			m2u = (0.9+0.08)
               			t2 = 0.8
               			t2d = (0.8-0.14)
               			t2u = (0.8+0.08)
            	if self.year == "2018":
               		if self.T.FatJet_pt[0] > 250 and self.T.FatJet_pt[0] <= 350:
               			m1 = 0.93
               			m1d = (0.93-0.05)
               			m1u = (0.93+0.05)
               			t1 = 0.89
               			t1d = (0.89-0.08)
               			t1u = (0.89+0.04)
               		elif self.T.FatJet_pt[0] > 350 and self.T.FatJet_pt[0] < 850:
               			m1 = 0.89
               			m1d = (0.89-0.06)
               			m1u = (0.89+0.04)
               			t1 = 0.84
               			t1d = (0.84-0.05)
               			t1u = (0.84+0.05)
               		else:
               			m1 = 0.89
               			m1d = (0.89-0.12)
               			m1u = (0.89+0.08)
               			t1 = 0.84
               			t1d = (0.84-0.1)
               			t1u = (0.84+0.1)
               		if self.T.FatJet_pt[1] > 250 and self.T.FatJet_pt[1] <= 350:
               			m2 = 0.93
               			m2d = (0.93-0.05)
               			m2u = (0.93+0.05)
               			t2 = 0.89
               			t2d = (0.89-0.08)
               			t2u = (0.89+0.04)
               		elif self.T.FatJet_pt[1] > 350 and self.T.FatJet_pt[1] < 850:
               			m2 = 0.89
               			m2d = (0.89-0.08)
               			m2u = (0.89+0.04)
               			t2 = 0.84
               			t2d = (0.84-0.05)
               			t2u = (0.84+0.05)
               		else:
               			m2 = 0.89
               			m2d = (0.89-0.12)
               			m2u = (0.89+0.08)
               			t2 = 0.84
               			t2d = (0.84-0.1)
               			t2u = (0.84+0.1)
                self.WbbMM[0] = m1*m2
                self.WbbMMu[0] = m1u*m2u
                self.WbbMMd[0] = m1d*m2d
                self.WbbMT[0] = t1*m2
                self.WbbMTu[0] = t1u*m2u
                self.WbbMTd[0] = t1d*m2d
                self.WbbTT[0] = t1*t2
                self.WbbTTu[0] = t1u*t2u
                self.WbbTTd[0] = t1d*t1d
                ttbarHT = 0.0
                for gp in range(self.T.nGenPart):
                    if math.fabs(self.T.GenPart_pdgId[gp]) == 6 and self.T.GenPart_status[gp] == 62:
                        ttbarHT += self.T.GenPart_pt[gp]
                self.evt_ttRW[0] = ttbarHT
                self.WT[0] = self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT))
                if self.WT[0] > 0:
		            self.WTup[0] = min(1.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) + self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))/self.WT[0]
		            self.WTdn[0] = max(0.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) - self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))/self.WT[0]
                self.PDFup[0] = 1 + numpy.std(self.T.LHEPdfWeight)
                self.PDFdn[0] = 1 - numpy.std(self.T.LHEPdfWeight)
                Kin_jesCorrUp = self.GetJESComp("C", "Up")
                Kin_jesCorrDown = self.GetJESComp("C", "Down")
                Kin_jesUnCorrUp = self.GetJESComp("U", "Up")
                Kin_jesUnCorrDown = self.GetJESComp("U", "Down")

                self.FillJetVars(Kin_jesCorrUp[0], Kin_jesCorrUp[1], Kin_jesCorrUp[2], self.T_jesCorr_up, Kin_jesCorrUp[3])
                self.FillJetVars(Kin_jesCorrDown[0], Kin_jesCorrDown[1], Kin_jesCorrDown[2], self.T_jesCorr_down, Kin_jesCorrDown[3])
                self.FillJetVars(Kin_jesUnCorrUp[0], Kin_jesUnCorrUp[1], Kin_jesUnCorrUp[2], self.T_jesUnCorr_up, Kin_jesUnCorrUp[3])
                self.FillJetVars(Kin_jesUnCorrDown[0], Kin_jesUnCorrDown[1], Kin_jesUnCorrDown[2], self.T_jesUnCorr_down, Kin_jesUnCorrUp[3])
                self.FillJetVars(self.T.FatJet_pt_jerUp, self.T.FatJet_mass_jerUp, self.T.FatJet_msoftdrop_jerUp, self.T_jer_up, self.T.Jet_pt_jerUp)
                self.FillJetVars(self.T.FatJet_pt_jerDown, self.T.FatJet_mass_jerDown, self.T.FatJet_msoftdrop_jerDown, self.T_jer_down, self.T.Jet_pt_jerDown)

    def GET(self, B, i):
		return getattr(self.e, B)[i]
		
    def GetCorrectedVal(self, var, i, W, C):
		delta = 0.
		if C == "C":
			Sys = [
                    ["AbsoluteMPFBias", 1.],
                    ["AbsoluteScale", 1.],
                    ["FlavorQCD", 1.],
                    ["Fragmentation", 1.],
                    ["PileUpDataMC", 2.],
                    ["PileUpPtBB", 2.],
                    ["PileUpPtEC1", 2.],
                    ["PileUpPtEC2", 2.],
                    ["PileUpPtHF", 2.],
                    ["PileUpPtRef", 2.],
                    ["RelativeFSR", 2.],
                    ["RelativeJERHF", 2.],
                    ["RelativePtBB", 2.],
                    ["RelativePtHF", 2.],
                    ["RelativeBal", 2.],
                    ["SinglePionECAL", 1.],
                    ["SinglePionHCAL", 1.]
			]
			for S in Sys:
				delta += ((self.GET(var+"_jes"+S[0]+W, i) - self.GET(var+"_nom", i))/(S[1]*self.GET(var+"_nom", i)))**2
		if C == "U":
			Sys = [
                    ["AbsoluteStat", 1.],
                    ["PileUpDataMC", 2.],
                    ["PileUpPtBB", 2.],
                    ["PileUpPtEC1", 2.],
                    ["PileUpPtEC2", 2.],
                    ["PileUpPtHF", 2.],
                    ["PileUpPtRef", 2.],
                    ["RelativeFSR", 2.],
                    ["RelativeJERHF", 2.],
                    ["RelativePtBB", 2.],
                    ["RelativePtHF", 2.],
                    ["RelativeBal", 2.],
                    ["RelativeJEREC1", 1.],
                    ["RelativeJEREC2", 1.],
                    ["RelativePtEC1", 1.],
                    ["RelativePtEC2", 1.],
                    ["RelativeSample", 1.],
                    ["RelativeStatEC", 1.],
                    ["RelativeStatFSR", 1.],
                    ["RelativeStatHF", 1.],
                    ["TimePtEta", 1.]
			]
			for S in Sys:
				delta += ((self.GET(var+"_jes"+S[0]+W, i) - self.GET(var+"_nom", i))/(S[1]*self.GET(var+"_nom", i)))**2
		fac = 0.
		if W == "Up": fac = 1 + math.sqrt(delta)
		if W == "Down": fac = 1 - math.sqrt(delta)
		return self.GET(var+"_nom", i) * (fac)
		
    def GetJESComp(self, corr, which):
    	PT4 = []
        PT = []
        MASS = []
        SDM = []
        for jet in [0,1]:
			PT.append(self.GetCorrectedVal("FatJet_pt", jet, which, corr))
			MASS.append(self.GetCorrectedVal("FatJet_mass", jet, which, corr))
			SDM.append(self.GetCorrectedVal("FatJet_msoftdrop", jet, which, corr))
        for jet in range(self.T.nJet): 
        	PT4.append(self.GetCorrectedVal("Jet_pt", jet, which, corr))
        return [PT, MASS, SDM, PT4]

    def FillJetVars(self, PT, MASS, SDMASS, B, Jet_pt):
        HT = 0.
        for j in range(self.T.nJet):
        	if (Jet_pt[j] > 50. and math.fabs(self.T.Jet_eta[j]) < 2.4):
        		HT += Jet_pt[j]
        self.J1.SetPtEtaPhiM(PT[0], self.T.FatJet_eta[0], self.T.FatJet_phi[0], MASS[0])
        self.J2.SetPtEtaPhiM(PT[1], self.T.FatJet_eta[1], self.T.FatJet_phi[1], MASS[1])
        self.evt_HT[0] = HT
        self.evt_XM[0] = (self.J1+self.J2).M()
        self.evt_Deta[0] = math.fabs(self.J1.Eta() - self.J2.Eta())
        self.evt_Dphi[0] = math.fabs(self.J1.DeltaPhi(self.J2))
        self.evt_DR[0] = self.J1.DeltaR(self.J2)
        self.evt_Masym[0] = math.fabs(SDMASS[0] - SDMASS[1])/(SDMASS[0] + SDMASS[1])
        self.evt_aM[0] = math.fabs(SDMASS[0] + SDMASS[1])/2.0
        self.J1pt[0] = self.J1.Pt()
        self.J1eta[0] = self.J1.Eta()
        self.J1phi[0] = self.J1.Phi()
        self.J2pt[0] = self.J2.Pt()
        self.J2eta[0] = self.J2.Eta()
        self.J2phi[0] = self.J2.Phi()
        self.J1DeepBBtag[0] = self.T.FatJet_btagDDBvL[0]
        self.J2DeepBBtag[0] = self.T.FatJet_btagDDBvL[1]
        self.J1DeeptagMD_Hbb[0] = self.T.FatJet_deepTagMD_HbbvsQCD[0]
        self.J2DeeptagMD_Hbb[0] = self.T.FatJet_deepTagMD_HbbvsQCD[1]
        self.J1dbtag[0] = self.T.FatJet_btagHbb[0]
        self.J2dbtag[0] = self.T.FatJet_btagHbb[1]
        self.J1SDM[0] = SDMASS[0]
        self.J2SDM[0] = SDMASS[1]
        B.Fill()
    def AddBranch(self, name, obj):
        self.T_nominal.Branch(name, obj, name+"/F")
        if self.mc:
            self.T_jesCorr_up.Branch(name, obj, name+"/F")
            self.T_jesCorr_down.Branch(name, obj, name+"/F")
            self.T_jesUnCorr_up.Branch(name, obj, name+"/F")
            self.T_jesUnCorr_down.Branch(name, obj, name+"/F")
            self.T_jer_up.Branch(name, obj, name+"/F")
            self.T_jer_down.Branch(name, obj, name+"/F")

picoTree(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
