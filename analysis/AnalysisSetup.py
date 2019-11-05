import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

			#  import the payload, spit an error
			#  if you can't find it
###################################################
try:
	import TEMPPAYLOAD
	from TEMPPAYLOAD import *
except:
	print ">>ERROR IMPORTING PAYLOAD!<<"


######### Just making sure in case the user notices a mistake:
print "ABCD regions defined as follows:"
print RegA
print RegB
print RegC
print RegD

			#  Create the results file which will
			#  be added to in each step.
###################################################

try:
    os.stat("../results/"+NAME)
except:
    os.mkdir("../results/"+NAME)       

outF = ROOT.TFile("../results/"+NAME+"/Analysis_"+NAME+".root", "recreate")
outF.Save()
outF.Write()