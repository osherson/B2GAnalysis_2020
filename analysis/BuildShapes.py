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

outF = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "update")
def GetEsts(Dists, Reg, name):
	if Reg == "SR":
		RegA = SR_A
		RegB = SR_B
	else:
		RegA = CR_A
		RegB = CR_B
	F = ROOT.TChain(Dists[2])
	for f in Dists[0]:
		F.Add(f)
	rdf = RDF(F)
	rdf = rdf.Define("total_weight", Dists[1])
	rdf = AddFitToRDF(outF, Reg+"aufit", FitVar[0], Reg+"w_aufit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"adfit", FitVar[0], Reg+"w_adfit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"nufit", FitVar[0], Reg+"w_nufit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"ndfit", FitVar[0], Reg+"w_ndfit", rdf, name)
	for i in range(NFITPAR):
		rdf = AddFitToRDF(outF, Reg+"uncfit_u_"+str(i), FitVar[0], Reg+"w_uncfit_u"+str(i), rdf, name)
		rdf = AddFitToRDF(outF, Reg+"uncfit_d_"+str(i), FitVar[0], Reg+"w_uncfit_d"+str(i), rdf, name)
	rdf = AddFitToRDF(outF, Reg+"CDnomfit", FitVar[0], Reg+"w_nomfit", rdf, name)

	for VAR in EstVars:
		rA_lazy = rdf.Filter(RegA).Histo2D((Reg+"rA_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		rB_stat_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_stat_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], "total_weight")
		rB_nom_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_nom_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_nomfit")
		rB_au_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_au_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_aufit")
		rB_ad_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_ad_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_adfit")
		rB_nu_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_nu_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_nufit")
		rB_nd_lazy = rdf.Filter(RegB).Histo2D((Reg+"rB_nd_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_ndfit")
		UNCS_lazy = []
		for i in range(NFITPAR):
			UNCS_lazy.append(rdf.Filter(RegB).Histo2D((Reg+"rB_uncU_"+str(i)+"_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_uncfit_u"+str(i)))
			UNCS_lazy.append(rdf.Filter(RegB).Histo2D((Reg+"rB_uncD_"+str(i)+"_"+name+"_"+VAR[0]+"_"+VAR[3], ";"+VAR[2]+";"+VAR[5], len(VAR[1])-1, numpy.array(VAR[1]), len(VAR[4])-1, numpy.array(VAR[4])), VAR[0], VAR[3], Reg+"w_uncfit_d"+str(i)))
		rA = rA_lazy.GetValue()
		rB_nom = rB_nom_lazy.GetValue()
		rB_stat = rB_stat_lazy.GetValue()
		rB_au = rB_au_lazy.GetValue()
		rB_ad = rB_ad_lazy.GetValue()
		rB_nu = rB_nu_lazy.GetValue()
		rB_nd = rB_nd_lazy.GetValue()
		outF.cd()
		rA.Write()
		rB_nom.Write()
		rB_stat.Write()
		rB_au.Write()
		rB_ad.Write()
		rB_nu.Write()
		rB_nd.Write() 
		for u in UNCS_lazy:
			U = u.GetValue()
			U.Write()
	
for R in ["SR", "CR"]:
	GetEsts(DATA, R, "data")
	GetEsts(TTBAR, R, "ttbar")
	GetEsts(TTBAR_AU, R, "ttbar_au")
	GetEsts(TTBAR_AD, R, "ttbar_ad")
	GetEsts(TTBAR_NU, R, "ttbar_nu")
	GetEsts(TTBAR_ND, R, "ttbar_nd")

outF.Save()
outF.Write()
outF.Close()
