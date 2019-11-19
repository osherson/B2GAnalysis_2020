import PyFunctions
from PyFunctions import *
import TEMPPAYLOAD
from TEMPPAYLOAD import *
import os

print "RUNNING COMBINE CARDS: "
for Sigs in SIG:
	for VAR in EstVars:
		cardname = VAR[0]+"_"+Sigs[3]
		print "Running combine for:   " + cardname
		