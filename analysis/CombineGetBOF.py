import TEMPPAYLOAD
from TEMPPAYLOAD import *

for Sigs in SIG:
	for VAR in EstVars:
		name = VAR[0]+"_"+VAR[3]
		CbnF = ROOT.TFile("fitDiagnostics.root")
		CbnW = ROOT.TFile("higgsCombineTest.FitDiagnostics.mH120.root")
		w = CbnW.Get('w')
		fr = CbnF.Get('fit_b')
		myargs = ROOT.RooArgSet(fr.floatParsFinal())
		importPars = w.saveSnapshot(Sigs[3]+name+'BOFit',myargs)
		fout = ROOT.TFile(Sigs[3]+name+'FitWorkspace.root',"recreate")
		fout.cd()
		fout.WriteTObject(w,'w')
		fout.Write()
		fout.Save()
		fout.Close()
