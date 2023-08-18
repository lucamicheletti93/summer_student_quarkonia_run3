import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf
import time
import concurrent.futures
import math
import numpy as np
import numpy
#ROOT.EnableImplicitMT()

start_time = time.time()

myfile = TFile('/media/lucas/ADATA SE760/CERN/AO2D_cut.root')
#myfile = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/data_new.root')
treeList = []

# Get the list of keys in the file

keys = myfile.GetListOfKeys()
#keys.pop()

hist_arr_mass = []
hist_arr_tauz = []

hm = ROOT.TH1F("hm","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm.SetMarkerStyle(ROOT.kFullCross)
hm.SetMarkerColor(ROOT.kBlue)
hm.SetMarkerSize(0.6)

hm_pp = ROOT.TH1F("hm_pp","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm_pp.SetMarkerStyle(ROOT.kFullCross)
hm_pp.SetMarkerColor(ROOT.kRed)
hm_pp.SetMarkerSize(0.6)

hm_mm = ROOT.TH1F("hm_mm","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm_mm.SetMarkerStyle(ROOT.kFullCross)
hm_mm.SetMarkerColor(ROOT.kRed)
hm_mm.SetMarkerSize(0.6)

ht = ROOT.TH1F("ht","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht.SetMarkerStyle(ROOT.kFullCross)
ht.SetMarkerColor(ROOT.kBlue)
ht.SetMarkerSize(0.6)

ht_pp = ROOT.TH1F("ht_pp","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht_pp.SetMarkerStyle(ROOT.kFullCross)
ht_pp.SetMarkerColor(ROOT.kRed)
ht_pp.SetMarkerSize(0.6)

ht_mm = ROOT.TH1F("ht_mm","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht_mm.SetMarkerStyle(ROOT.kFullCross)
ht_mm.SetMarkerColor(ROOT.kRed)
ht_mm.SetMarkerSize(0.6)

hm_cut = ROOT.TH1F("hm_cut","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm_cut.SetMarkerStyle(ROOT.kFullCross)
hm_cut.SetMarkerColor(ROOT.kRed)
hm_cut.SetMarkerSize(0.6)


ht_cut = ROOT.TH1F("ht_cut","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht_cut.SetMarkerStyle(ROOT.kFullCross)
ht_cut.SetMarkerColor(ROOT.kRed)
ht_cut.SetMarkerSize(0.6)

hm_bkg = ROOT.TH1F("hm_bkg","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm_bkg.SetMarkerStyle(ROOT.kFullCross)
hm_bkg.SetMarkerColor(ROOT.kGreen)
hm_bkg.SetMarkerSize(0.6)

hm_sig = ROOT.TH1F("hm_sig","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm_sig.SetMarkerStyle(ROOT.kFullCross)
hm_sig.SetMarkerColor(ROOT.kRed)
hm_sig.SetMarkerSize(0.6)

ht_bkg = ROOT.TH1F("ht_bkg","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht_bkg.SetMarkerStyle(ROOT.kFullCross)
ht_bkg.SetMarkerColor(ROOT.kGreen)
ht_bkg.SetMarkerSize(0.6)

ht_sig = ROOT.TH1F("ht_sig","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.01, 0.01)
ht_sig.SetMarkerStyle(ROOT.kFullCross)
ht_sig.SetMarkerColor(ROOT.kRed)
ht_sig.SetMarkerSize(0.6)


tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.01, 0.01)

accumulated_data = {
    'fMass': [],
    'fTauz': [],
    'fSign': [],
}

fIn_number = 3
counter = 0

# conds = (
#         "fMass >= 2 && fMass <= 5 &&"
#         "abs(fEta) >= 2.5 && abs(fEta) <= 4.0 && "
#         "abs(fEta1) >= 2.5 && abs(fEta1) <= 4.0 && "
#         "abs(fEta2) >= 2.5 && abs(fEta2) <= 4.0 && "
#         "(fChi2MatchMCHMFT1 <= 45 && fChi2MatchMCHMFT2 <= 45) &&"
#         #"fChi2pca >= 0")
#         "fPt >= 2 && fPt <= 10")

conds = (
    "!(fMass < 2 || fMass > 5 ||"
    "abs(fEta) < 2.5 || abs(fEta) > 4.0 || "
    "abs(fEta1) < 2.5 || abs(fEta1) > 4.0 || "
    "abs(fEta2) < 2.5 || abs(fEta2) > 4.0 || "
    "(fChi2MatchMCHMFT1 > 45 || fChi2MatchMCHMFT2 > 45) ||"
    #"fChi2pca < 0")
    "fPt < 4 || fPt > 6)")

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


    # print(len(accumulated_data['fMass']))
# global sum_fTauz
# sum_fTauz = 0
# def process_file(key):
#     obj_name = key.GetName()
#     if obj_name == 'parentFiles':
#         return

#     myTree = myfile.Get(obj_name+'/O2rtdimuonall;1')

#     # Create an RDataFrame from the tree and apply filtering conditions
#     rdf = ROOT.RDataFrame(myTree).Filter(conds)

#     # rdf = ROOT.RDataFrame(myTree)

#     # rdf =rdf.Filter('fSign == 0')
#     # rdf =rdf.Filter('abs(fEta) >= 2.5 && abs(fEta) <= 4.0')
#     # rdf =rdf.Filter('abs(fEta1) >= 2.5 && abs(fEta1) <= 4.0')
#     # rdf =rdf.Filter('abs(fEta2) >= 2.5 && abs(fEta2) <= 4.0')
#     # rdf =rdf.Filter('(fChi2MatchMCHMFT1 <= 40 || fChi2MatchMCHMFT2 <= 40)')
#     # rdf =rdf.Filter('fChi2pca >= 0')
#     # rdf =rdf.Filter('fPt >= 2')
#     # rdf =rdf.Filter('fPt1 >= 1.0')
#     # rdf =rdf.Filter('fPt2 >= 1.0')

#     data = rdf.AsNumpy(columns=["fMass", "fTauz", "fSign"])
#     accumulated_data['fMass'].extend(data["fMass"])
#     accumulated_data['fTauz'].extend(data["fTauz"])
#     accumulated_data['fSign'].extend(data["fSign"])
#     print("Number of events: ",len(accumulated_data['fMass']))


# with concurrent.futures.ThreadPoolExecutor(max_workers=len(keys)) as executor:
#     executor.map(process_file, keys)

#print("Final Sum of fTauz:", sum_fTauz)

# Fill histograms




for valm, valt, valsign in zip(accumulated_data['fMass'],accumulated_data['fTauz'],accumulated_data['fSign']):
    if valsign > 0:
        hm_pp.Fill(valm)
        ht_pp.Fill(valt)

    if valsign < 0:
        hm_mm.Fill(valm)
        ht_mm.Fill(valt)

    if valsign != 0: continue
    
    hm.Fill(valm)
    ht.Fill(valt)

    if (valm > 2.1 and valm < 2.5) or (valm > 4.1 and valm < 4.5):
    # if (valm > 1.5 and valm < 2):
        hm_cut.Fill(valm)
        ht_cut.Fill(valt)  

    counter +=1


# for i in range(fIn_number):
for iBin in range(1, hm.GetNbinsX() + 1):
    OS = hm.GetBinContent(iBin)
    SDOS = hm.GetBinError(iBin)
    PP = hm_pp.GetBinContent(iBin)
    SDPP = hm_pp.GetBinError(iBin)
    MM = hm_mm.GetBinContent(iBin)
    SDMM = hm_mm.GetBinError(iBin)
    GM = 2 * np.sqrt(PP * MM)
    SDGM = GM * ((SDPP / PP) + (SDMM / MM))
    hm_bkg.SetBinContent(iBin, GM)
    hm_bkg.SetBinError(iBin, SDGM)
    hm_sig.SetBinContent(iBin, OS - GM)
    hm_sig.SetBinError(iBin, np.sqrt(OS - GM))

for iBin in range(1, ht.GetNbinsX() + 1):
    OS = ht.GetBinContent(iBin)
    SDOS = ht.GetBinError(iBin)
    PP = ht_pp.GetBinContent(iBin)
    SDPP = ht_pp.GetBinError(iBin)
    MM = ht_mm.GetBinContent(iBin)
    SDMM = ht_mm.GetBinError(iBin)
    GM = 2 * np.sqrt(PP * MM)
    SDGM = GM * ((SDPP / PP) + (SDMM / MM))
    ht_bkg.SetBinContent(iBin, GM)
    ht_bkg.SetBinError(iBin, SDGM)
    ht_sig.SetBinContent(iBin, OS - GM)
    ht_sig.SetBinError(iBin, np.sqrt(OS - GM))

# for valt in accumulated_data['fTauz']:
#     ht.Fill(valt)

print("Number of envents: ",counter)

c1 = ROOT.TCanvas("c", "Fit Canvas", 1600, 900)
c1.Divide(2, 2)

c1.cd(1)
hm.Draw("P")
hm_bkg.Draw("P SAME")
hm_sig.Draw("P SAME")

c1.cd(2).SetLogy()
ht.Draw("P")
ht_bkg.Draw("P SAME")
ht_sig.Draw("P SAME")

c1.cd(3)
hm.Draw("P")
hm_cut.Draw("P SAME")

c1.cd(4).SetLogy()
ht.Draw("P")
ht_cut.Draw("P SAME")

c1.Draw()
c1.SaveAs("output_hists_data_new_tune_45_4-6_sign_plus.png")



c2 = ROOT.TCanvas("c", "Fit Canvas", 1600, 900)

#ht_bkg.Scale(1. / ht_bkg.Integral())
ht_bkg.Draw("P")
#ht_cut.Scale(1. / ht_cut.Integral())
ht_cut.Draw("P SAME")

c2.SetLogy()
c2.Draw()



c2.SaveAs("output_hists_data_new_tune_45_4-6_bkg_comp.png")

print(hm)

# fl1 = ROOT.TFile("hm_data_tune_45_4-6.root", "RECREATE")
# hm.Write()
# fl1.Close()

# fl2 = ROOT.TFile("ht_data_tune_45_4-6.root", "RECREATE")
# ht.Write()
# fl2.Close()

# fl3 = ROOT.TFile("hm_data_cut_tune_45_4-6.root", "RECREATE")
# hm_cut.Write()
# fl3.Close()

# fl4 = ROOT.TFile("ht_data_cut_tune_45_4-6.root", "RECREATE")
# ht_bg.Write()
# fl4.Close()

# fl5 = ROOT.TFile("hm_data_bg_tune_45_4-6.root", "RECREATE")
# hm_bg.Write()
# fl5.Close()

fl = ROOT.TFile("data_tune_45_4-6_sign_plus.root", "RECREATE")
hm.Write()
ht.Write()

hm_cut.Write()
ht_cut.Write()

hm_pp.Write()
hm_mm.Write()
ht_pp.Write()
ht_mm.Write()

hm_sig.Write()
hm_bkg.Write()

ht_sig.Write()
ht_bkg.Write()

fl.Close()


end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")