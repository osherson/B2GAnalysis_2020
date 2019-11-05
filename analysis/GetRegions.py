import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

ROOT.ROOT.EnableImplicitMT()

def GetABCD(Dists, name):
	# load the dists in a tchain and then make an RDF with them
	F = ROOT.TChain(Dists[2])
	for f in Dists[0]:
		F.Add(f)
	rdf = RDF(F)
	w_rdf = rdf.Define("total_weight", Dists[1])

	# now we extract the plots that we want:
	PreSel_H2_lazy = w_rdf.Filter(PRESELECTION).Histo2D(("presel_ABCD_"+name, ";"+VAR_ABvCD[2]+";"+VAR_ACvBD[2], len(VAR_ABvCD[1])-1, numpy.array(VAR_ABvCD[1]), len(VAR_ACvBD[1])-1, numpy.array(VAR_ACvBD[1])), VAR_ABvCD[0], VAR_ACvBD[0], "total_weight")
	rA_lazy = w_rdf.Filter(RegA).Histo1D(("rA_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	rB_lazy = w_rdf.Filter(RegB).Histo1D(("rB_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	rC_lazy = w_rdf.Filter(RegC).Histo1D(("rC_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	rD_lazy = w_rdf.Filter(RegD).Histo1D(("rD_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")

	PreSel_H2 = PreSel_H2_lazy.GetValue()
	rA = rA_lazy.GetValue()
	rB = rB_lazy.GetValue()
	rC = rC_lazy.GetValue()
	rD = rD_lazy.GetValue()

	outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")
	PreSel_H2.Write()
	rA.Write()
	rB.Write()
	rC.Write()
	rD.Write()
	outF.Save()
	outF.Write()
	outF.Close()


GetABCD(DATA, "data")
GetABCD(TTBAR, "ttbar")
GetABCD(TTBAR_AU, "ttbar_au")
GetABCD(TTBAR_AD, "ttbar_ad")
GetABCD(TTBAR_NU, "ttbar_nu")
GetABCD(TTBAR_ND, "ttbar_nd")
for S in SIG:
	GetABCD(S, S[3])