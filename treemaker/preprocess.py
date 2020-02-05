#!/usr/bin/env python
import os
import sys
import ROOT
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *

def GetJSON(year):
    path = "/cms/xaastorage/PicoTrees/JSON_FILES/"
    if year == 2016: return path+"Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
    if year == 2017: return path+"Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
    if year == 2018: return path+"Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"

def preprocess(Inputs, OutputFolder, Year, Run, Triggers):
    JSON = None
    useModules = [PrefCorr()]
    if Run == "MC":
        jmeCorrectionsAK8 = createJMECorrector(True, Year, Run, "All", True, "AK8PFPuppi")
        useModules.append(jmeCorrectionsAK8())
        if Year == "2016":
            useModules.append(puWeight_2016())
        if Year == "2017":
            useModules.append(puWeight_2017())
        if Year == "2018":
            useModules.append(puWeight_2018())
    else:
        jmeCorrectionsAK8 = createJMECorrector(False, Year, Run, "Total", True, "AK8PFPuppi")
        useModules.append(jmeCorrectionsAK8())
        JSON = GetJSON(Year)

    preproc_cuts = "nFatJet>1&&PV_npvsGood>0&&("

    with open(Triggers) as triggers:
        ntrig = 0
        for trigger in triggers:
            if ntrig > 0: preproc_cuts += "||"
            preproc_cuts += trigger.rstrip()+">0"
            ntrig+=1
    preproc_cuts += ")"
    p = PostProcessor(OutputFolder, [Inputs], preproc_cuts, modules=useModules, provenance=False, outputbranchsel="keepfile.txt", jsonInput=JSON)
    p.run()

preprocess(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])