import PyFunctions
from PyFunctions import *
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
#### TEST PAYLOAD FOR DEVELOPMENT: DO NOT MODIFY TO RUN ANALYSIS! MAKE A COPY SO ALL STEPS ARE UNDERSTOOD!
# email oshersonmarc@gmail.com for questions
#####--------------------------------------------------------
###################################
###			SOME SETUP			###
###################################
# Name this payload (this is the name that will be used for all files)
NAME = "TEST"
# Luminosity (in fb):
LUMI = 35.9
LUMIUNC = 1.025
BBSFU = 1.10
# IS THIS DATA?
IsData = False
# BLIND THE RESULTS? (If true, will not create any plots that would unblind the analyis)
Blind = False
###################################
###			INPUT FILES			###
###################################
# The sum of these files will be used as the "data":
DATA_FILES = 	[
				"/home/rek81/userArea/TreeMaker_Jan31/CMSSW_10_6_2/src/ABCD_multivar/treemaker/treemaker_trial2/2017_QCDHT_test.root", "/home/rek81/userArea/TreeMaker_Jan31/CMSSW_10_6_2/src/ABCD_multivar/treemaker/treemaker_trial2/2017_ttbar_test.root"
				]
# The sum of these files will be used as the ttbar:
TTBAR_FILES = 	[
				"/home/rek81/userArea/TreeMaker_Jan31/CMSSW_10_6_2/src/ABCD_multivar/treemaker/treemaker_trial2/2017_ttbar_test.root"
				]
###################################
###			SIGNAL INPUTS		###
###################################
# signals (these will not be summed, each signal is treated independently).
# The format for including these is ([FILE], WEIGHT, TREE, NAME, TITLE, XS),
# where TREE is the name of the TTree, the NAME is an internal convention for the code and the TITLE is what will be plotted in legends
SIG = [
		[["/home/rek81/userArea/TreeMaker_Jan31/CMSSW_10_6_2/src/ABCD_multivar/2016_Treemaker/treemaker_test1/2016_X1500a50.root"],
			"10.0*36.9*weight_xsN*weight_PU",
			"tree_nominal",
			"X1000a50",
			"X_{1000} #rightarrow a_{50}a_{50}"],
]
# Signal systematics: This section is a bit complicated.
# If a weight is stored in the weights structure, for example the PU weight, you can tell the code to make a shape systematic by adding something to the SysWeighted.
# NOTE: This code currently only supports signals that all share the same structure (so this will happen to all signals and will crash if that can't be done)
# The format for SysWeighted is [name of this systematic (has to be on word, no _/-/spaces so it can be used in a combine card), weight FACTOR Up, weight FACTOR down]
# FACTOR here is what to CHANGE the original weight by (this way we don't forget to change things in multiple places).
# Give it a name you want to see in a legend (name for the systematic), and finally, True/False this should apply to ttbar as well?
SysWeighted = 	[["PU", "weight_PU_up/weight_PU", "weight_PU_dn/weight_PU", "Pileup Uncertainty", True]]
# Systematics kept in separate trees are done in the SysComputed, which has exactly the same format, except now you tell it what the up/down trees are for
# that systematic
SysComputed = 	[["JER", "tree_jer_up", "tree_jer_down", "Jet Energy Resolution Uncertainty", True],
					["JES", "tree_jes_up", "tree_jes_down", "Jet Energy Scale Uncertainty", True]]
###################################
###			FIT VARIABLES		###
###################################
# This is the variable being fit in the ABCD methods. It needs to be (varname, bins, title) where the varname is the branch name in the TTree and the bins edges need to be specified. Title is what the axis will read
# *If you want to use fixed binning, you can use the helper function above (MakeNBinsFromMinToMax(N, min, max) )*
FitVarBins = [10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,70.,80.,90.,100.,125.,150.,200.,250.,300.,400.]
FitVar = ("J2SDM", FitVarBins, "Subleading Jet Soft Drop Mass (GeV)")
###################################
###			LIMIT VARIABLES		###
###################################
# 2D Vars: These combinations will be processed as unrolled histograms.
# Format as "varname, bins, title, othervarname, otherbins, othertitle"
# The last bool is whether or not to create a combine card from this variable!
#X2DVarBins = MakeNBinsFromMinToMax(15,800.,2300.)
jmBins = MakeNBinsFromMinToMax(15,15.,265.)
XBins = [800.,900.,1000.,1100.,1200.,1300.,1400.,1500.,1750.,2000.,2500.,4000.]

