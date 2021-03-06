import TEMPPAYLOAD
from TEMPPAYLOAD import *

outF = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "update")
for Sigs in SIG:
	for VAR in EstVars:
		name = VAR[0]+"_"+VAR[3]
		os.system("cp CardTemplate.tpl CARD_"+Sigs[3]+name+".txt") 
		shapes = []
		
		SR_A = outF.Get("SRrA_data_"+name)
		CR_A = outF.Get("CRrA_data_"+name)
		SR_Att = outF.Get("SRrA_ttbar_"+name)
		CR_Att = outF.Get("CRrA_ttbar_"+name)
		
		shapes.append(Unroll(SR_A, "SR"+NAME+"_data_obs"))
		shapes.append(Unroll(CR_A, "CR"+NAME+"_data_obs"))
		shapes.append(Unroll(SR_Att, "SR"+NAME+"_ttbar"+NAME))
		shapes.append(Unroll(CR_Att, "CR"+NAME+"_ttbar"+NAME))
		
		SRN = SR_A.Integral()
		CRN = CR_A.Integral()
		TSR = SR_Att.Integral()
		TCR = CR_Att.Integral()
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_SRN_", str(SRN))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_CRN_", str(CRN))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_TSR_", str(TSR))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_TCR_", str(TCR))
		
		SR_B = outF.Get("SRrB_nom_data_"+name)
		SR_Btt = outF.Get("SRrB_nom_ttbar_"+name)
		SR_B.Add(SR_Btt, -1.)
		CR_B = outF.Get("CRrB_nom_data_"+name)
		CR_Btt = outF.Get("CRrB_nom_ttbar_"+name)
		CR_B.Add(CR_Btt, -1.)
		
		shapes.append(Unroll(SR_B, "SR"+NAME+"_qcdsr"+NAME))
		shapes.append(Unroll(CR_B, "CR"+NAME+"_qcdcr"+NAME))
		
		
		QSR = SR_B.Integral()
		QCR = CR_B.Integral()
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_QSR_", str(QSR))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_QCR_", str(QCR))
		
		SR_Attau = outF.Get("SRrA_ttbar_au_"+name)
		CR_Attau = outF.Get("CRrA_ttbar_au_"+name)
		SR_Attad = outF.Get("SRrA_ttbar_ad_"+name)
		CR_Attad = outF.Get("CRrA_ttbar_ad_"+name)
		SR_Attnu = outF.Get("SRrA_ttbar_nu_"+name)
		CR_Attnu = outF.Get("CRrA_ttbar_nu_"+name)
		SR_Attnd = outF.Get("SRrA_ttbar_nd_"+name)
		CR_Attnd = outF.Get("CRrA_ttbar_nd_"+name)
		
		shapes.append(Unroll(SR_Attau, "SR"+NAME+"_ttbar"+NAME+"_ttA"+NAME+"Up"))
		shapes.append(Unroll(CR_Attau, "CR"+NAME+"_ttbar"+NAME+"_ttA"+NAME+"Up"))
		shapes.append(Unroll(SR_Attad, "SR"+NAME+"_ttbar"+NAME+"_ttA"+NAME+"Down"))
		shapes.append(Unroll(CR_Attad, "CR"+NAME+"_ttbar"+NAME+"_ttA"+NAME+"Down"))
		shapes.append(Unroll(SR_Attnu, "SR"+NAME+"_ttbar"+NAME+"_ttN"+NAME+"Up"))
		shapes.append(Unroll(CR_Attnu, "CR"+NAME+"_ttbar"+NAME+"_ttN"+NAME+"Up"))
		shapes.append(Unroll(SR_Attnd, "SR"+NAME+"_ttbar"+NAME+"_ttN"+NAME+"Down"))
		shapes.append(Unroll(CR_Attnd, "CR"+NAME+"_ttbar"+NAME+"_ttN"+NAME+"Down"))
		

		
		SR_Bau = outF.Get("SRrB_au_data_"+name)
		SR_Bttau = outF.Get("SRrB_au_ttbar_"+name)
		SR_Bau.Add(SR_Bttau, -1.)
		CR_Bau = outF.Get("CRrB_au_data_"+name)
		CR_Bttau = outF.Get("CRrB_au_ttbar_"+name)
		CR_Bau.Add(CR_Bttau, -1.)
		
		SR_Bad = outF.Get("SRrB_ad_data_"+name)
		SR_Bttad = outF.Get("SRrB_ad_ttbar_"+name)
		SR_Bad.Add(SR_Bttad, -1.)
		CR_Bad = outF.Get("CRrB_ad_data_"+name)
		CR_Bttad = outF.Get("CRrB_ad_ttbar_"+name)
		CR_Bad.Add(CR_Bttad, -1.)
		
		SR_Bnu = outF.Get("SRrB_nu_data_"+name)
		SR_Bttnu = outF.Get("SRrB_nu_ttbar_"+name)
		SR_Bnu.Add(SR_Bttnu, -1.)
		CR_Bnu = outF.Get("CRrB_nu_data_"+name)
		CR_Bttnu = outF.Get("CRrB_nu_ttbar_"+name)
		CR_Bnu.Add(CR_Bttnu, -1.)
		
		SR_Bnd = outF.Get("SRrB_nd_data_"+name)
		SR_Bttnd = outF.Get("SRrB_nd_ttbar_"+name)
		SR_Bnd.Add(SR_Bttnd, -1.)
		CR_Bnd = outF.Get("CRrB_nd_data_"+name)
		CR_Bttnd = outF.Get("CRrB_nd_ttbar_"+name)
		CR_Bnd.Add(CR_Bttnd, -1.)
		
		shapes.append(Unroll(SR_Bau, "SR"+NAME+"_qcdsr"+NAME+"_ttA"+NAME+"Up"))
		shapes.append(Unroll(CR_Bau, "CR"+NAME+"_qcdcr"+NAME+"_ttA"+NAME+"Up"))
		shapes.append(Unroll(SR_Bad, "SR"+NAME+"_qcdsr"+NAME+"_ttA"+NAME+"Down"))
		shapes.append(Unroll(CR_Bad, "CR"+NAME+"_qcdcr"+NAME+"_ttA"+NAME+"Down"))
		shapes.append(Unroll(SR_Bnu, "SR"+NAME+"_qcdsr"+NAME+"_ttN"+NAME+"Up"))
		shapes.append(Unroll(CR_Bnu, "CR"+NAME+"_qcdcr"+NAME+"_ttN"+NAME+"Up"))
		shapes.append(Unroll(SR_Bnd, "SR"+NAME+"_qcdsr"+NAME+"_ttN"+NAME+"Down"))
		shapes.append(Unroll(CR_Bnd, "CR"+NAME+"_qcdcr"+NAME+"_ttN"+NAME+"Down"))
		
		for i in range(NFITPAR):
			SR_Bu = outF.Get("SRrB_uncU_"+str(i)+"_data_"+name)
			SR_Bttu = outF.Get("SRrB_uncU_"+str(i)+"_ttbar_"+name)
			SR_Bu.Add(SR_Bttu, -1.)
			CR_Bu = outF.Get("CRrB_uncU_"+str(i)+"_data_"+name)
			CR_Bttu = outF.Get("CRrB_uncU_"+str(i)+"_ttbar_"+name)
			CR_Bu.Add(CR_Bttu, -1.)
			
			SR_Bd = outF.Get("SRrB_uncD_"+str(i)+"_data_"+name)
			SR_Bttd = outF.Get("SRrB_uncD_"+str(i)+"_ttbar_"+name)
			SR_Bd.Add(SR_Bttd, -1.)
			CR_Bd = outF.Get("CRrB_uncD_"+str(i)+"_data_"+name)
			CR_Bttd = outF.Get("CRrB_uncD_"+str(i)+"_ttbar_"+name)
			CR_Bd.Add(CR_Bttd, -1.)
			
			shapes.append(Unroll(SR_Bu, "SR"+NAME+"_qcdsr"+NAME+"_SRP"+str(i)+"Up"))
			shapes.append(Unroll(CR_Bu, "CR"+NAME+"_qcdcr"+NAME+"_CRP"+str(i)+"Up"))
			shapes.append(Unroll(SR_Bd, "SR"+NAME+"_qcdsr"+NAME+"_SRP"+str(i)+"Down"))
			shapes.append(Unroll(CR_Bd, "CR"+NAME+"_qcdcr"+NAME+"_CRP"+str(i)+"Down"))
		
		SR_S = outF.Get("SRrA_"+Sigs[3]+"_"+name)
		CR_S = outF.Get("CRrA_"+Sigs[3]+"_"+name)
		shapes.append(Unroll(SR_S, "SR"+NAME+"_Sig"))
		shapes.append(Unroll(CR_S, "CR"+NAME+"_Sig"))
		
		SSR = SR_S.Integral()
		SCR = CR_S.Integral()
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_SSR_", str(SSR))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_SCR_", str(SCR))
		
		
		for sys in SysWeighted:
			SuSysU = outF.Get("SRrA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			SuSysD = outF.Get("SRrA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			CuSysU = outF.Get("CRrA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			CuSysD = outF.Get("CRrA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			shapes.append(Unroll(SuSysU, "SR"+NAME+"_Sig_"+sys[0]+"Up"))
			shapes.append(Unroll(SuSysD, "SR"+NAME+"_Sig_"+sys[0]+"Down"))
			shapes.append(Unroll(CuSysU, "CR"+NAME+"_Sig_"+sys[0]+"Up"))
			shapes.append(Unroll(CuSysD, "CR"+NAME+"_Sig_"+sys[0]+"Down"))
			
		for sys in SysComputed:
			SuSysU = outF.Get("SRrA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			SuSysD = outF.Get("SRrA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			CuSysU = outF.Get("CRrA_"+Sigs[3]+"_"+sys[0]+"U_"+VAR[0]+"_"+VAR[3])
			CuSysD = outF.Get("CRrA_"+Sigs[3]+"_"+sys[0]+"D_"+VAR[0]+"_"+VAR[3])
			shapes.append(Unroll(SuSysU, "SR"+NAME+"_Sig_"+sys[0]+"Up"))
			shapes.append(Unroll(SuSysD, "SR"+NAME+"_Sig_"+sys[0]+"Down"))
			shapes.append(Unroll(CuSysU, "CR"+NAME+"_Sig_"+sys[0]+"Up"))
			shapes.append(Unroll(CuSysD, "CR"+NAME+"_Sig_"+sys[0]+"Down"))

		
		ShapesF = ROOT.TFile("SHAPES_"+Sigs[3]+name+".root", "recreate")
		ShapesF.cd()
		for x in shapes: x.Write()
		ShapesF.Write()
		ShapesF.Save()
		ShapesF.Close()
		
		# Replace our placeholders:
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_Y_", NAME)
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_name_", Sigs[3]+name)
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_lumU_", str(LUMIUNC))
		Template_Replace("CARD_"+Sigs[3]+name+".txt", "_bbSFU_", str(BBSFU))

		text_file = open("CARD_"+Sigs[3]+name+".txt", "a")
		for i in range(NFITPAR):
			text_file.write("SRP"+str(i)+" shapeN2    		         -             1.000         -			-			-			-\n")
			text_file.write("CRP"+str(i)+" shapeN2   	             -             -	         -			-			1.000			-\n")
		for sys in SysWeighted:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          1.000              -          -          \n")
		for sys in SysComputed:
			text_file.write(sys[0]+" shapeN2                      1.000              -          -          1.000              -          -          \n")
		text_file.close()
		
