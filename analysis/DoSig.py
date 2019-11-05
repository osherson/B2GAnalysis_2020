from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

ROOT.ROOT.EnableImplicitMT()

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")

def GetEsts(files, weights, trees, name):
	print "Filling histograms for "+ name
	F = ROOT.TChain(trees)
	for f in files:
		F.Add(f)
	rdf = RDF(F)

	rdf = rdf.Define("total_weight", weights)
	for VAR in EstVars:
		rA_lazy = rdf.Filter(RegA).Histo1D(("rA_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "total_weight")
		rA = rA_lazy.GetValue()
		outF.cd()
		rA.Write()

	for VAR in EstVars2D:
		rA_lazy = rdf.Filter(RegA).Histo2D(("rA_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		rA = rA_lazy.GetValue()
		outF.cd()
		rA.Write()

for S in SIG:
	GetEsts(S[0], S[1], S[2], S[3])
	for sys in SysWeighted:
		GetEsts(S[0], S[1]+"*"+sys[1], S[2], S[3]+"_"+sys[0]+"U")
		GetEsts(S[0], S[1]+"*"+sys[2], S[2], S[3]+"_"+sys[0]+"D")
	for sys in SysComputed:
		GetEsts(S[0], S[1], sys[1], S[3]+"_"+sys[0]+"U")
		GetEsts(S[0], S[1], sys[1], S[3]+"_"+sys[0]+"D")

outF.Save()
outF.Write()
outF.Close()