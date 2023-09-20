import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf
import time
import concurrent.futures
import math
import numpy as np
import numpy

start_time = time.time()

#myfile = TFile('/Users/lucamicheletti/cernbox/summer_student_quarkonia_run3/data/LHC22o/AO2D.root')
#myfile = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/data_new.root')
myfile = TFile('/media/lucas/ADATA SE760/CERN/AO2D_cut.root')
treeList = []

# Get the list of keys in the file

keys = myfile.GetListOfKeys()


ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]

hMass = ROOT.TH1F("hMass","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hMassPP = ROOT.TH1F("hMassPP","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hMassMM = ROOT.TH1F("hMassMM","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hTauz = ROOT.TH1F("hTauz","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hTauzPP = ROOT.TH1F("hTauzPP","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hTauzMM = ROOT.TH1F("hTauzMM","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hMassSideBand = ROOT.TH1F("hMassSideBand","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hTauSideBand = ROOT.TH1F("hTauSideBand","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hMassBkg = ROOT.TH1F("hMassBkg","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hMassSig = ROOT.TH1F("hMassSig","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hTauzBkg = ROOT.TH1F("hTauzBkg","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hTauzSig = ROOT.TH1F("hTauzSig","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hMassNoPeak = ROOT.TH1F("hMassNoPeak","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)

hMass  = []
hMassPP  = []
hMassMM  = []
hTauz = []
hTauzPP = []
hTauzMM  = []
hMassSideBand = []
hTauzSideBand  = []
hMassBkg = []
hMassSig = []
hTauzBkg = []
hTauzSig = []
hMassNoPeak = []

for iPt in range(0, len(ptMin)):
    hMass.append(ROOT.TH1F("hMass_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassPP.append(ROOT.TH1F("hMassPP_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassMM.append(ROOT.TH1F("hMassMM_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hTauz.append(ROOT.TH1F("hTauz_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzPP.append(ROOT.TH1F("hTauzPP_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzMM.append(ROOT.TH1F("hTauzMM_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hMassSideBand.append(ROOT.TH1F("hMassSideBand_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hTauzSideBand.append(ROOT.TH1F("hTauzSideBand_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hMassBkg.append(ROOT.TH1F("hMassBkg_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassSig.append(ROOT.TH1F("hMassSig_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hTauzBkg.append(ROOT.TH1F("hTauzBkg_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzSig.append(ROOT.TH1F("hTauzSig_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hMassNoPeak.append(ROOT.TH1F("hMassNoPeak_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))


    accumulated_data = {
        'fMass': [],
        'fTauz': [],
        'fSign': [],
    }

    fIn_number = 3
    counter = 0


    conds = (
        "!(fMass < 2 || fMass > 5 ||"
        "abs(fEta) < 2.5 || abs(fEta) > 4.0 || "
        "abs(fEta1) < 2.5 || abs(fEta1) > 4.0 || "
        "abs(fEta2) < 2.5 || abs(fEta2) > 4.0 || "
        "(fChi2MatchMCHMFT1 > 45 || fChi2MatchMCHMFT2 > 45) ||"
        #f"fPt < {ptMin[iPt]} || fPt > {ptMax[iPt]} ||"
        "fPt < 0 || fPt > 2 ||"
        "abs(fTauz) > 0.007 )")

    for key in keys:
        obj_name = key.GetName()
        if obj_name == 'parentFiles':
            continue

        myTree = myfile.Get(obj_name+'/O2rtdimuonall;1')

        # Define filter conditions
        
        rdf = ROOT.RDataFrame(myTree).Filter(conds)


        data = rdf.AsNumpy(columns=["fMass", "fTauz", "fSign"])
        accumulated_data['fMass'].extend(data["fMass"])
        accumulated_data['fTauz'].extend(data["fTauz"])
        accumulated_data['fSign'].extend(data["fSign"])



    for valm, valt, valsign in zip(accumulated_data['fMass'],accumulated_data['fTauz'],accumulated_data['fSign']):
        if valsign > 0:
            hMassPP[iPt].Fill(valm)
            hTauzPP[iPt].Fill(valt)

        if valsign < 0:
            hMassMM[iPt].Fill(valm)
            hTauzMM[iPt].Fill(valt)

        if valsign != 0: continue
        
        hMass[iPt].Fill(valm)
        hTauz[iPt].Fill(valt)

        if valm < 2.7 or valm > 3.4:
            hMassNoPeak[iPt].Fill(valm)

        if (valm > 2.1 and valm < 2.5) or (valm > 4.1 and valm < 4.5):
            hMassSideBand[iPt].Fill(valm)
            hTauzSideBand[iPt].Fill(valt)  

        counter +=1

    for iBin in range(1, hMass[iPt].GetNbinsX() + 1):
        OS = hMass[iPt].GetBinContent(iBin)
        SDOS = hMass[iPt].GetBinError(iBin)
        PP = hMassPP[iPt].GetBinContent(iBin)
        SDPP = hMassPP[iPt].GetBinError(iBin)
        MM = hMassMM[iPt].GetBinContent(iBin)
        SDMM = hMassMM[iPt].GetBinError(iBin)
        GM = 2 * np.sqrt(PP * MM)
        SDGM = GM * ((SDPP / PP) + (SDMM / MM))
        hMassBkg[iPt].SetBinContent(iBin, GM)
        hMassBkg[iPt].SetBinError(iBin, SDGM)
        hMassSig[iPt].SetBinContent(iBin, OS - GM)
        hMassSig[iPt].SetBinError(iBin, np.sqrt(OS - GM))

    for iBin in range(1, hTauz[iPt].GetNbinsX() + 1):
        OS = hTauz[iPt].GetBinContent(iBin)
        SDOS = hTauz[iPt].GetBinError(iBin)
        PP = hTauzPP[iPt].GetBinContent(iBin)
        SDPP = hTauzPP[iPt].GetBinError(iBin)
        MM = hTauzMM[iPt].GetBinContent(iBin)
        SDMM = hTauzMM[iPt].GetBinError(iBin)
        GM = 2 * np.sqrt(PP * MM)
        SDGM = GM * ((SDPP / PP) + (SDMM / MM))
        hTauzBkg[iPt].SetBinContent(iBin, GM)
        hTauzBkg[iPt].SetBinError(iBin, SDGM)
        hTauzSig[iPt].SetBinContent(iBin, OS - GM)
        hTauzSig[iPt].SetBinError(iBin, np.sqrt(OS - GM))



    fl = ROOT.TFile("data.root", "RECREATE")
    hMass[iPt].Write()
    hTauz[iPt].Write()

    hMassSideBand[iPt].Write()
    hTauzSideBand[iPt].Write()

    hMassPP[iPt].Write()
    hMassMM[iPt].Write()
    hTauzPP[iPt].Write()
    hTauzMM[iPt].Write()

    hMassSig[iPt].Write()
    hMassBkg[iPt].Write()

    hTauzSig[iPt].Write()
    hTauzBkg[iPt].Write()

    hMassNoPeak[iPt].Write()

    fl.Close()


end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")