import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf
import time
import concurrent.futures
#ROOT.EnableImplicitMT()

start_time = time.time()

myfile = TFile('/media/lucas/ADATA SE760/CERN/AO2D.root')
#myfile = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/data_new.root')
treeList = []

# Get the list of keys in the file

keys = myfile.GetListOfKeys()
#keys.pop()

hist_arr_mass = []
hist_arr_tauz = []

hm = ROOT.TH1F("hm","Dimuon mass ;m (GeV/c^2);#", 100, 2, 5)
hm.SetMarkerStyle(ROOT.kFullCross)
hm.SetMarkerColor(ROOT.kRed)
hm.SetMarkerSize(0.6)


ht = ROOT.TH1F("ht","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.003, 0.003)
ht.SetMarkerStyle(ROOT.kFullCross)
ht.SetMarkerColor(ROOT.kRed)
ht.SetMarkerSize(0.6)


hm_cut = ROOT.TH1F("hm_cut","Dimuon mass ;m (GeV/c^2);#", 100, 2, 5)
hm_cut.SetMarkerStyle(ROOT.kFullCross)
hm_cut.SetMarkerColor(ROOT.kRed)
hm_cut.SetMarkerSize(0.6)


ht_bg = ROOT.TH1F("ht_bg","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.003, 0.003)
ht_bg.SetMarkerStyle(ROOT.kFullCross)
ht_bg.SetMarkerColor(ROOT.kRed)
ht_bg.SetMarkerSize(0.6)

hm_bg = ROOT.TH1F("hm_bg","Dimuon mass ;m (GeV/c^2);#", 100, 0, 10)
hm_bg.SetMarkerStyle(ROOT.kFullCross)
hm_bg.SetMarkerColor(ROOT.kRed)
hm_bg.SetMarkerSize(0.6)


accumulated_data = {
    'fMass': [],
    'fTauz': [],
}


counter = 0

conds = ("fSign == 0 && "
        "abs(fEta) >= 2.5 && abs(fEta) <= 4.0 && "
        "abs(fEta1) >= 2.5 && abs(fEta1) <= 4.0 && "
        "abs(fEta2) >= 2.5 && abs(fEta2) <= 4.0 && "
        "(fChi2MatchMCHMFT1 <= 45 && fChi2MatchMCHMFT2 <= 45) && "
        "fChi2pca >= 0 && "
        "fPt >= 4 && fPt <= 6")



# for key in keys:
#     obj_name = key.GetName()
#     if obj_name == 'parentFiles':
#         continue

#     myTree = myfile.Get(obj_name+'/O2rtdimuonall;1')

#     # Define filter conditions
    
#     rdf = ROOT.RDataFrame(myTree).Filter(conds)


#     data = rdf.AsNumpy(columns=["fMass", "fTauz"])
#     accumulated_data['fMass'].extend(data["fMass"])
#     accumulated_data['fTauz'].extend(data["fTauz"])


    # print(len(accumulated_data['fMass']))

def process_file(key):
    obj_name = key.GetName()
    if obj_name == 'parentFiles':
        return

    myTree = myfile.Get(obj_name+'/O2rtdimuonall;1')

    # Create an RDataFrame from the tree and apply filtering conditions
    rdf = ROOT.RDataFrame(myTree).Filter(conds)

    # rdf = ROOT.RDataFrame(myTree)

    # rdf =rdf.Filter('fSign == 0')
    # rdf =rdf.Filter('abs(fEta) >= 2.5 && abs(fEta) <= 4.0')
    # rdf =rdf.Filter('abs(fEta1) >= 2.5 && abs(fEta1) <= 4.0')
    # rdf =rdf.Filter('abs(fEta2) >= 2.5 && abs(fEta2) <= 4.0')
    # rdf =rdf.Filter('(fChi2MatchMCHMFT1 <= 40 || fChi2MatchMCHMFT2 <= 40)')
    # rdf =rdf.Filter('fChi2pca >= 0')
    # rdf =rdf.Filter('fPt >= 2')
    # rdf =rdf.Filter('fPt1 >= 1.0')
    # rdf =rdf.Filter('fPt2 >= 1.0')

    data = rdf.AsNumpy(columns=["fMass", "fTauz"])
    accumulated_data['fMass'].extend(data["fMass"])
    accumulated_data['fTauz'].extend(data["fTauz"])
    print("Number of events: ",len(accumulated_data['fMass']))

with concurrent.futures.ThreadPoolExecutor(max_workers=len(keys)) as executor:
    executor.map(process_file, keys)

# Fill histograms
for valm, valt in zip(accumulated_data['fMass'],accumulated_data['fTauz']):
    
    hm.Fill(valm)
    ht.Fill(valt)
    
    if (valm > 2.1 and valm < 2.5) or (valm > 4.1 and valm < 4.5):
        hm_cut.Fill(valm)

        

    if valm < 2.9 or valm > 3.2:
        hm_bg.Fill(valm)
        ht_bg.Fill(valt) 
    
    counter +=1

# for valt in accumulated_data['fTauz']:
#     ht.Fill(valt)

print("Number of envents: ",counter)

c = ROOT.TCanvas()
c.Divide(2, 1)

c.cd(1)
hm.Draw("P")

c.cd(2)
ht.Draw("P")


c.Draw()
c.SaveAs("output_hists_data_new_tune_45_4-6.png")
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

fl = ROOT.TFile("data_tune_45_4-6.root", "RECREATE")
hm.Write()
hm_cut.Write()
hm_bg.Write()
ht.Write()
ht_bg.Write()
fl.Close()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")