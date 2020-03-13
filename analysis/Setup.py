import os
import TEMPPAYLOAD
from TEMPPAYLOAD import *
try: # create or recreate the output folder in "results"
    os.stat("results/"+NAME)
    os.system("rm -rf results/"+NAME)
    os.mkdir("results/"+NAME) 
except:
    os.mkdir("results/"+NAME)       
F = ROOT.TFile("results/"+NAME+"/Debubg_"+NAME+".root", "recreate") # Master plots file which can be used to debug and serves as storage for ROOT objects sbetween between scripts
F.Save()
F.Write()
