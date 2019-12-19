import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
########## PAYLOAD ########### Ask oshersonmarc@gmail.com for further clarification
NAME = "TEST" # THIS IS THE NAME OF THIS ANALYSIS

def MakeNBinsFromMinToMax(N,Min,Max): # helper for making large bin arrays makes N bins between Min and Max (same as you're feed to a TH1F)
	BINS = []
	for i in range(N+1):
		BINS.append(Min+(i*(Max-Min)/N))
	return BINS

# PLOTTING DETAILS:
# Luminosity to be displayed (in fb-1) at the top of plots
plot_lumi = 35.9
# CMS "preliminary", "simulation" or just CMS?
cmsextra = "Simulation"

# TTBAR REWEIGHTING:
# ----------------------------------- #
# recall that the ttbar is re-weighted as a function of the gen_tt_HT
# according to N * exp (- alpah * gen_tt_HT)
# the starting values for N and alpha are set here:
# (they will be naturally propagated into the weights below so you only have to change them here!)
N = 1.0
alpha = 0.0005
# ----------------------------------- #

# IS THIS DATA?
IsData = False

# BLIND THE RESULTS? (If true, will not create any plots that would unblind the analyis)
Blind = False

# The sum of these files will be used as the data:
DATA_FILES = [
				"/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/June2019/QCD/trig_800or900/2016_HTQCD_trigHT900.root",
				"/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/June2019/TTBAR/ttbar.root"
			]
NAME_OF_TREE = "tree_nominal"

# The sum of these files will be used as the ttbar, including where it needs to be subtracted from the "data"
TTBAR_FILES = [
				"/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/June2019/TTBAR/ttbar.root"
			]

# WEIGHTS:
# Note that the luminosity is explicitly set in the weight.
# (This is to combat situations where the weight stored in the trees isn't consistent: i.e. pb vs fb)

# Data weight (should always be 1.0)
DATA_WEIGHT = "1.0"
# QCD weight (don't  include the ttbar reweighting part, since this is applied automatically)
MC_WEIGHT = "36900.*weight_xsN*weight_PU"

# signals (these will not be summed, each signal is treated independently).
# The format for including these is ([FILE], WEIGHT, TREE, NAME, TITLE, XS),
# where TREE is the name of the TTree, the NAME is an internal convention for the code and the TITLE is what will be plotted in legends
# Finally, XS is the cross section in fb (this is for limit setting, so ideally it's the same as in the weight)
SIG = [
		[["/home/rek81/userArea/treemaker_version_May7/CMSSW_10_2_9/src/PICOTREES_WITH_TTBARvariables/June2019/Xaa_SIGNAL/X1000a50.root"],
			"10.0*36.9*weight_xsN*weight_PU",
			"tree_nominal",
			"X1000a50",
			"X_{1000} #rightarrow a_{50}a_{50}",
			10.0],
]
# Signal systematics: This section is a bit complicated.
# If a weight is stored in the weights structure, for example the PU weight, you can tell the code to make a shape systematic by adding something to the SysWeighted.
# NOTE: This code currently only supports signals that all share the same structure (so this will happen to all signals and will crash if that can't be done)
# The format for SysWeighted is [name of this systematic (has to be on word, no _/-/spaces so it can be used in a combine card), weight FACTOR Up, weight FACTOR down]
# FACTOR here is what to CHANGE the original weight by (this way we don't forget to change things in multiple places).
# Finally, give it a name you want to see in a legend (name for the systematic)
SysWeighted = 	[
					["PU", "weight_PU_up/weight_PU", "weight_PU_dn/weight_PU", "Pileup Uncertainty"]
				]
# Systematics kept in separate trees are done in the SysComputed, which has exactly the same format, except now you tell it what the up/down trees are for
# that systematic
SysComputed = 	[
					["JER", "tree_jer_up", "tree_jer_down", "Jet Energy Resolution Uncertainty"],
					["JES", "tree_jes_up", "tree_jes_down", "Jet Energy Scale Uncertainty"]
				]

## VARIABLES
# All these need to be (varname, bins, title) where the varname is the branch name in the TTree and the bins edges need to be specified. Title is what the axis will read
# If you want to use fixed binning, you can use the helper function above (MakeNBinsFromMinToMax(N, min, max) ) which takes N = number of bins, min and max are the min and max.

# Fit Var:
FitVarBins = [10.,15.,20.,25.,30.,35.,40.,45.,50.,60.,70.,80.,90.,100.,125.,150.,200.,250.,300.,400.]
FitVar = ("J2SDM", FitVarBins, "Subleading Jet Soft Drop Mass (GeV)")

