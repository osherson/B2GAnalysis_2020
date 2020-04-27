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

# JEC dict
jecTagsMC = {'2016' : 'Summer16_07Aug2017_V11_MC', 
             '2017' : 'Fall17_17Nov2017_V32_MC', 
             '2018' : 'Autumn18_V19_MC'}

jecTagsFastSim = {'2016' : 'Summer16_FastSimV1_MC',
                  '2017' : 'Fall17_FastSimV1_MC',
                  '2018' : 'Autumn18_FastSimV1_MC'}

archiveTagsDATA = {'2016' : 'Summer16_07Aug2017_V11_DATA', 
                   '2017' : 'Fall17_17Nov2017_V32_DATA', 
                   '2018' : 'Autumn18_V19_DATA'
                  }

jecTagsDATA = { '2016B' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016C' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016D' : 'Summer16_07Aug2017BCD_V11_DATA', 
                '2016E' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016F' : 'Summer16_07Aug2017EF_V11_DATA', 
                '2016G' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2016H' : 'Summer16_07Aug2017GH_V11_DATA', 
                '2017B' : 'Fall17_17Nov2017B_V32_DATA', 
                '2017C' : 'Fall17_17Nov2017C_V32_DATA', 
                '2017D' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017E' : 'Fall17_17Nov2017DE_V32_DATA', 
                '2017F' : 'Fall17_17Nov2017F_V32_DATA', 
                '2018A' : 'Autumn18_RunA_V19_DATA',
                '2018B' : 'Autumn18_RunB_V19_DATA',
                '2018C' : 'Autumn18_RunC_V19_DATA',
                '2018D' : 'Autumn18_RunD_V19_DATA',
                } 

jerTagsMC = {'2016' : 'Summer16_25nsV1_MC',
             '2017' : 'Fall17_V3_MC',
             '2018' : 'Autumn18_V7_MC'
            }

#jet mass resolution: https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging
#nominal, up, down
jmrValues = {'2016' : [1.0, 1.2, 0.8],
             '2017' : [1.09, 1.14, 1.04],
             '2018' : [1.24, 1.20, 1.28]
            }

#jet mass scale
#W-tagging PUPPI softdrop JMS values: https://twiki.cern.ch/twiki/bin/view/CMS/JetWtagging
#2016 values 
jmsValues = { '2016' : [1.00, 0.9906, 1.0094], #nominal, down, up
              '2017' : [0.982, 0.978, 0.986],
              '2018' : [0.997, 0.993, 1.001]
            }


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
