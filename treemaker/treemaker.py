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

class PUW:
	def __init__(self, F, T, N, RW):
		self.npvTH = TH1F("npvTH", "", 100, 0, 100)
		self.Pn = TH1F("pn", "", 100, 0, 100)
		self.Pu = TH1F("pu", "", 100, 0, 100)
		self.Pd = TH1F("pd", "", 100, 0, 100)
		self.chain = ROOT.TChain(T)
		self.chain.Add(F)
		self.chain.Draw("Pileup_nTrueInt>>npvTH", "", "goff")
		self.Fn = TFile(RW[0])
		self.Fu = TFile(RW[1])
		self.Fd = TFile(RW[2])
		self.Pn.Add(self.Fn.Get("pileup"))
		self.Pu.Add(self.Fu.Get("pileup"))
		self.Pd.Add(self.Fd.Get("pileup"))
		self.npvTH.Scale(1/self.npvTH.Integral())
		self.Pn.Scale(1/self.Pn.Integral())
		self.Pu.Scale(1/self.Pu.Integral())
		self.Pd.Scale(1/self.Pd.Integral())
		self.Pn.Divide(self.npvTH)
		self.Pu.Divide(self.npvTH)
		self.Pd.Divide(self.npvTH)
	def GetW(self, which, npv):
		b = self.Pn.FindBin(npv)
		if which == "n":
			return self.Pn.GetBinContent(b)
		if which == "u":
			return self.Pu.GetBinContent(b)
		if which == "d":
			return self.Pd.GetBinContent(b)
	def SavePURWrates(self):
		C = TCanvas()
		C.cd()
		self.Pu.SetLineStyle(2)
		self.Pd.SetLineStyle(2)
		self.Pu.Draw("hist")
		self.Pn.Draw("histsame")
		self.Pd.Draw("histsame")
		C.Print("temp.png")

def GET(E, B):
	return getattr(E, B)
class JESUEtaSlice:
	def __init__(self, R):
		self.min = float(R[0])
		self.max = float(R[1])
		self.pTs = []
		for i in range(3,len(R)):
			if i%3 == 0:
				self.pTs.append([float(R[i]),float(R[i+1]),float(R[i+2])])
	def getU(self, J):
		if J.Eta() < self.max and J.Eta() > self.min:
			p = J.Pt()
			I = None
			i = 0
			while (p - self.pTs[i][0]) > 0:
				I = self.pTs[i]
				i += 1
				if i == len(self.pTs): break
			return [I[1], I[2]]
		else: return [-1.0, -1.0]
class PREPJESU:
	def __init__(self, J):
		self.Slices = []
		with open(J) as jecu:
			reader = csv.reader(jecu)
			next(reader)
			for row in reader:
				R = row[0].split()
				self.Slices.append(JESUEtaSlice(R))
				
	def GetU(self, j):
		for i in self.Slices:
			u =  i.getU(j)
			if u != [-1.0,-1.0]: return u
		return [-1.0, -1.0]			
class JERUEtaSlice:
	def __init__(self, R):
		self.min = float(R[0])
		self.max = float(R[1])
		self.cor = [float(R[3]), float(R[4]), float(R[5])]
	def getU(self, J):
		if J.Eta() < self.max and J.Eta() > self.min:
			return self.cor
		else: return [-1.0, -1.0, -1.0]
class PREPJERU:
	def __init__(self, J):
		self.Slices = []
		with open(J) as jecu:
			reader = csv.reader(jecu)
			next(reader)
			for row in reader:
				R = row[0].split()
				self.Slices.append(JERUEtaSlice(R))
	def GetU(self, j):
		for i in self.Slices:
			u =  i.getU(j)
			if u != [-1.0,-1.0, -1.0]: return u
		return [-1.0, -1.0, -1.0]
def GetJerJet(J, G, P, W):
	dM = J.M() - G.M()
	dP = J.Pt() - G.Pt()
	C = P.GetU(J)
	SF = 1 + ((C[0]-1)*dP/J.Pt())
	SFU =	1 + ((C[2]-1)*dP/J.Pt())
	SFD = 1 + ((C[1]-1)*dP/J.Pt())
	Jn = TLorentzVector()
	if W == "up":
		Jn.SetPtEtaPhiM(J.Pt()*SFU/SF, J.Eta(), J.Phi(), J.M()*SFU/SF)
	if W == "down":
		Jn.SetPtEtaPhiM(J.Pt()*SFD/SF, J.Eta(), J.Phi(), J.M()*SFD/SF)
	return Jn