EstVars = [
				["evt_XM", XBins, "Dijet Mass (GeV)", "evt_aM", jmBins, "Average Jet Mass (GeV)", True]
			]
###################################
###		REGIONS AND CUTS		###
###################################
#Preselection (will be applied to ALL plots produced by this code)
PRESELECTION = "J1dbtag>0.6 && evt_HT>900 && J2pt>300"
SR = "evt_Masym>0.0 && evt_Masym<0.1" # Specify the signal region.
CR = "evt_Masym>0.2 && evt_Masym<0.3" # Specify the ttbar control region
# What variable do we use to separate region A and C from B and D?
VAR_ACvBD = ("J2dbtag", MakeNBinsFromMinToMax(20, -1.,1.), "Subleading Jet Double-B Score") # Same format as the FitVar
# What cut do you apply to it (define the passing and failing requirement))?
pass_ACvBD = ">0.6"
fail_ACvBD = "<0.6"
# What variable do we use to separate region A and B from C and D?
VAR_ABvCD = ("evt_Deta", MakeNBinsFromMinToMax(20,0.,4.), "#Delta#eta") # Same format as the FitVar
# What cut do you apply to it (define the passing and failing requirement)?
pass_ABvCD = "<1.5"
fail_ABvCD = ">1.5"
# Are there any extra cuts on the signal region you would like to use? (e.g. if you want to measure the rate in a region with more statistics)
ExSigCuts = "J1dbtag>0.8 && J2SDM > 12.5"
###################################
###			FIT DETAILS			###
###################################
# We'll need to know the number of parameters in the fit. Needs to match what you define below.
NFITPAR = 4
# Notice that it needs to be a function that returns a fit (so we can make many of them)
import math
def Atan(xx, p):
    x=-1*xx[0]
    return math.atan(x*p[0]+p[1])*p[2] + p[3]
def FIT(name):
	myFit = ROOT.TF1(name, Atan, 10.,415., 4)
	myFit.SetParameters(0.20,-20.,2.0,3.0)
	return myFit

# DO NOT MODIFY ANYTHING BELOW THIS LINE:
#-------------------------------------------------------------------------------------------------------------------------------------
SR_A = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + SR + "&&" + ExSigCuts
SR_B = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + SR + "&&" + ExSigCuts
SR_C = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD + "&&" + SR
SR_D = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD + "&&" + SR
CR_A = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + CR + "&&" + ExSigCuts
CR_B = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + CR + "&&" + ExSigCuts
CR_C = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD + "&&" + CR
CR_D = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD + "&&" + CR

MC_WEIGHT = str(1000 * LUMI) + "*weight_xsN*weight_PU"

MC_WEIGHT_NOM = MC_WEIGHT +"*exp(evt_ttRW*-0.0005)"
MC_WEIGHT_AU = MC_WEIGHT
MC_WEIGHT_AD = MC_WEIGHT +"*(2*exp(evt_ttRW*-0.0005))"
MC_WEIGHT_NU = MC_WEIGHT +"*1.2*exp(evt_ttRW*-0.0005)"
MC_WEIGHT_ND = MC_WEIGHT +"*0.8*exp(evt_ttRW*-0.0005)"

if IsData:
	DATA = (DATA_FILES, "1.0", "tree_nominal")
else:
	DATA = (DATA_FILES, MC_WEIGHT_NOM, "tree_nominal")

TTBAR = (TTBAR_FILES, MC_WEIGHT_NOM, "tree_nominal")
TTBAR_AU = (TTBAR_FILES, MC_WEIGHT_AU, "tree_nominal")
TTBAR_AD = (TTBAR_FILES, MC_WEIGHT_AD, "tree_nominal")
TTBAR_NU = (TTBAR_FILES, MC_WEIGHT_NU, "tree_nominal")
TTBAR_ND = (TTBAR_FILES, MC_WEIGHT_ND, "tree_nominal")

if IsData: cmsextra = "Preliminary"
else: cmsextra = "Simulation"
