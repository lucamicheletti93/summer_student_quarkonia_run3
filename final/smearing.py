import os
import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf
from ROOT import gROOT, gBenchmark, gRandom, gSystem
import time
import concurrent.futures
import math
import numpy as np
import numpy
from scipy.stats import levy_stable

start_time = time.time()

fInPrompt = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/MC_prompt_jpsi_update.root')
fInNonPrompt = TFile('/home/lucas/Documents/CERN/alice_project/alice/root/MC_non_prompt_jpsi_update.root')
 
keysPrompt = fInPrompt.GetListOfKeys()
keysNonPrompt = fInNonPrompt.GetListOfKeys()

ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]

muon_mass = 0.105658

fPt1 = 0
fEta1 = 0
fPhi1 = 0
fPt2 = 0
fEta2 = 0
fPhi2 = 0


hMassPrompt =[]
hMassPromptSmeared = []
hMassNonPrompt = []
hMassNonPromptSmeared = []

hTauzPrompt = []
hTauzPromptSmeared = []
hTauzNonPrompt = []
hTauzNonPromptSmeared = []

hMass  = []
hTauz = []


for iPt in range(0, len(ptMin)):
    hMassPrompt.append(ROOT.TH1F("hMass_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassPromptSmeared.append(ROOT.TH1F("hMassPromptSmeared_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass Smeared;m (GeV/c^2);#", 200, 2, 5))
    hMassNonPrompt.append(ROOT.TH1F("hMassNonPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassNonPromptSmeared.append(ROOT.TH1F("hMassNonPromptSmeared_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass Smeared;m (GeV/c^2);#", 200, 2, 5))

    hTauzPrompt.append(ROOT.TH1F("hTauzPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzPromptSmeared.append(ROOT.TH1F("hTauzPromptSmeared_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass Smeared;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzNonPrompt.append(ROOT.TH1F("hTauzNonPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon Tauz ;m (GeV/c^2);#", 100,  -0.007, 0.007))
    hTauzNonPromptSmeared.append(ROOT.TH1F("hTauzNonPromptSmeared_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon Tauz Smeared;m (GeV/c^2);#", 100, -0.007, 0.007))


counter = 0

for key in keysPrompt:
    obj_name = key.GetName()
    if obj_name == 'parentFiles':
        continue

    myTree = fInPrompt.Get(obj_name+'/O2rtdimuonall;1')

    for e in myTree:
        fSign = getattr(e, 'fSign')
        fEta = getattr(e, 'fEta')
        fEta1 = getattr(e, 'fEta1')
        fEta2 = getattr(e, 'fEta2')
        fPt1 = getattr(e, 'fPt1')
        fPt2 = getattr(e, 'fPt2')
        fPhi1 = getattr(e, 'fPhi1')
        fPhi2 = getattr(e, 'fPhi2')
        fChi2MatchMCHMFT1= getattr(e, 'fChi2MatchMCHMFT1')
        fChi2MatchMCHMFT2= getattr(e, 'fChi2MatchMCHMFT2')
        fChi2pca = getattr(e, 'fChi2pca')
        fPt = getattr(e, 'fPt')
        fTauzTemp = getattr(e, 'fTauz')
        fMcDecision = getattr(e, 'fMcDecision')

        fMass = getattr(e, 'fMass')
        fTauz = getattr(e, 'fTauz')

        if fMcDecision == 0: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        #if fChi2pca < 0: continue
        if abs(fTauzTemp) > 0.007: continue
        if fMass < 2 or fMass > 5: continue
        

        for iPt in range(0, len(ptMin)):
            if fPt > ptMin[iPt] and fPt < ptMax[iPt]:
                hMassPrompt[iPt].Fill(fMass)
                hTauzPrompt[iPt].Fill(fTauz)


                tauz_smear = fTauz + np.random.normal(0, 0.00025)
                hTauzPromptSmeared[iPt].Fill(tauz_smear)


                mu1 = ROOT.TLorentzVector()
                mu1.SetPtEtaPhiM(fPt1, fEta1, fPhi1, muon_mass)
                mu1_Px = mu1.Px() * gRandom.Uniform(0.92, 1.08)
                mu1_Py = mu1.Py() * gRandom.Uniform(0.92, 1.08)
                mu1_Pz = mu1.Pz() * gRandom.Uniform(0.92, 1.08)
                mu1_P = ROOT.TMath.Sqrt(mu1_Px * mu1_Px + mu1_Py * mu1_Py + mu1_Pz * mu1_Pz)
                mu1_E = ROOT.TMath.Sqrt(muon_mass * muon_mass + mu1_P * mu1_P)
                mu1_smeared = ROOT.TLorentzVector()
                mu1_smeared.SetPxPyPzE(mu1_Px, mu1_Py, mu1_Pz, mu1_E)

                mu2 = ROOT.TLorentzVector()
                mu2.SetPtEtaPhiM(fPt2, fEta2, fPhi2, muon_mass)
                mu2_Px = mu2.Px() * gRandom.Uniform(0.92, 1.08)
                mu2_Py = mu2.Py() * gRandom.Uniform(0.92, 1.08)
                mu2_Pz = mu2.Pz() * gRandom.Uniform(0.92, 1.08)
                mu2_P = ROOT.TMath.Sqrt(mu2_Px * mu2_Px + mu2_Py * mu2_Py + mu2_Pz * mu2_Pz)
                mu2_E = ROOT.TMath.Sqrt(muon_mass * muon_mass + mu2_P * mu2_P)
                mu2_smeared = ROOT.TLorentzVector()
                mu2_smeared.SetPxPyPzE(mu2_Px, mu2_Py, mu2_Pz, mu2_E)



                dimuon_smeared = mu1_smeared + mu2_smeared
                hMassPromptSmeared[iPt].Fill(dimuon_smeared.M())

                counter +=1


counter = 0

for key in keysNonPrompt:
    obj_name = key.GetName()
    if obj_name == 'parentFiles':
        continue

    myTree = fInNonPrompt.Get(obj_name+'/O2rtdimuonall;1')

    for e in myTree:
        fSign = getattr(e, 'fSign')
        fEta = getattr(e, 'fEta')
        fEta1 = getattr(e, 'fEta1')
        fEta2 = getattr(e, 'fEta2')
        fPt1 = getattr(e, 'fPt1')
        fPt2 = getattr(e, 'fPt2')
        fPhi1 = getattr(e, 'fPhi1')
        fPhi2 = getattr(e, 'fPhi2')
        fChi2MatchMCHMFT1= getattr(e, 'fChi2MatchMCHMFT1')
        fChi2MatchMCHMFT2= getattr(e, 'fChi2MatchMCHMFT2')
        fChi2pca = getattr(e, 'fChi2pca')
        fPt = getattr(e, 'fPt')
        fTauzTemp = getattr(e, 'fTauz')
        fMcDecision = getattr(e, 'fMcDecision')

        fMass = getattr(e, 'fMass')
        fTauz = getattr(e, 'fTauz')

        if fMcDecision == 0: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        #if fChi2pca < 0: continue
        if abs(fTauzTemp) > 0.007: continue
        if fMass < 2 or fMass > 5: continue
        

        for iPt in range(0, len(ptMin)):
            if fPt > ptMin[iPt] and fPt < ptMax[iPt]:
                hMassNonPrompt[iPt].Fill(fMass)
                hTauzNonPrompt[iPt].Fill(fTauz)
                

                #   NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE 
                #     1  Constant     1.24328e+03   3.14657e+01   9.42465e-02   2.51758e-06
                #     2  MPV          6.64938e-04   1.79402e-05   6.10221e-08   3.31423e+00
                #     3  Sigma        4.92372e-04   1.15309e-05   1.19827e-05  -3.64546e-02
                
                tauz_smear = fTauz + levy_stable.rvs(alpha=1.0, beta=1.14938e-04, loc=1.14938e-04, scale=1.52372e-04)
                hTauzNonPromptSmeared[iPt].Fill(tauz_smear)

                mu1 = ROOT.TLorentzVector()
                mu1.SetPtEtaPhiM(fPt1, fEta1, fPhi1, muon_mass)
                mu1_Px = mu1.Px() * gRandom.Uniform(0.96, 1.04)
                mu1_Py = mu1.Py() * gRandom.Uniform(0.96, 1.04)
                mu1_Pz = mu1.Pz() * gRandom.Uniform(0.96, 1.04)
                mu1_P = ROOT.TMath.Sqrt(mu1_Px * mu1_Px + mu1_Py * mu1_Py + mu1_Pz * mu1_Pz)
                mu1_E = ROOT.TMath.Sqrt(muon_mass * muon_mass + mu1_P * mu1_P)
                mu1_smeared = ROOT.TLorentzVector()
                mu1_smeared.SetPxPyPzE(mu1_Px, mu1_Py, mu1_Pz, mu1_E)

                mu2 = ROOT.TLorentzVector()
                mu2.SetPtEtaPhiM(fPt2, fEta2, fPhi2, muon_mass)
                mu2_Px = mu2.Px() * gRandom.Uniform(0.96, 1.04)
                mu2_Py = mu2.Py() * gRandom.Uniform(0.96, 1.04)
                mu2_Pz = mu2.Pz() * gRandom.Uniform(0.96, 1.04)
                mu2_P = ROOT.TMath.Sqrt(mu2_Px * mu2_Px + mu2_Py * mu2_Py + mu2_Pz * mu2_Pz)
                mu2_E = ROOT.TMath.Sqrt(muon_mass * muon_mass + mu2_P * mu2_P)
                mu2_smeared = ROOT.TLorentzVector()
                mu2_smeared.SetPxPyPzE(mu2_Px, mu2_Py, mu2_Pz, mu2_E)



                dimuon_smeared = mu1_smeared + mu2_smeared
                hMassNonPromptSmeared[iPt].Fill(dimuon_smeared.M())

                counter +=1
os.remove("mcSmear.root")
for iPt in range(0, len(ptMin)):
    
    fl = ROOT.TFile("mcSmear.root", "UPDATE")
    hMassPrompt[iPt].Write()
    hMassPromptSmeared[iPt].Write()
    
    hMassNonPrompt[iPt].Write()
    hMassNonPromptSmeared[iPt].Write()
    
    hTauzPrompt[iPt].Write()
    hTauzPromptSmeared[iPt].Write()

    hTauzNonPrompt[iPt].Write()
    hTauzNonPromptSmeared[iPt].Write()

    fl.Close()


end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")