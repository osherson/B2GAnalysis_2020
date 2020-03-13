import os
import TEMPPAYLOAD
from TEMPPAYLOAD import *
os.system("convert results/"+NAME+"/*.png results/"+NAME+"/REPORT.pdf")
os.system("rm TEMPPAYLOAD.py")
