from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

ROOT.ROOT.EnableImplicitMT()

def AddFitToRDF(file, fit, var, newvar, rdf, name):
	newname = newvar+name
	usefit = file.Get(fit)
	ROOT.gInterpreter.ProcessLine("auto Use_Fit_"+newname+" = "+fit+";")
	usefit_code = 	'''
					float UseFit_'''+newname+'''(float x)
					{
						return Use_Fit_'''+newname+'''->Eval(x);
					}
					'''
	ROOT.gInterpreter.Declare(usefit_code)
	new_rdf = rdf.Define(newvar, "UseFit_"+newname+"("+var+")*total_weight")
	return new_rdf

def AddHToRDF(file, hist, var, newvar, rdf, name):
	newname = newvar+name
	useh = file.Get(hist)
	ROOT.gInterpreter.ProcessLine("auto Use_H_"+newname+" = "+hist+";")
	useh_code = 	'''
					float UseH_'''+newname+'''(float x)
					{

						return Use_H_'''+newname+'''->GetBinContent(Use_H_'''+newname+'''->FindBin(x));
					}
					'''
	ROOT.gInterpreter.Declare(useh_code)
	new_rdf = rdf.Define(newvar, "UseH_"+newname+"("+var+")*total_weight")
	return new_rdf


outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")

def GetEsts(Dists, name):
	print "Filling histograms for "+ name
	F = ROOT.TChain(Dists[2])
	for f in Dists[0]:
		F.Add(f)
	rdf = RDF(F)
	rdf = rdf.Define("total_weight", Dists[1])
	rdf = AddFitToRDF(outF, "aufit", FitVar[0], "w_aufit", rdf, name)
	rdf = AddFitToRDF(outF, "adfit", FitVar[0], "w_adfit", rdf, name)
	rdf = AddFitToRDF(outF, "nufit", FitVar[0], "w_nufit", rdf, name)
	rdf = AddFitToRDF(outF, "ndfit", FitVar[0], "w_ndfit", rdf, name)
	rdf = AddHToRDF(outF, "F_CD_fit_up", FitVar[0], "w_upfit", rdf, name)
	rdf = AddHToRDF(outF, "F_CD_fit_down", FitVar[0], "w_downfit", rdf, name)
	for i in range(NFITPAR):
		rdf = AddFitToRDF(outF, "uncfit_u_"+str(i), FitVar[0], "w_uncfit_u"+str(i), rdf, name)
		rdf = AddFitToRDF(outF, "uncfit_d_"+str(i), FitVar[0], "w_uncfit_d"+str(i), rdf, name)
	rdf = AddFitToRDF(outF, "nomfit", FitVar[0], "w_nomfit", rdf, name)

	VarsReturns = []
	for VAR in EstVars:
		rA_lazy = rdf.Filter(RegA).Histo1D(("rA_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "total_weight")
		rB_stat_lazy = rdf.Filter(RegB).Histo1D(("rB_stat_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "total_weight")
		rB_nom_lazy = rdf.Filter(RegB).Histo1D(("rB_nom_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_nomfit")
		rB_up_lazy = rdf.Filter(RegB).Histo1D(("rB_up_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_upfit")
		rB_down_lazy = rdf.Filter(RegB).Histo1D(("rB_down_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_downfit")
		rB_au_lazy = rdf.Filter(RegB).Histo1D(("rB_au_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_aufit")
		rB_ad_lazy = rdf.Filter(RegB).Histo1D(("rB_ad_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_adfit")
		rB_nu_lazy = rdf.Filter(RegB).Histo1D(("rB_nu_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_nufit")
		rB_nd_lazy = rdf.Filter(RegB).Histo1D(("rB_nd_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_ndfit")
		UNCS_lazy = []
		for i in range(NFITPAR):
			UNCS_lazy.append(rdf.Filter(RegB).Histo1D(("rB_uncU_"+str(i)+"_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_uncfit_u"+str(i)))
			UNCS_lazy.append(rdf.Filter(RegB).Histo1D(("rB_uncD_"+str(i)+"_"+name+"_"+VAR[0], ";"+VAR[2], len(VAR[1])-1, numpy.array(VAR[1])), VAR[0], "w_uncfit_d"+str(i)))
		rA = rA_lazy.GetValue()
		rB_nom = rB_nom_lazy.GetValue()
		rB_stat = rB_stat_lazy.GetValue()
		rB_up = rB_up_lazy.GetValue()
		rB_down = rB_down_lazy.GetValue()
		rB_au = rB_au_lazy.GetValue()
		rB_ad = rB_ad_lazy.GetValue()
		rB_nu = rB_nu_lazy.GetValue()
		rB_nd = rB_nd_lazy.GetValue()
		outF.cd()
		rA.Write()
		rB_nom.Write()
		rB_stat.Write()
		rB_up.Write()
		rB_down.Write()
		rB_au.Write()
		rB_ad.Write()
		rB_nu.Write()
		rB_nd.Write() 
		for u in UNCS_lazy:
			U = u.GetValue()
			U.Write()

	for VAR in EstVars2D:
		rA_lazy = rdf.Filter(RegA).Histo2D(("rA_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		rB_stat_lazy = rdf.Filter(RegB).Histo2D(("rB_stat_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		rB_nom_lazy = rdf.Filter(RegB).Histo2D(("rB_nom_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_nomfit")
		rB_up_lazy = rdf.Filter(RegB).Histo2D(("rB_up_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_upfit")
		rB_down_lazy = rdf.Filter(RegB).Histo2D(("rB_down_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_downfit")
		rB_au_lazy = rdf.Filter(RegB).Histo2D(("rB_au_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_aufit")
		rB_ad_lazy = rdf.Filter(RegB).Histo2D(("rB_ad_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_adfit")
		rB_nu_lazy = rdf.Filter(RegB).Histo2D(("rB_nu_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_nufit")
		rB_nd_lazy = rdf.Filter(RegB).Histo2D(("rB_nd_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_ndfit")
		UNCS_lazy = []
		for i in range(NFITPAR):
			UNCS_lazy.append(rdf.Filter(RegB).Histo2D(("rB_uncU_"+str(i)+"_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_uncfit_u"+str(i)))
			UNCS_lazy.append(rdf.Filter(RegB).Histo2D(("rB_uncD_"+str(i)+"_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "w_uncfit_d"+str(i)))
		rA = rA_lazy.GetValue()
		rB_nom = rB_nom_lazy.GetValue()
		rB_stat = rB_stat_lazy.GetValue()
		rB_up = rB_up_lazy.GetValue()
		rB_down = rB_down_lazy.GetValue()
		rB_au = rB_au_lazy.GetValue()
		rB_ad = rB_ad_lazy.GetValue()
		rB_nu = rB_nu_lazy.GetValue()
		rB_nd = rB_nd_lazy.GetValue()
		outF.cd()
		rA.Write()
		rB_nom.Write()
		rB_stat.Write()
		rB_up.Write()
		rB_down.Write()
		rB_au.Write()
		rB_ad.Write()
		rB_nu.Write()
		rB_nd.Write() 
		for u in UNCS_lazy:
			U = u.GetValue()
			U.Write()



GetEsts(DATA, "data")
GetEsts(TTBAR, "ttbar")
GetEsts(TTBAR_AU, "ttbar_au")
GetEsts(TTBAR_AD, "ttbar_ad")
GetEsts(TTBAR_NU, "ttbar_nu")
GetEsts(TTBAR_ND, "ttbar_nd")

outF.Save()
outF.Write()
outF.Close()