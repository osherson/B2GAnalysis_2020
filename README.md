# Install:

cmsrel CMSSW_10_6_2
cd CMSSW_10_6_2/src
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cmsenv
scram b -j8
git clone https://github.com/osherson/ABCD_multivar.git
mkdir results

# Running (Treemaker):
This code (in the treemaker folder) turns nanoAOD into useable picotrees.

source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]
- ouput: Name of the output file (must be unique)
- inputPath: path to the nanoAOd. Can inlude wildcards if you want to run over a subset of files
- goBetween: path to a folder you can store intermediate nanoSkims (so womewhere you have space to store some large-ish files)
- year: dataset year
- Run/MC: if this is data, the run period, if this is MC, just write "MC"
- TriggerList: text file containing the names of the triggers you want to keep
- weight: 1 for data, cross-section for MC

Example (MC):
source MakeNano.sh X1000a50 /cms/xaastorage/NanoAOD/2016/JUNE19/Xaa_Signal/X1000a50/ /cms/osherson/NanoToolOutput 2016 MC triglist.txt 9.8
Example (Data, just running on one file):
source MakeNano.sh Data16C /cms/xaastorage/NanoAOD/2016/JUNE19/JetHT_DATA/Run2016C/910727BA-1093-0343-B569-CD480F6CCC7F /cms/osherson/NanoToolOutput 2016 C triglist.txt 1

source MakeNano.sh X1000a50 /cms/xaastorage/NanoAOD/2016/JUNE19/Xaa_Signal/X1000a50/ /cms/osherson/NanoToolOutput 2016 MC triglist.txt 1
# Running (Analysis):

The code can be launched in the "analysis" folder by doing.

./LaunchAnalysis.sh [path-to-payload]

- Marc
