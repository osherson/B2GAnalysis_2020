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
            self.T_jms_up = TTree("tree_jms_up", "tree_jms_up")
            self.T_jms_down = TTree("tree_jms_down", "tree_jms_down")
            self.T_jmr_up = TTree("tree_jmr_up", "tree_jmr_up")
            self.T_jmr_down = TTree("tree_jmr_down", "tree_jmr_down")
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
        for e in range(self.T.GetEntries()):
            self.T.GetEvent(e)
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
            self.FillJetVars(self.T.FatJet_pt_nom, self.T.FatJet_mass_nom, self.T.FatJet_msoftdrop_nom, self.T_nominal)
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
               		if self.T.FatJet_pt[0] > 350 and self.T.FatJet_pt[0] < 840:
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
               		if self.T.FatJet_pt[1] > 350 and self.T.FatJet_pt[1] < 840:
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
               		if self.T.FatJet_pt[0] > 350 and self.T.FatJet_pt[0] < 850:
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
               		if self.T.FatJet_pt[1] > 350 and self.T.FatJet_pt[1] < 850:
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
                self.WTup[0] = min(1.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) + self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))
                self.WTdn[0] = max(0.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) - self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))
                self.PDFup[0] = 1 + numpy.std(self.T.LHEPdfWeight)
                self.PDFdn[0] = 1 - numpy.std(self.T.LHEPdfWeight)
                Kin_jesCorrUp = self.GetJESComp("C", "up")
                Kin_jesCorrDown = self.GetJESComp("C", "down")
                Kin_jesUnCorrUp = self.GetJESComp("U", "up")
                Kin_jesUnCorrDown = self.GetJESComp("U", "down")
                self.FillJetVars(Kin_jesCorrUp[0], Kin_jesCorrUp[1], Kin_jesCorrUp[2], self.T_jesCorr_up)
                self.FillJetVars(Kin_jesCorrDown[0], Kin_jesCorrDown[1], Kin_jesCorrDown[2], self.T_jesCorr_down)
                self.FillJetVars(Kin_jesUnCorrUp[0], Kin_jesUnCorrUp[1], Kin_jesUnCorrUp[2], self.T_jesUnCorr_up)
                self.FillJetVars(Kin_jesUnCorrDown[0], Kin_jesUnCorrDown[1], Kin_jesUnCorrDown[2], self.T_jesUnCorr_down)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmsUp, self.T.FatJet_msoftdrop_jmsUp, self.T_jms_up)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmsDown, self.T.FatJet_msoftdrop_jmsDown, self.T_jms_down)
                self.FillJetVars(self.T.FatJet_pt_jerUp, self.T.FatJet_mass_jerUp, self.T.FatJet_msoftdrop_jerUp, self.T_jer_up)
                self.FillJetVars(self.T.FatJet_pt_jerDown, self.T.FatJet_mass_jerDown, self.T.FatJet_msoftdrop_jerDown, self.T_jer_down)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmrUp, self.T.FatJet_msoftdrop_jmrUp, self.T_jmr_up)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmrDown, self.T.FatJet_msoftdrop_jmrDown, self.T_jmr_down)

    def GetJESComp(self, corr, which):
        PT = []
        MASS = []
        SDM = []
        for jet in [0,1]:
            scale = 0.
            pt = 0.
            mass = 0.
            sdm = 0.
            if which == "up":
                if corr == "C":
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteMPFBiasUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteMPFBiasUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteMPFBiasUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteScaleUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteScaleUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteScaleUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesFlavorQCDUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesFlavorQCDUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesFlavorQCDUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesFragmentationUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesFragmentationUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesFragmentationUp[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesPileUpDataMCUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpDataMCUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpDataMCUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtBBUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtBBUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtBBUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC1Up[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC1Up[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC1Up[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC2Up[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC2Up[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC2Up[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtRefUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtRefUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtRefUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeFSRUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeFSRUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeFSRUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeJERHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeJERHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeJERHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtBBUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtBBUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtBBUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeBalUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeBalUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeBalUp[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesSinglePionECALUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesSinglePionECALUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesSinglePionECALUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesSinglePionHCALUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesSinglePionHCALUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesSinglePionHCALUp[jet]
                    scale += 2.
                else:
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteStatUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteStatUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteStatUp[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesPileUpDataMCUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpDataMCUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpDataMCUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtBBUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtBBUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtBBUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC1Up[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC1Up[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC1Up[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC2Up[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC2Up[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC2Up[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtRefUp[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtRefUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtRefUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeFSRUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeFSRUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeFSRUp[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeJEREC1Up[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeJEREC1Up[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeJEREC1Up[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeJEREC2Up[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeJEREC2Up[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeJEREC2Up[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesRelativeJERHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeJERHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeJERHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtBBUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtBBUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtBBUp[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativePtEC1Up[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativePtEC1Up[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativePtEC1Up[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativePtEC2Up[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativePtEC2Up[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativePtEC2Up[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesRelativePtHFUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtHFUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtHFUp[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeBalUp[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeBalUp[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeBalUp[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeSampleUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeSampleUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeSampleUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatECUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatECUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatECUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatFSRUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatFSRUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatFSRUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatHFUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatHFUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatHFUp[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesTimePtEtaUp[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesTimePtEtaUp[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesTimePtEtaUp[jet]
                    scale += 2.
            else:
                if corr == "C":
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteMPFBiasDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteMPFBiasDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteMPFBiasDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteScaleDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteScaleDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteScaleDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesFlavorQCDDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesFlavorQCDDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesFlavorQCDDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesFragmentationDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesFragmentationDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesFragmentationDown[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesPileUpDataMCDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpDataMCDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpDataMCDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtBBDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtBBDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtBBDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC1Down[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC1Down[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC1Down[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC2Down[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC2Down[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC2Down[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtRefDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtRefDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtRefDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeFSRDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeFSRDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeFSRDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeJERHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeJERHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeJERHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtBBDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtBBDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtBBDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeBalDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeBalDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeBalDown[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesSinglePionECALDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesSinglePionECALDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesSinglePionECALDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesSinglePionHCALDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesSinglePionHCALDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesSinglePionHCALDown[jet]
                    scale += 2.
                else:
                    pt = pt + 2.*self.T.FatJet_pt_jesAbsoluteStatDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesAbsoluteStatDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesAbsoluteStatDown[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesPileUpDataMCDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpDataMCDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpDataMCDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtBBDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtBBDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtBBDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC1Down[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC1Down[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC1Down[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtEC2Down[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtEC2Down[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtEC2Down[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesPileUpPtRefDown[jet]
                    mass = mass + self.T.FatJet_mass_jesPileUpPtRefDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesPileUpPtRefDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeFSRDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeFSRDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeFSRDown[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeJEREC1Down[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeJEREC1Down[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeJEREC1Down[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeJEREC2Down[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeJEREC2Down[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeJEREC2Down[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesRelativeJERHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeJERHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeJERHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativePtBBDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtBBDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtBBDown[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativePtEC1Down[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativePtEC1Down[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativePtEC1Down[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativePtEC2Down[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativePtEC2Down[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativePtEC2Down[jet]
                    scale += 2.
                    pt = pt + self.T.FatJet_pt_jesRelativePtHFDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativePtHFDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativePtHFDown[jet]
                    scale += 1.
                    pt = pt + self.T.FatJet_pt_jesRelativeBalDown[jet]
                    mass = mass + self.T.FatJet_mass_jesRelativeBalDown[jet]
                    sdm = sdm + self.T.FatJet_msoftdrop_jesRelativeBalDown[jet]
                    scale += 1.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeSampleDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeSampleDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeSampleDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatECDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatECDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatECDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatFSRDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatFSRDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatFSRDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesRelativeStatHFDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesRelativeStatHFDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesRelativeStatHFDown[jet]
                    scale += 2.
                    pt = pt + 2.*self.T.FatJet_pt_jesTimePtEtaDown[jet]
                    mass = mass + 2.*self.T.FatJet_mass_jesTimePtEtaDown[jet]
                    sdm = sdm + 2.*self.T.FatJet_msoftdrop_jesTimePtEtaDown[jet]
                    scale += 2.
            PT.append(pt/scale)
            MASS.append(mass/scale)
            SDM.append(sdm/scale)
        return [PT, MASS, SDM]

    def FillJetVars(self, PT, MASS, SDMASS, B):
        self.J1.SetPtEtaPhiM(PT[0], self.T.FatJet_eta[0], self.T.FatJet_phi[0], MASS[0])
        self.J2.SetPtEtaPhiM(PT[1], self.T.FatJet_eta[1], self.T.FatJet_phi[1], MASS[1])
        self.evt_HT[0] = self.HT
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
            self.T_jms_up.Branch(name, obj, name+"/F")
            self.T_jms_down.Branch(name, obj, name+"/F")
            self.T_jmr_up.Branch(name, obj, name+"/F")
            self.T_jmr_down.Branch(name, obj, name+"/F")


picoTree(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
