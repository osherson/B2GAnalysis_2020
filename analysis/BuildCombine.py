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
	F = ROOT.TChain(Dists[2])
	for f in Dists[0]:
		F.Add(f)
	rdf = RDF(F)
	rdf = rdf.Define("total_weight", Dists[1])
	rdf = AddFitToRDF(outF, Reg+"aufit", FitVar[0], "w_aufit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"adfit", FitVar[0], "w_adfit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"nufit", FitVar[0], "w_nufit", rdf, name)
	rdf = AddFitToRDF(outF, Reg+"ndfit", FitVar[0], "w_ndfit", rdf, name)
	for i in range(NFITPAR):
		rdf = AddFitToRDF(outF, Reg+"uncfit_u_"+str(i), FitVar[0], "w_uncfit_u"+str(i), rdf, name)
		rdf = AddFitToRDF(outF, Reg+"uncfit_d_"+str(i), FitVar[0], "w_uncfit_d"+str(i), rdf, name)
	rdf = AddFitToRDF(outF, Reg+"nomfit", FitVar[0], "w_nomfit", rdf, name)
	
for R in ["sr", "cr"]:
	GetEsts(DATA, R, "data")
	GetEsts(TTBAR, R, "ttbar")
	GetEsts(TTBAR_AU, R, "ttbar_au")
	GetEsts(TTBAR_AD, R, "ttbar_ad")
	GetEsts(TTBAR_NU, R, "ttbar_nu")
	GetEsts(TTBAR_ND, R, "ttbar_nd")

outF.Save()
outF.Write()
outF.Close()
