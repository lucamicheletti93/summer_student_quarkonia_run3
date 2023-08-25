import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf

myfile = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/MC_prompt_jpsi_update.root')
myfile_non = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/MC_non_prompt_jpsi_update.root')
treeList = []

# Get the list of keys in the file

keys = myfile.GetListOfKeys()
keys.pop()

keys_non = myfile_non.GetListOfKeys()
keys_non.pop()

hist_arr_mass = []
hist_arr_non_mass = []
hist_arr_tauz = []
hist_arr_non_tauz = []
# Iterate over the keys and print the object names

for key in keys:
    obj_name = key.GetName()
    myTree = myfile.Get(obj_name+'/O2rtdimuonall;1')
    branch_list = myTree.GetListOfBranches()
    fMass = 'fMass'
    fTauz = 'fTauz'
    
    #restrictions = ['fEta', 'fEta1', 'fEta2', 'fChi2MatchMCHMID1', 'fChi2MatchMCHMID2']
    
    for e in myTree:
        fSign = getattr(e, 'fSign')
        fEta = getattr(e, 'fEta')
        fEta1 = getattr(e, 'fEta1')
        fEta2 = getattr(e, 'fEta2')
        fChi2MatchMCHMFT1 = getattr(e, 'fChi2MatchMCHMFT1')
        fChi2MatchMCHMFT2= getattr(e, 'fChi2MatchMCHMFT2')
        fChi2pca = getattr(e, 'fChi2pca')
        fPt = getattr(e, 'fPt')
        fTauzTemp = getattr(e, 'fTauz')
        fMcDecision = getattr(e, 'fMcDecision')

        if fMcDecision == 1: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        if fChi2pca < 0: continue
        if fPt < 4 or fPt > 6: continue
        if abs(fTauzTemp) > 0.007: continue
            
        valm = getattr(e, fMass)
        valt = getattr(e, fTauz)

        if valm < 2 or valm > 5: continue
        
        hist_arr_mass.append(valm)
        hist_arr_tauz.append(valt)
        
#print(len(hist_arr))

for key in keys_non:
    obj_name = key.GetName()
    myTree = myfile_non.Get(obj_name+'/O2rtdimuonall;1')
    branch_list = myTree.GetListOfBranches()
    fMass = 'fMass'
    fTauz = 'fTauz'
    
    for e in myTree:
        fSign = getattr(e, 'fSign')
        fEta = getattr(e, 'fEta')
        fEta1 = getattr(e, 'fEta1')
        fEta2 = getattr(e, 'fEta2')
        fChi2MatchMCHMFT1 = getattr(e, 'fChi2MatchMCHMFT1')
        fChi2MatchMCHMFT2= getattr(e, 'fChi2MatchMCHMFT2')
        fChi2pca = getattr(e, 'fChi2pca')
        fPt = getattr(e, 'fPt')
        fTauzTemp = getattr(e, 'fTauz')
        fMcDecision = getattr(e, 'fMcDecision')

        if fMcDecision == 1: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        #if fChi2pca < 0: continue
        if fPt < 4 or fPt > 6: continue
        if abs(fTauzTemp) > 0.007: continue
        
        valm = getattr(e, fMass)
        valt = getattr(e, fTauz)

        if valm < 2 or valm > 5: continue

        hist_arr_non_mass.append(valm)
        hist_arr_non_tauz.append(valt)

print(len(hist_arr_mass))
print(len(hist_arr_non_mass))

print(len(hist_arr_tauz))
print(len(hist_arr_non_tauz))
hist_arr_combined_mass = hist_arr_mass + hist_arr_non_mass
hist_arr_combined_tauz = hist_arr_tauz + hist_arr_non_tauz


hm = ROOT.TH1F("hm","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hm.SetMarkerStyle(ROOT.kFullCross)
hm.SetMarkerColor(ROOT.kRed)
hm.SetMarkerSize(0.6)

hmnon = ROOT.TH1F("hmnon", str(fMass)+";m (GeV/c^2);#", 200, 2, 5)
hmnon.SetMarkerStyle(ROOT.kFullCross)
hmnon.SetMarkerColor(ROOT.kBlue)
hmnon.SetMarkerSize(0.6)

hm_comb = ROOT.TH1F("hmnon", str(fMass)+";m (GeV/c^2);#", 200, 2, 5)
hm_comb.SetMarkerStyle(ROOT.kFullCross)
hm_comb.SetMarkerColor(ROOT.kBlue)
hm_comb.SetMarkerSize(0.6)

ht = ROOT.TH1F("ht","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
ht.SetMarkerStyle(ROOT.kFullCross)
ht.SetMarkerColor(ROOT.kRed)
ht.SetMarkerSize(0.6)

htnon = ROOT.TH1F("htnon", str(fTauz)+";m (GeV/c^2);#", 100, -0.007, 0.007)
htnon.SetMarkerStyle(ROOT.kFullCross)
htnon.SetMarkerColor(ROOT.kBlue)
htnon.SetMarkerSize(0.6)

ht_comb = ROOT.TH1F("htnon", str(fTauz)+";m (GeV/c^2);#", 100, -0.007, 0.007)
ht_comb.SetMarkerStyle(ROOT.kFullCross)
ht_comb.SetMarkerColor(ROOT.kBlue)
ht_comb.SetMarkerSize(0.6)


for i in hist_arr_mass: hm.Fill(i)
for i in hist_arr_non_mass: hmnon.Fill(i)
for i in hist_arr_combined_mass: hm_comb.Fill(i)
    
for i in hist_arr_tauz: ht.Fill(i)
for i in hist_arr_non_tauz: htnon.Fill(i)
for i in hist_arr_combined_tauz: ht_comb.Fill(i)    

c = ROOT.TCanvas()
c.Divide(2, 1)

c.cd(1)
hmnon.Scale(1. / hmnon.Integral())
hmnon.Draw('P')
hm.Scale(1. / hm.Integral())
hm.Draw("P SAME")

c.cd(2)
htnon.Scale(1. / htnon.Integral())
htnon.Draw('P')
ht.Scale(1. / ht.Integral())
ht.Draw("P SAME")

c.Draw()
c.SaveAs("imgs/output_hists_tune_45_4-6.png")

