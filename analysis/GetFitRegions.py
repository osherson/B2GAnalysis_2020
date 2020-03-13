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
	srA_lazy = w_rdf.Filter(SR_A).Histo1D(("SRA_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	srB_lazy = w_rdf.Filter(SR_B).Histo1D(("SRB_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	srC_lazy = w_rdf.Filter(SR_C).Histo1D(("SRC_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	srD_lazy = w_rdf.Filter(SR_D).Histo1D(("SRD_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	crA_lazy = w_rdf.Filter(CR_A).Histo1D(("CRA_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	crB_lazy = w_rdf.Filter(CR_B).Histo1D(("CRB_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	crC_lazy = w_rdf.Filter(CR_C).Histo1D(("CRC_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")
	crD_lazy = w_rdf.Filter(CR_D).Histo1D(("CRD_fitvar_"+name, ";"+FitVar[2], len(FitVar[1])-1, numpy.array(FitVar[1])), FitVar[0], "total_weight")


	srA = srA_lazy.GetValue()
	srB = srB_lazy.GetValue()
	srC = srC_lazy.GetValue()
	srD = srD_lazy.GetValue()
	crA = crA_lazy.GetValue()
	crB = crB_lazy.GetValue()
	crC = crC_lazy.GetValue()
	crD = crD_lazy.GetValue()

	outF = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "update")
	srA.Write()
	srB.Write()
	srC.Write()
	srD.Write()
	crA.Write()
	crB.Write()
	crC.Write()
	crD.Write()
	outF.Save()
	outF.Write()
	outF.Close()
	
GetABCD(DATA, "data")
GetABCD(TTBAR, "ttbar")
GetABCD(TTBAR_AU, "ttbar_au")
GetABCD(TTBAR_AD, "ttbar_ad")
GetABCD(TTBAR_NU, "ttbar_nu")
GetABCD(TTBAR_ND, "ttbar_nd")
