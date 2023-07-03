#if !defined(CLING) || defined(ROOTCLING)

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

#include "TSystemDirectory.h"
#include <TLorentzVector.h>
#include "TCanvas.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2D.h"
#include "TH1D.h"
#include "TF1.h"
#include "TMath.h"
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TKey.h"
#include "THashList.h"

#endif

std::vector<std::string> get_directories(const std::string& s) {
    std::vector<std::string> r;
    for(auto& p : std::filesystem::recursive_directory_iterator(s))
        if (p.is_directory())
            r.push_back(p.path().string());
    return r;
}

void read_tree(){

    const int fIn_number = 3;
    int fIn_counter = 0;
    int color_list[fIn_number] = {2, 4, 1};
    string fIn_names[fIn_number] = {"MC_non_prompt_jpsi.root", "MC_prompt_jpsi.root", "data.root"};

    float fMass = 0;
    float fPt = 0;
    float fPt1 = 0;
    float fPt2 = 0;
    float fEta = 0;
    float fEta1 = 0;
    float fEta2 = 0;
    int fSign = 0;
    float fChi21 = 0;
    float fChi22 = 0;
    float fChi2MatchMCHMID1 = 0;
    float fChi2MatchMCHMID2 = 0;
    float fChi2MatchMCHMFT1 = 0;
    float fChi2MatchMCHMFT2 = 0;
    float fTauz = 0;
    float fTauxy = 0;

    TH1F *hist_mass[fIn_number];
    TH1F *hist_tauz[fIn_number];
    TH1F *hist_pt[fIn_number];
    TH1F *hist_eta[fIn_number];

    for (auto& fIn_name : fIn_names) {
        hist_mass[fIn_counter] = new TH1F("hist_mass", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);
        
        hist_tauz[fIn_counter] = new TH1F("hist_tauz", "Dimuon tauz; #tau (ms); counts", 100, -0.1, 0.1);
        hist_tauz[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_pt[fIn_counter] = new TH1F("hist_pt", "Dimuon pt; pT (GeV/c); counts", 100, 0., 20);
        hist_pt[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_pt[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);
        
        hist_eta[fIn_counter] = new TH1F("hist_eta", "Dimuon eta; #eta; counts", 100, -5, -2);
        hist_eta[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_eta[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        TFile *fIn_tree = new TFile(Form("../data/%s", fIn_name.c_str()), "READ");
        TIter next(fIn_tree -> GetListOfKeys()); 
        TKey *key; 
        while ((key = (TKey*) next())) { 
            TString dirName = key -> GetName();
            if (!dirName.Contains("DF_")) {
                continue;
            }

            TTree *tree = (TTree*) fIn_tree -> Get(Form("%s/O2rtdimuonall", dirName.Data()));
            tree -> SetBranchAddress("fMass", &fMass);
            tree -> SetBranchAddress("fPt", &fPt);
            tree -> SetBranchAddress("fPt1", &fPt1);
            tree -> SetBranchAddress("fPt2", &fPt2);
            tree -> SetBranchAddress("fEta", &fEta);
            tree -> SetBranchAddress("fEta1", &fEta1);
            tree -> SetBranchAddress("fEta2", &fEta2);
            tree -> SetBranchAddress("fSign", &fSign);
            tree -> SetBranchAddress("fTauz", &fTauz);
            tree -> SetBranchAddress("fTauxy", &fTauxy);
            tree -> SetBranchAddress("fChi21", &fChi21);
            tree -> SetBranchAddress("fChi22", &fChi22);
            tree -> SetBranchAddress("fChi2MatchMCHMID1", &fChi2MatchMCHMID1);
            tree -> SetBranchAddress("fChi2MatchMCHMID2", &fChi2MatchMCHMID2);
            tree -> SetBranchAddress("fChi2MatchMCHMFT1", &fChi2MatchMCHMFT1);
            tree -> SetBranchAddress("fChi2MatchMCHMFT2", &fChi2MatchMCHMFT2);

            for (int iEntry = 0;iEntry < tree -> GetEntries();iEntry++) {
                tree -> GetEntry(iEntry);

                if (fSign != 0) continue;
                if (TMath::Abs(fEta) < 2.5 || TMath::Abs(fEta) > 4) continue;
                if (TMath::Abs(fEta1) < 2.5 || TMath::Abs(fEta1) > 4) continue;
                if (TMath::Abs(fEta2) < 2.5 || TMath::Abs(fEta2) > 4) continue;
                if (fChi2MatchMCHMID1 > 15 || fChi2MatchMCHMID2 > 15) continue;

                hist_mass[fIn_counter] -> Fill(fMass);
                hist_tauz[fIn_counter] -> Fill(fTauz);
                hist_pt[fIn_counter] -> Fill(fPt);
                hist_eta[fIn_counter] -> Fill(fEta);
            }
        }
        fIn_counter++;
    }

    TCanvas *canvas_var = new TCanvas("canvas_mass", "", 1800, 1200);
    canvas_var -> Divide(2, 2);

    canvas_var -> cd(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_mass[i] -> Scale(1. / hist_mass[i] -> Integral());
        hist_mass[i] -> Draw("EP SAME");
    }

    canvas_var -> cd(2);
    for (int i = 0;i < fIn_number;i++) {
        hist_tauz[i] -> Scale(1. / hist_tauz[i] -> Integral());
        hist_tauz[i] -> Draw("EP SAME");
    }

    canvas_var -> cd(3);
    for (int i = 0;i < fIn_number;i++) {
        hist_pt[i] -> Scale(1. / hist_pt[i] -> Integral());
        hist_pt[i] -> Draw("EP SAME");
    }

    canvas_var -> cd(4);
    for (int i = 0;i < fIn_number;i++) {
        hist_eta[i] -> Scale(1. / hist_eta[i] -> Integral());
        hist_eta[i] -> Draw("EP SAME");
    }
}