class picoTree:
	def __init__(self, name, nanotrees, weight, triggers, jess, jers, JSON, mc, year, PUs):
		self.PUhits = PUs
		self.year = year
		self.jess = jess
		self.mc = mc
		self.jers = jers
		self.weight = weight
		self.JSON = LumiList (filename = JSON)
		self.__book__(name)
		for file in glob.glob(nanotrees + "*.root"):
			self.Fill(file, triggers)
		self.O.cd()
		self.O.Write()
		self.O.Close()
	def __book__(self, name):
		self.O = TFile(name+".root", "recreate")
		self.O.cd()
		self.T_nominal = TTree("tree_nominal", "tree_nominal")
		if self.mc:
			self.T_jes_up = TTree("tree_jes_up", "tree_jes_up")
			self.T_jes_down = TTree("tree_jes_down", "tree_jes_down")
			self.T_jer_up = TTree("tree_jer_up", "tree_jer_up")
			self.T_jer_down = TTree("tree_jer_down", "tree_jer_down")
		
		# EVENT VARIABLES
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
		self.evt_ttVeto = array('f', [-1.0])
		self.AddBranch('evt_ttVeto', self.evt_ttVeto)
		self.evt_ttRW = array('f', [-1.0])
		self.AddBranch('evt_ttRW', self.evt_ttRW)
		self.PV = array('f', [-1.0])
		self.AddBranch('PV', self.PV)
		self.evt_XM = array('f', [-1.0])
		self.AddBranch('evt_XM', self.evt_XM)
		self.evt_HT = array('f', [-1.0])
		self.AddBranch('evt_HT', self.evt_HT)
		self.evt_hhM = array('f', [-1.0])
		self.AddBranch('evt_hhM', self.evt_hhM)
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
		self.J1sbtag = array('f', [-1.0])
		self.AddBranch('J1sbtag', self.J1sbtag)
		self.J1dbtag = array('f', [-1.0])
		self.AddBranch('J1dbtag', self.J1dbtag)
		self.J1DeepBBtag = array('f', [-1.0])
		self.AddBranch('J1DeepBBtag', self.J1DeepBBtag)
		self.J1tau21 = array('f', [-1.0])
		self.AddBranch('J1tau21', self.J1tau21)
		self.J1tau32 = array('f', [-1.0])
		self.AddBranch('J1tau32', self.J1tau32)
		self.J2pt = array('f', [-1.0])
		self.AddBranch('J2pt', self.J2pt)
		self.J2eta = array('f', [-1.0])
		self.AddBranch('J2eta', self.J2eta)
		self.J2phi = array('f', [-1.0])
		self.AddBranch('J2phi', self.J2phi)
		self.J2SDM = array('f', [-1.0])
		self.AddBranch('J2SDM', self.J2SDM)
		self.J2sbtag = array('f', [-1.0])
		self.AddBranch('J2sbtag', self.J2sbtag)
		self.J2dbtag = array('f', [-1.0])
		self.AddBranch('J2dbtag', self.J2dbtag)
		self.J2DeepBBtag = array('f', [-1.0])
		self.AddBranch('J2DeepBBtag', self.J2DeepBBtag)
		self.J2tau21 = array('f', [-1.0])
		self.AddBranch('J2tau21', self.J2tau21)
		self.J2tau32 = array('f', [-1.0])
		self.AddBranch('J2tau32', self.J2tau32)
		
	def Fill(self, f, trigs):
		print "Working on " + f
		F = TFile(f)
		self.PUweighter = PUW(f, "Events", "doesthisgetreplaces", self.PUhits)
		self.T = F.Get("Events")
		n = 0
		for e in self.T:
			n+=1