# Est Vars: Each of these will be estimated (the difference between spectators and not spectators is redundant now).
# The last bool is whether or not to create a combine card from this variable!
XVarBins = MakeNBinsFromMinToMax(50,800.,2800.)
HTVarBins = MakeNBinsFromMinToMax(40,900.,2900.)
jmBins = MakeNBinsFromMinToMax(50,15.,265.)
etaBins = MakeNBinsFromMinToMax(20,-3.,3.)
pTBins = MakeNBinsFromMinToMax(50,300.,1800.)
EstVars = 	[
				("evt_aM", jmBins, "Average Jet Mass (GeV)", True),
				#("evt_HT", HTVarBins, "Event HT (GeV)", False),
				#("J1SDM", jmBins, "Leading Jet Soft Drop Mass (GeV)", False),
				#("J2SDM", jmBins, "Subleading Jet Soft Drop Mass (GeV)", False),
				#("J1pt", pTBins, "Leading Jet p_{T} (GeV)", False),
				#("J2pt", pTBins, "Subleading Jet p_{T} (GeV)", False),
				#("J1eta", etaBins, "Leading Jet #eta", False),
				#("J2eta", etaBins, "Subleading #eta", False),
				#("evt_XM", XVarBins, "Dijet Mass (GeV)", False),
			]

# 2D Vars: These combinations will be processed as 2D hists and also unrolled.
# Format as "treename, bins, title, othertreename, otherbins, othertitle"
# The last bool is whether or not to create a combine card from this variable!
#X2DVarBins = MakeNBinsFromMinToMax(15,800.,2300.)
#jm2DBins = MakeNBinsFromMinToMax(15,15.,265.)
X2DVarBins = [800.,900.,1000.,1100.,1200.,1300.,1400.,1500.,1750.,2000.,2500.]
jm2DBins = [15.,20.,25.,30.,35.,40.,45.,50.,60.,70.,80.,90.,100.,125.,150.,200.,300.]
eta2DBins = MakeNBinsFromMinToMax(6,-3.,3.)

EstVars2D = [
				["evt_XM", X2DVarBins, "Dijet Mass (GeV)", "evt_aM", jm2DBins, "Average Jet Mass (GeV)", True],
				#["J1eta", eta2DBins, "Leading Jet #eta","J2eta", eta2DBins, "Subleading #eta", False],
				#["J1SDM", jm2DBins, "Leading Jet Soft Drop Mass (GeV)","J2SDM", jm2DBins, "Subleading Jet Soft Drop Mass (GeV)", False]
			]

## CUTS (all these need to be in RDF format: && instead of just &)
#Preselection (will be applied to ALL plots produced by this code)
PRESELECTION = "J1dbtag>0.6 && evt_HT>900 && J2pt>300 && evt_Masym>0.0 && evt_Masym<0.1"
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


### THE FIT: Define and initialize your fit here.
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

### COMBINE OPTIONS:
# NTOYS is the number of toys for statistical tests, bias tests, etc. Large numbers = better results but will run slower
NTOYS = 100
# Extra Combine options for intial computation. This in case combine needs a little fidgiting. Probably ask Marc about this!
EXTRACOMBINEOPTION = "--setParameters P0=0.25"

























# DO NOT MODIFY ANYTHING BELOW THIS LINE:
#-------------------------------------------------------------------------------------------------------------------------------------
			# Set things up based on the payload:
###################################################
MC_WEIGHT_NOM = MC_WEIGHT +"*"+str(N)+"*exp(evt_ttRW*-"+str(alpha)+")"
MC_WEIGHT_AU = MC_WEIGHT +"*"+str(N)+"*exp(evt_ttRW*-"+str(alpha*0.8)+")"
MC_WEIGHT_AD = MC_WEIGHT +"*"+str(N)+"*exp(evt_ttRW*-"+str(alpha*1.2)+")"
MC_WEIGHT_NU = MC_WEIGHT +"*"+str(N*1.2)+"*exp(evt_ttRW*-"+str(alpha)+")"
MC_WEIGHT_ND = MC_WEIGHT +"*"+str(N*0.8)+"*exp(evt_ttRW*-"+str(alpha)+")"

if IsData:
	DATA = (DATA_FILES, DATA_WEIGHT, NAME_OF_TREE)
else:
	DATA = (DATA_FILES, MC_WEIGHT_NOM, NAME_OF_TREE)

TTBAR = (TTBAR_FILES, MC_WEIGHT_NOM, NAME_OF_TREE)
TTBAR_AU = (TTBAR_FILES, MC_WEIGHT_AU, NAME_OF_TREE)
TTBAR_AD = (TTBAR_FILES, MC_WEIGHT_AD, NAME_OF_TREE)
TTBAR_NU = (TTBAR_FILES, MC_WEIGHT_NU, NAME_OF_TREE)
TTBAR_ND = (TTBAR_FILES, MC_WEIGHT_ND, NAME_OF_TREE)

RegA = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + ExSigCuts
RegB = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + pass_ABvCD + "&&" + ExSigCuts
RegC = PRESELECTION + " && " + VAR_ACvBD[0] + pass_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD
RegD = PRESELECTION + " && " + VAR_ACvBD[0] + fail_ACvBD + " && " + VAR_ABvCD[0] + fail_ABvCD
