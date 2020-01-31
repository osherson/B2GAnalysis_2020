#
import os
import ROOT
from ROOT import *
from array import array
import math
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
            self.T_jes_up = TTree("tree_jes_up", "tree_jes_up")
            self.T_jes_down = TTree("tree_jes_down", "tree_jes_down")
            self.T_jer_up = TTree("tree_jer_up", "tree_jer_up")
            self.T_jer_down = TTree("tree_jer_down", "tree_jer_down")
            self.T_jms_up = TTree("tree_jms_up", "tree_jms_up")
            self.T_jms_down = TTree("tree_jms_down", "tree_jms_down")
            self.T_jmr_up = TTree("tree_jmr_up", "tree_jmr_up")
            self.T_jmr_down = TTree("tree_jmr_down", "tree_jmr_down")
            # MC ONLY VARIABLES
            self.W = array('f', [1.0])
            self.AddBranch('weight_xsN', self.W)
            self.Wpu = array('f', [1.0])
            self.AddBranch('weight_PU', self.Wpu)
            self.Wpuu = array('f', [1.0])
            self.AddBranch('weight_PU_up', self.Wpuu)
            self.Wpud = array('f', [1.0])
            self.AddBranch('weight_PU_dn', self.Wpud)
            self.WT = array('f', [-1.0])
            self.AddBranch('weight_trig', self.WT)
            self.WTup = array('f', [-1.0])
            self.AddBranch('weight_trig_up', self.WTup)
            self.WTdn = array('f', [-1.0])
            self.AddBranch('weight_trig_dn', self.WTdn)
            self.evt_ttRW = array('f', [-1.0])
            self.AddBranch('evt_ttRW', self.evt_ttRW)
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
        for e in self.T:
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
                self.Wpuu[0] = self.T.puWeightUp
                self.Wpud[0] = self.T.puWeightDown
                ttbarHT = 0.0
                for gp in range(self.T.nGenPart):
                    if math.fabs(self.T.GenPart_pdgId[gp]) == 6 and self.T.GenPart_status[gp] == 62:
                        ttbarHT += self.T.GenPart_pt[gp]
                self.evt_ttRW[0] = ttbarHT
                self.WT[0] = self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT))
                self.WTup[0] = min(1.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) + self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))
                self.WTdn[0] = max(0.0, self.TrigHist.GetBinContent(self.TrigHist.FindBin(self.HT)) - self.TrigHist.GetBinError(self.TrigHist.FindBin(self.HT)))
                self.FillJetVars(self.T.FatJet_pt_jesTotalUp, self.T.FatJet_mass_jesTotalUp, self.T.FatJet_msoftdrop_jesTotalUp, self.T_jes_up)
                self.FillJetVars(self.T.FatJet_pt_jesTotalDown, self.T.FatJet_mass_jesTotalDown, self.T.FatJet_msoftdrop_jesTotalDown, self.T_jes_down)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmsUp, self.T.FatJet_msoftdrop_jmsUp, self.T_jms_up)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmsDown, self.T.FatJet_msoftdrop_jmsDown, self.T_jms_down)
                self.FillJetVars(self.T.FatJet_pt_jerUp, self.T.FatJet_mass_jerUp, self.T.FatJet_msoftdrop_jerUp, self.T_jer_up)
                self.FillJetVars(self.T.FatJet_pt_jerDown, self.T.FatJet_mass_jerDown, self.T.FatJet_msoftdrop_jerDown, self.T_jer_down)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmrUp, self.T.FatJet_msoftdrop_jmrUp, self.T_jmr_up)
                self.FillJetVars(self.T.FatJet_pt, self.T.FatJet_mass_jmrDown, self.T.FatJet_msoftdrop_jmrDown, self.T_jmr_down)


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
            self.T_jes_up.Branch(name, obj, name+"/F")
            self.T_jes_down.Branch(name, obj, name+"/F")
            self.T_jer_up.Branch(name, obj, name+"/F")
            self.T_jer_down.Branch(name, obj, name+"/F")
            self.T_jms_up.Branch(name, obj, name+"/F")
            self.T_jms_down.Branch(name, obj, name+"/F")
            self.T_jmr_up.Branch(name, obj, name+"/F")
            self.T_jmr_down.Branch(name, obj, name+"/F")


picoTree(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])