#			if not n%33 == 0: continue
			passJson = False
			if self.mc:
				passJson = True
			else:
				passJson = self.JSON.contains(self.T.run,self.T.luminosityBlock)
			if not(passJson): continue

			triggered = False
			for t in trigs:
				if GET(e, t) > 0:
					triggered = True
					continue
			if not (triggered and self.T.nFatJet > 1 and self.T.PV_npvsGood > 0): continue
			if not min(self.T.FatJet_msoftdrop[0], self.T.FatJet_msoftdrop[1]) > 0.: continue
			if self.year == 2016: IDCUT = 2
			if self.year == 2017: IDCUT = 5
			if not min(self.T.FatJet_jetId[0], self.T.FatJet_jetId[1]) > IDCUT: continue
			
			
			self.HT = 0.
			for j in range(self.T.nJet):
				if self.T.Jet_pt[j] > 50. and math.fabs(self.T.Jet_eta[j]) < 2.4:
					self.HT += self.T.Jet_pt[j]
			
			J1 = TLorentzVector()
			J2 = TLorentzVector()
			
			J1.SetPtEtaPhiM(self.T.FatJet_pt[0], self.T.FatJet_eta[0], self.T.FatJet_phi[0], self.T.FatJet_mass[0])
			J2.SetPtEtaPhiM(self.T.FatJet_pt[1], self.T.FatJet_eta[1], self.T.FatJet_phi[1], self.T.FatJet_mass[1])
			self.FillJetVars([J1,J2], self.T_nominal)
                        self.PV[0] = self.T.PV_npvsGood
			if self.mc:
				# DO TTBAR RW STEP:
				ttbarHT = 0.0
				for gp in range(self.T.nGenPart):
					if math.fabs(self.T.GenPart_pdgId[gp]) == 6 and self.T.GenPart_status[gp] == 62:
						ttbarHT += self.T.GenPart_pt[gp]

				self.evt_ttRW[0] = ttbarHT

				J1sU = self.jess["JES"].GetU(J1)
				J2sU = self.jess["JES"].GetU(J2)
			
				JsU1 = J1*(1+J1sU[1])			
				JsU2 = J2*(1+J2sU[1])
				JsD1 = J1*(1-J1sU[0])			
				JsD2 = J2*(1-J2sU[0])
			
				G1 = TLorentzVector()
				G2 = TLorentzVector()
				G1m = False
				G2m = False
				for gj in range(self.T.nGenJetAK8):
					GJ = TLorentzVector()
					GJ.SetPtEtaPhiM(self.T.GenJetAK8_pt[gj], self.T.GenJetAK8_eta[gj], self.T.GenJetAK8_phi[gj], self.T.GenJetAK8_mass[gj])
					if GJ.DeltaR(J1) < 0.5:
						G1m = True
						G1 = GJ
					if GJ.DeltaR(J2) < 0.5:
						G2m = True
						G2 = GJ
				if G1m == False: G1 = J1*0.8
				if G2m == False: G2 = J2*0.8
						
				JrU1 = GetJerJet(J1, G1, self.jers["JER"], "up")
				JrU2 = GetJerJet(J2, G2, self.jers["JER"], "up")
				JrD1 = GetJerJet(J1, G1, self.jers["JER"], "down")
				JrD2 = GetJerJet(J2, G2, self.jers["JER"], "down")

				self.FillJetVars([JsU1,JsU2], self.T_jes_up)
				self.FillJetVars([JsD1,JsD2], self.T_jes_down)
				self.FillJetVars([JrU1,JrU2], self.T_jer_up)
				self.FillJetVars([JrD1,JrD2], self.T_jer_down)
	def FillJetVars(self, JETS, B):
		J1 = JETS[0]
		J2 = JETS[1]
		ntVj = 0
		for j in range(self.T.nJet):
			J = TLorentzVector()
			J.SetPtEtaPhiM(self.T.Jet_pt[j],self.T.Jet_eta[j],self.T.Jet_phi[j],self.T.Jet_mass[j])
			if J.Pt() > 90. and ((0.4 < J.DeltaR(J1) < 1.) or (0.4 < J.DeltaR(J2) < 1.)):
				ntVj += 1
		self.evt_ttVeto[0] = ntVj
		self.evt_HT[0] = self.HT
		self.evt_XM[0] = (J1+J2).M()
		self.evt_hhM[0] = (J1+J2).M() - (self.T.FatJet_msoftdrop[0] - 125.09) - (self.T.FatJet_msoftdrop[1] - 125.09)
		self.evt_Deta[0] = math.fabs(J1.Eta() - J2.Eta())
		self.evt_Dphi[0] = J1.DeltaPhi(J2)
		self.evt_DR[0] = J1.DeltaR(J2)
		self.evt_Masym[0] = math.fabs(self.T.FatJet_msoftdrop[0] - self.T.FatJet_msoftdrop[1])/(self.T.FatJet_msoftdrop[0] + self.T.FatJet_msoftdrop[1])
		self.evt_aM[0] = math.fabs(self.T.FatJet_msoftdrop[0] + self.T.FatJet_msoftdrop[1])/2.0
		if self.mc:
			self.W[0] = self.weight
			self.WT[0] = 1.
			npv = self.T.Pileup_nTrueInt
			self.Wpu[0] = self.PUweighter.GetW("n", npv)
			self.Wpuu[0] = self.PUweighter.GetW("u", npv)
			self.Wpud[0] = self.PUweighter.GetW("d", npv)
		self.J1pt[0] = J1.Pt()
		self.J1eta[0] = J1.Eta()
		self.J1phi[0] = J1.Phi()
		self.J2pt[0] = J2.Pt()
		self.J2eta[0] = J2.Eta()
		self.J2phi[0] = J2.Phi()
		self.J1sbtag[0] = self.T.FatJet_btagCSVV2[0]
		self.J2sbtag[0] = self.T.FatJet_btagCSVV2[1]
		self.J1DeepBBtag[0] = self.T.FatJet_btagDDBvL[0]
		self.J2DeepBBtag[0] = self.T.FatJet_btagDDBvL[1]
		self.J1dbtag[0] = self.T.FatJet_btagHbb[0]
		self.J2dbtag[0] = self.T.FatJet_btagHbb[1]
		if self.T.FatJet_tau2[0] > 0: self.J1tau32[0] = self.T.FatJet_tau3[0]/self.T.FatJet_tau2[0]
		if self.T.FatJet_tau2[1] > 0: self.J2tau32[0] = self.T.FatJet_tau3[1]/self.T.FatJet_tau2[1]
		if self.T.FatJet_tau1[0] > 0: self.J1tau21[0] = self.T.FatJet_tau2[0]/self.T.FatJet_tau1[0]
		if self.T.FatJet_tau1[1] > 0: self.J2tau21[0] = self.T.FatJet_tau2[1]/self.T.FatJet_tau1[1]
		self.J1SDM[0] = self.T.FatJet_msoftdrop[0]
		self.J2SDM[0] = self.T.FatJet_msoftdrop[1]
		B.Fill()
			
	def AddBranch(self, name, obj):
		self.T_nominal.Branch(name, obj, name+"/F")
		if self.mc:
			self.T_jes_up.Branch(name, obj, name+"/F")
			self.T_jes_down.Branch(name, obj, name+"/F")
			self.T_jer_up.Branch(name, obj, name+"/F")
			self.T_jer_down.Branch(name, obj, name+"/F")
	
if __name__ == "__main__":
	triggers = ["HLT_PFHT800", "HLT_PFHT900", "HLT_AK8PFJet450"]
	jess = {"JES": PREPJESU("Summer16_07Aug2017_V11_MC_Uncertainty_AK8PFPuppi.txt")}
	jers = {"JER": PREPJERU("Summer16_25nsV1_MC_SF_AK8PFPuppi.txt")}
	JSON = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_Alejandro.txt"
#	PicoTreeDATATest = picoTree("DATA_TEST", "/cms/vlq2/nanoaod/2016/data/JetHT/JetHT_Run2016B_05Feb2018_ver1-v1/", 1.0, triggers, jess, jers, JSON, False, 2016,["pileup_nominal_data16.root","pileup_up_data16.root","pileup_down_data16.root"])
	PicoTreeMCTest = picoTree("MC_TEST", "/cms/xaastorage/NanoAOD/2016/2016_TT_Jets/", 1.0, triggers, jess, jers, JSON, True, 2016,["pileup_nominal_data16.root","pileup_up_data16.root","pileup_down_data16.root"])

