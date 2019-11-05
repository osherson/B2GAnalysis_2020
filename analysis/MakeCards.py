from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "update")
for Sigs in SIG:
	for VAR in EstVars:
		if not VAR[3]: continue
		cardname = VAR[0]+"_"+Sigs[3]
		print "Making datacard for " + VAR[0] + ", " + Sigs[3]
		print "Card and Shapes name:   " + cardname

		# The "Main histograms:"
		###########################################################################
		A = outF.Get("rA_data_"+VAR[0])
		NBINS = A.GetNbinsX()+1
		Att = outF.Get("rA_ttbar_"+VAR[0])
		B = outF.Get("rB_nom_data_"+VAR[0])
		B_stat = outF.Get("rB_stat_data_"+VAR[0])
		Btt = outF.Get("rB_nom_ttbar_"+VAR[0])
		Btt_stat = outF.Get("rB_stat_ttbar_"+VAR[0])

		B.Add(Btt, -1.)
		B_stat.Add(Btt_stat, -1.)
		DATA = A.Clone("data_obs")
		TTBAR = Att.Clone("ttbar")
		NONRES = B.Clone("nonres")
		###########################################################################

		# now the ttbar uncertainties:
		###########################################################################
		Att_au = outF.Get("rA_ttbar_au_"+VAR[0])
		Att_ad = outF.Get("rA_ttbar_ad_"+VAR[0])
		Att_nu = outF.Get("rA_ttbar_nu_"+VAR[0])
		Att_nd = outF.Get("rA_ttbar_nd_"+VAR[0])
		B_au = outF.Get("rB_au_data_"+VAR[0])
		Btt_au = outF.Get("rB_au_ttbar_au_"+VAR[0])
		B_au.Add(Btt_au, -1.)
		B_ad = outF.Get("rB_ad_data_"+VAR[0])
		Btt_ad = outF.Get("rB_ad_ttbar_ad_"+VAR[0])
		B_ad.Add(Btt_ad, -1.)
		B_nu = outF.Get("rB_nu_data_"+VAR[0])
		Btt_nu = outF.Get("rB_nu_ttbar_nu_"+VAR[0])
		B_nu.Add(Btt_nu, -1.)
		B_nd = outF.Get("rB_nd_data_"+VAR[0])
		Btt_nd = outF.Get("rB_nd_ttbar_nd_"+VAR[0])
		B_nd.Add(Btt_nd, -1.)



		TTBAR_au = Att_au.Clone("ttbar_TTAUp")
		TTBAR_ad = Att_ad.Clone("ttbar_TTADown")
		TTBAR_nu = Att_nu.Clone("ttbar_TTNormUp")
		TTBAR_nd = Att_nd.Clone("ttbar_TTNormDown")
		NONRES_au = B_au.Clone("nonres_TTAUp")
		NONRES_ad = B_ad.Clone("nonres_TTADown")
		NONRES_nu = B_nu.Clone("nonres_TTNormUp")
		NONRES_nd = B_nd.Clone("nonres_TTNormDown")
		###########################################################################

		# now the bin by bin BB uncertainties:
		###########################################################################
		NONRES_BB = []
		for i in range(1,NBINS):
			BB_B_tempU = B.Clone("nonres_BarBeeBin"+str(i)+"Up")
			BB_B_tempD = B.Clone("nonres_BarBeeBin"+str(i)+"Down")
			ErrStat = B.GetBinContent(i)*(B_stat.GetBinError(i)/B_stat.GetBinContent(i))
			BB_B_tempU.SetBinContent(i, BB_B_tempU.GetBinContent(i) + ErrStat)
			BB_B_tempD.SetBinContent(i, max(0.,BB_B_tempD.GetBinContent(i) - ErrStat))
			NONRES_BB.append(BB_B_tempU)
			NONRES_BB.append(BB_B_tempD)
		###########################################################################

		# now the uncertainty from each variables in the fit:
		###########################################################################
		FitUncs = []
		for i in range(NFITPAR):
			B_unc_u = outF.Get("rB_uncU_"+str(i)+"_data_"+VAR[0])
			B_unc_d = outF.Get("rB_uncD_"+str(i)+"_data_"+VAR[0])
			Btt_unc_u = outF.Get("rB_uncU_"+str(i)+"_ttbar_"+VAR[0])
			Btt_unc_d = outF.Get("rB_uncD_"+str(i)+"_ttbar_"+VAR[0])
			B_unc_u.Add(Btt_unc_u, -1.)
			B_unc_d.Add(Btt_unc_d, -1.)
			FUnc_tempU = B_unc_u.Clone("nonres_P"+str(i)+"Up")
			FUnc_tempD = B_unc_d.Clone("nonres_P"+str(i)+"Down")
			FitUncs.append(FUnc_tempU)
			FitUncs.append(FUnc_tempD)
		###########################################################################


		#### SIGNALS!!!
		AS = outF.Get("rA_"+Sigs[3]+"_"+VAR[0])
		SIGNAL = AS.Clone("signal")

		# Using this for a plot later
		Leg = ROOT.TLegend(0.65,0.65,0.89,0.89)
		Leg.SetLineColor(0)
		Leg.SetFillColor(0)
		Leg.AddEntry(SIGNAL, "Signal: " + Sigs[4], "L")

		SignalSysts = []
		for sys in SysWeighted:
			SysU = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0])
			SysD = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0])
			SaveSysU = SysU.Clone("signal_"+sys[0]+"Up")
			SaveSysD = SysD.Clone("signal_"+sys[0]+"Down")
			SignalSysts.append(SaveSysU)
			SignalSysts.append(SaveSysD)
			Leg.AddEntry(SaveSysU, sys[3],"L")
		for sys in SysComputed:
			SysU = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0])
			SysD = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0])
			SaveSysU = SysU.Clone("signal_"+sys[0]+"Up")
			SaveSysD = SysD.Clone("signal_"+sys[0]+"Down")
			SignalSysts.append(SaveSysU)
			SignalSysts.append(SaveSysD)
			Leg.AddEntry(SaveSysU, sys[3],"L")


		CombineShapes = ROOT.TFile("../results/"+NAME+"/"+cardname+"_SHAPES.root", "recreate")
		CombineShapes.cd()

		DATA.Write()
		TTBAR.Write()
		NONRES.Write()
		SIGNAL.Write()

		TTBAR_au.Write()
		TTBAR_ad.Write()
		TTBAR_nu.Write()
		TTBAR_nd.Write()
		NONRES_au.Write()
		NONRES_ad.Write()
		NONRES_nu.Write()
		NONRES_nd.Write()

		for h in NONRES_BB: h.Write()
		for h in FitUncs: h.Write()
		for h in SignalSysts: h.Write()

		CombineShapes.Write()
		CombineShapes.Save()
		CombineShapes.Close()

		##### WRITE THE ACTUAL CARD:




		text_file = open("../results/"+NAME+"/Card_"+cardname+".txt", "w")
		text_file.write("max    1     number of categories\n")
		text_file.write("jmax   *     number of samples minus one\n")
		text_file.write("kmax   *     number of nuisance parameters\n")
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("shapes * * "+cardname+"_SHAPES.root $PROCESS $PROCESS_$SYSTEMATIC\n")
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("bin                                            SigReg\n")
		text_file.write("observation                                    %f\n"%(DATA.Integral()))
		text_file.write("-------------------------------------------------------------------------------\n")

		text_file.write("bin                                   SigReg             SigReg      SigReg     \n")
		text_file.write("process                               0                  1           2         \n")
		text_file.write("process                               signal             nonres         ttbar     \n")
		text_file.write("rate                                  %f                 %f          %f        \n"%(SIGNAL.Integral(),NONRES.Integral(),TTBAR.Integral()))
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("BBSF lnN                      1.15              -          -          \n")
		text_file.write("lumi lnN                      1.025              -          -          \n")
		text_file.write("trig lnN                      1.05              -          -       \n")
		for i in range(NFITPAR):
			text_file.write("P"+str(i)+" shapeN2                -             1.000         -\n")
		text_file.write("TTA shapeN2                             -                 1.000      1.000      \n")
		text_file.write("TTN shapeN2                             -                 1.000      1.000      \n")
		for i in range(1,NBINS):
		    text_file.write("BarBeeBin"+str(i)+" shapeN2                -             1.000         -\n")
		for sys in SysWeighted:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          \n")
		for sys in SysComputed:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          \n")
		text_file.close()


		GoodPlotFormat(SIGNAL, "thickline", ROOT.kBlack, 1)

		FindAndSetMax(SignalSysts)
		C = ROOT.TCanvas()
		C.cd()
		SIGNAL.Draw("hist")
		index = 0
		for h in SignalSysts:
			GoodPlotFormat(h, "thinline", ColLine[index][0], ColLine[index][1])
			index += 1
			h.Draw("samehist")
		Leg.Draw("same")
		C.Print("../results/"+NAME+"/SIGSYS"+Sigs[3]+"_"+NAME+"_"+VAR[0]+".root")
		C.Print("../results/"+NAME+"/SIGSYS"+Sigs[3]+"_"+NAME+"_"+VAR[0]+".png")

	for VAR in EstVars2D:
		if not VAR[3]: continue
		cardname = VAR[0]+"_vs_"+VAR[3]+"_"+Sigs[3]
		print "Making datacard for " + VAR[0]+"/"+VAR[3] + ", " + Sigs[3]
		print "Card and Shapes name:   " + cardname

		# The "Main histograms:"
		###########################################################################
		uA = outF.Get("rA_data_"+VAR[0]+"_"+VAR[3])
		A = Unroll(uA)
		NBINS = uA.GetNbinsX()+1
		uAtt = outF.Get("rA_ttbar_"+VAR[0]+"_"+VAR[3])
		uB = outF.Get("rB_nom_data_"+VAR[0]+"_"+VAR[3])
		uB_stat = outF.Get("rB_stat_data_"+VAR[0]+"_"+VAR[3])
		uBtt = outF.Get("rB_nom_ttbar_"+VAR[0]+"_"+VAR[3])
		uBtt_stat = outF.Get("rB_stat_ttbar_"+VAR[0]+"_"+VAR[3])

		uB.Add(uBtt, -1.)
		uB_stat.Add(uBtt_stat, -1.)

		DATA = A.Clone("data_obs")
		Att = Unroll(uAtt)
		TTBAR = Att.Clone("ttbar")

		B = Unroll(uB)
		NONRES = B.Clone("nonres")
		###########################################################################

		# now the ttbar uncertainties:
		###########################################################################
		uAtt_au = outF.Get("rA_ttbar_au_"+VAR[0]+"_"+VAR[3])
		uAtt_ad = outF.Get("rA_ttbar_ad_"+VAR[0]+"_"+VAR[3])
		uAtt_nu = outF.Get("rA_ttbar_nu_"+VAR[0]+"_"+VAR[3])
		uAtt_nd = outF.Get("rA_ttbar_nd_"+VAR[0]+"_"+VAR[3])
		uB_au = outF.Get("rB_au_data_"+VAR[0]+"_"+VAR[3])
		uBtt_au = outF.Get("rB_au_ttbar_au_"+VAR[0]+"_"+VAR[3])
		uB_au.Add(uBtt_au, -1.)
		uB_ad = outF.Get("rB_ad_data_"+VAR[0]+"_"+VAR[3])
		uBtt_ad = outF.Get("rB_ad_ttbar_ad_"+VAR[0]+"_"+VAR[3])
		uB_ad.Add(uBtt_ad, -1.)
		uB_nu = outF.Get("rB_nu_data_"+VAR[0]+"_"+VAR[3])
		uBtt_nu = outF.Get("rB_nu_ttbar_nu_"+VAR[0]+"_"+VAR[3])
		uB_nu.Add(uBtt_nu, -1.)
		uB_nd = outF.Get("rB_nd_data_"+VAR[0]+"_"+VAR[3])
		uBtt_nd = outF.Get("rB_nd_ttbar_nd_"+VAR[0]+"_"+VAR[3])
		uB_nd.Add(uBtt_nd, -1.)


		Att_au = Unroll(uAtt_au)
		Att_ad = Unroll(uAtt_ad)
		Att_nu = Unroll(uAtt_nu)
		Att_nd = Unroll(uAtt_nd)

		TTBAR_au = Att_au.Clone("ttbar_TTAUp")
		TTBAR_ad = Att_ad.Clone("ttbar_TTADown")
		TTBAR_nu = Att_nu.Clone("ttbar_TTNormUp")
		TTBAR_nd = Att_nd.Clone("ttbar_TTNormDown")
		
		B_au = Unroll(uB_au)
		B_ad = Unroll(uB_ad)
		B_nu = Unroll(uB_nu)
		B_nd = Unroll(uB_nd)

		NONRES_au = B_au.Clone("nonres_TTAUp")
		NONRES_ad = B_ad.Clone("nonres_TTADown")
		NONRES_nu = B_nu.Clone("nonres_TTNormUp")
		NONRES_nd = B_nd.Clone("nonres_TTNormDown")
		###########################################################################

		# now the bin by bin BB uncertainties:
		###########################################################################
		NONRES_BB = []
		for i in range(1,NBINS):
			BB_B_tempU = B.Clone("nonres_BarBeeBin"+str(i)+"Up")
			BB_B_tempD = B.Clone("nonres_BarBeeBin"+str(i)+"Down")
			ErrStat = B.GetBinContent(i)*(B_stat.GetBinError(i)/B_stat.GetBinContent(i))
			BB_B_tempU.SetBinContent(i, BB_B_tempU.GetBinContent(i) + ErrStat)
			BB_B_tempD.SetBinContent(i, max(0.,BB_B_tempD.GetBinContent(i) - ErrStat))
			NONRES_BB.append(BB_B_tempU)
			NONRES_BB.append(BB_B_tempD)
		###########################################################################

		# now the uncertainty from each variables in the fit:
		###########################################################################
		FitUncs = []
		for i in range(NFITPAR):
			uB_unc_u = outF.Get("rB_uncU_"+str(i)+"_data_"+VAR[0]+"_"+VAR[3])
			uB_unc_d = outF.Get("rB_uncD_"+str(i)+"_data_"+VAR[0]+"_"+VAR[3])
			uBtt_unc_u = outF.Get("rB_uncU_"+str(i)+"_ttbar_"+VAR[0]+"_"+VAR[3])
			uBtt_unc_d = outF.Get("rB_uncD_"+str(i)+"_ttbar_"+VAR[0]+"_"+VAR[3])
			uB_unc_u.Add(uBtt_unc_u, -1.)
			uB_unc_d.Add(uBtt_unc_d, -1.)
			B_unc_u = Unroll(uB_unc_u)
			B_unc_d = Unroll(uB_unc_d)
			FUnc_tempU = B_unc_u.Clone("nonres_P"+str(i)+"Up")
			FUnc_tempD = B_unc_d.Clone("nonres_P"+str(i)+"Down")
			FitUncs.append(FUnc_tempU)
			FitUncs.append(FUnc_tempD)
		###########################################################################


		#### SIGNALS!!!
		uAS = outF.Get("rA_"+Sigs[3]+"_"+VAR[0]+"_"+VAR[3])
		AS = Unroll(uAS)
		SIGNAL = AS.Clone("signal")

		# Using this for a plot later
		Leg = ROOT.TLegend(0.65,0.65,0.89,0.89)
		Leg.SetLineColor(0)
		Leg.SetFillColor(0)
		Leg.AddEntry(SIGNAL, "Signal: " + Sigs[4], "L")

		SignalSysts = []
		for sys in SysWeighted:
			uSysU = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			uSysD = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			SysU = Unroll(uSysU)
			SysD = Unroll(uSysD)
			SaveSysU = SysU.Clone("signal_"+sys[0]+"Up")
			SaveSysD = SysD.Clone("signal_"+sys[0]+"Down")
			SignalSysts.append(SaveSysU)
			SignalSysts.append(SaveSysD)
			Leg.AddEntry(SaveSysU, sys[3],"L")
		for sys in SysComputed:
			uSysU = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			uSysD = outF.Get("rA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			SysU = Unroll(uSysU)
			SysD = Unroll(uSysD)
			SaveSysU = SysU.Clone("signal_"+sys[0]+"Up")
			SaveSysD = SysD.Clone("signal_"+sys[0]+"Down")
			SignalSysts.append(SaveSysU)
			SignalSysts.append(SaveSysD)
			Leg.AddEntry(SaveSysU, sys[3],"L")


		CombineShapes = ROOT.TFile("../results/"+NAME+"/"+cardname+"_SHAPES.root", "recreate")
		CombineShapes.cd()

		DATA.Write()
		TTBAR.Write()
		NONRES.Write()
		SIGNAL.Write()

		TTBAR_au.Write()
		TTBAR_ad.Write()
		TTBAR_nu.Write()
		TTBAR_nd.Write()
		NONRES_au.Write()
		NONRES_ad.Write()
		NONRES_nu.Write()
		NONRES_nd.Write()

		for h in NONRES_BB: h.Write()
		for h in FitUncs: h.Write()
		for h in SignalSysts: h.Write()

		CombineShapes.Write()
		CombineShapes.Save()
		CombineShapes.Close()

		##### WRITE THE ACTUAL CARD:




		text_file = open("../results/"+NAME+"/Card_"+cardname+".txt", "w")
		text_file.write("max    1     number of categories\n")
		text_file.write("jmax   *     number of samples minus one\n")
		text_file.write("kmax   *     number of nuisance parameters\n")
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("shapes * * "+cardname+"_SHAPES.root $PROCESS $PROCESS_$SYSTEMATIC\n")
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("bin                                            SigReg\n")
		text_file.write("observation                                    %f\n"%(DATA.Integral()))
		text_file.write("-------------------------------------------------------------------------------\n")

		text_file.write("bin                                   SigReg             SigReg      SigReg     \n")
		text_file.write("process                               0                  1           2         \n")
		text_file.write("process                               signal             nonres         ttbar     \n")
		text_file.write("rate                                  %f                 %f          %f        \n"%(SIGNAL.Integral(),NONRES.Integral(),TTBAR.Integral()))
		text_file.write("-------------------------------------------------------------------------------\n")
		text_file.write("BBSF lnN                      1.15              -          -          \n")
		text_file.write("lumi lnN                      1.025              -          -          \n")
		text_file.write("trig lnN                      1.05              -          -       \n")
		for i in range(NFITPAR):
			text_file.write("P"+str(i)+" shapeN2                -             1.000         -\n")
		text_file.write("TTA shapeN2                             -                 1.000      1.000      \n")
		text_file.write("TTN shapeN2                             -                 1.000      1.000      \n")
		for i in range(1,NBINS):
		    text_file.write("BarBeeBin"+str(i)+" shapeN2                -             1.000         -\n")
		for sys in SysWeighted:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          \n")
		for sys in SysComputed:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          \n")
		text_file.close()


		GoodPlotFormat(SIGNAL, "thickline", ROOT.kBlack, 1)

		FindAndSetMax(SignalSysts)
		C = ROOT.TCanvas()
		C.cd()
		SIGNAL.Draw("hist")
		index = 0
		for h in SignalSysts:
			GoodPlotFormat(h, "thinline", ColLine[index][0], ColLine[index][1])
			index += 1
			h.Draw("samehist")
		Leg.Draw("same")
		AddCMSLumi(ROOT.gPad, plot_lumi, cmsextra)
		C.Print("../results/"+NAME+"/SIGSYS"+Sigs[3]+"_"+NAME+"_"+VAR[0]+"_vs_"+VAR[3]+".root")
		C.Print("../results/"+NAME+"/SIGSYS"+Sigs[3]+"_"+NAME+"_"+VAR[0]+"_vs_"+VAR[3]+".png")

