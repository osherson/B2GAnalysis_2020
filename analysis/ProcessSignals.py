import TEMPPAYLOAD
from TEMPPAYLOAD import *
ROOT.ROOT.EnableImplicitMT()

outF = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "update")


def GetEsts(files, weights, trees, name):
	print "Filling histograms for "+ name
	F = ROOT.TChain(trees)
	for f in files:
		F.Add(f)
	rdf = RDF(F)

	rdf = rdf.Define("total_weight", weights)

	for VAR in EstVars:
		SRrA_lazy = rdf.Filter(SR_A).Histo2D(("SRrA_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		CRrA_lazy = rdf.Filter(CR_A).Histo2D(("CRrA_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		SRrA = SRrA_lazy.GetValue()
		CRrA = CRrA_lazy.GetValue()
		outF.cd()
		SRrA.Write()
		CRrA.Write()

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
