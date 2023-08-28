import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf

fInPrompt = TFile('/Users/lucamicheletti/cernbox/summer_student_quarkonia_run3/data/MC_prompt_jpsi_update.root')
fInNonPrompt = TFile('/Users/lucamicheletti/cernbox/summer_student_quarkonia_run3/data/MC_non_prompt_jpsi_update.root')
treeList = []

# Get the list of keys in the file

keysPrompt = fInPrompt.GetListOfKeys()
keysPrompt.pop()

keysNonPrompt = fInNonPrompt.GetListOfKeys()
keysNonPrompt.pop()

ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]

hMassPrompt = []
hMassNonPrompt = []
hTauzPrompt = []
hTauzNonPrompt = []

hMassPromptInt = ROOT.TH1F("hMassPromptInt","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hTauzPromptInt = ROOT.TH1F("hTauzPromptInt","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hPtPromptInt = ROOT.TH1F("hPtPromptInt","Dimuon transverse momentum ;pT (GeV/c);#", 100, 0, 20)
hEtaPromptInt = ROOT.TH1F("hEtaPromptInt","Dimuon transverse momentum ;eta;#", 100, -5, 5)
hMassNonPromptInt = ROOT.TH1F("hMassNonPromptInt","Dimuon mass ;m (GeV/c^2);#", 200, 2, 5)
hTauzNonPromptInt = ROOT.TH1F("hTauzNonPromptInt","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hPtNonPromptInt = ROOT.TH1F("hPtNonPromptInt","Dimuon transverse momentum ;pT (GeV/c);#", 100, 0, 20)
hEtaNonPromptInt = ROOT.TH1F("hEtaNonPromptInt","Dimuon transverse momentum ;eta;#", 100, -5, 5)
for iPt in range(0, len(ptMin)):
    hMassPrompt.append(ROOT.TH1F("hMassPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hMassNonPrompt.append(ROOT.TH1F("hMassNonPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
    hTauzPrompt.append(ROOT.TH1F("hTauzPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007))
    hTauzNonPrompt.append(ROOT.TH1F("hTauzNonPrompt_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007))

# Iterate over the keys and print the object names

for key in keysPrompt:
    obj_name = key.GetName()
    myTree = fInPrompt.Get(obj_name+'/O2rtdimuonall;1')
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

        if fMcDecision == 0: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        if abs(fTauzTemp) > 0.007: continue
            
        valm = getattr(e, fMass)
        valt = getattr(e, fTauz)

        if valm < 2 or valm > 5: continue

        hMassPromptInt.Fill(valm)
        hTauzPromptInt.Fill(valt)
        hPtPromptInt.Fill(fPt)
        hEtaPromptInt.Fill(fEta)

        for iPt in range(0, len(ptMin)):
            if fPt > ptMin[iPt] and fPt < ptMax[iPt]:
                hMassPrompt[iPt].Fill(valm)
                hTauzPrompt[iPt].Fill(valt)

for key in keysNonPrompt:
    obj_name = key.GetName()
    myTree = fInNonPrompt.Get(obj_name+'/O2rtdimuonall;1')
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

        if fMcDecision == 0: continue
        if fSign != 0: continue
        if (abs(fEta) < 2.5 or abs(fEta) > 4.0): continue
        if (abs(fEta1) < 2.5 or abs(fEta1) > 4.0): continue
        if (abs(fEta2) < 2.5 or abs(fEta2) > 4.0): continue 
        if (fChi2MatchMCHMFT1 > 45 or fChi2MatchMCHMFT2 > 45): continue
        if abs(fTauzTemp) > 0.007: continue
        
        valm = getattr(e, fMass)
        valt = getattr(e, fTauz)

        if valm < 2 or valm > 5: continue

        hMassNonPromptInt.Fill(valm)
        hTauzNonPromptInt.Fill(valt)
        hPtNonPromptInt.Fill(fPt)
        hEtaNonPromptInt.Fill(fEta)

        for iPt in range(0, len(ptMin)):
            if fPt > ptMin[iPt] and fPt < ptMax[iPt]:
                hMassNonPrompt[iPt].Fill(valm)
                hTauzNonPrompt[iPt].Fill(valt)


fOut = ROOT.TFile("template.root", "RECREATE")
hMassPromptInt.Write()
hTauzPromptInt.Write()
hPtPromptInt.Write()
hEtaPromptInt.Write()
hMassNonPromptInt.Write()
hTauzNonPromptInt.Write()
hPtNonPromptInt.Write()
hEtaNonPromptInt.Write()
for iPt in range(0, len(ptMin)):
    hMassPrompt[iPt].Write()
    hTauzPrompt[iPt].Write()
    hMassNonPrompt[iPt].Write()
    hTauzNonPrompt[iPt].Write()
fOut.Close()