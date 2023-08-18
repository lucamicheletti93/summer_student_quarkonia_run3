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
#include "TRandom3.h"
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

void reduced_tree() {
    //string fIn_name = "/Users/lucamicheletti/cernbox/summer_student_quarkonia_run3/data/LHC22r/AO2D.root";
    string fIn_name = "/Users/lucamicheletti/cernbox/QM2023_DQ_performance/LHC22o/528379/001/AO2D.root";

    TFile *fIn_tree = new TFile(Form("%s", fIn_name.c_str()), "READ");
    TIter next(fIn_tree -> GetListOfKeys()); 
    TKey *key; 
    TFile* fOut = new TFile("outfile.root", "RECREATE");
    while ((key = (TKey*) next())) { 
        TString dirName = key -> GetName();
        if (!dirName.Contains("DF_")) {
            continue;
        }
        std::cout << dirName.Data() << std::endl;

        TTree *tree = (TTree*) fIn_tree -> Get(Form("%s/O2rtdimuonall", dirName.Data()));
        fOut -> cd();
        TDirectoryFile *dir = new TDirectoryFile(dirName.Data(), dirName.Data());
        dir -> cd();
        TTree *tree_selected = tree -> CopyTree("fMass>2. && fMass<5.");
        tree_selected -> Write("O2rtdimuonall");
    }
    fOut -> Close();
    fIn_tree -> Close();
}

void read_tree(){

    const double muon_mass = 0.105658;
    int fIn_counter = 0;
    /*const int fIn_number = 3;
    int color_list[fIn_number] = {2, 4, 1};
    //string fIn_names[fIn_number] = {"MC_non_prompt_jpsi.root", "MC_prompt_jpsi.root", "data.root"};
    string fIn_names[fIn_number] = {"AO2D_LHC21i3d2.root", "AO2D_LHC21i3g2.root", "data.root"};
    string hist_names[fIn_number] = {"prompt_Jpsi", "non_prompt_jpsi", "data"};*/

    const int fIn_number = 3;
    int color_list[fIn_number] = {
        2, 
        4, 
        1
    };
    string fIn_names[fIn_number] = {
        "../data/AO2D_LHC21i3d2_CPA.root", 
        "../data/AO2D_LHC21i3g2_CPA.root",
        "/Users/lucamicheletti/cernbox/summer_student_quarkonia_run3/data/LHC22o/AO2D.root"
    };
    string hist_names[fIn_number] = {
        "prompt_Jpsi", 
        "non_prompt_jpsi",
        "data"
    };

    float fMass = 0;
    float fPt = 0;
    float fPt1 = 0;
    float fPt2 = 0;
    float fEta = 0;
    float fEta1 = 0;
    float fEta2 = 0;
    float fPhi = 0;
    float fPhi1 = 0;
    float fPhi2 = 0;
    int fSign = 0;
    float fChi21 = 0;
    float fChi22 = 0;
    float fChi2MatchMCHMID1 = 0;
    float fChi2MatchMCHMID2 = 0;
    float fChi2MatchMCHMFT1 = 0;
    float fChi2MatchMCHMFT2 = 0;
    float fTauz = 0;
    float fTauxy = 0;
    float fCosPointingAngle = 0;
    float fFwdDcaX1 = 0;
    float fFwdDcaX2 = 0;
    float fFwdDcaY1 = 0;
    float fFwdDcaY2 = 0;
    uint32_t fMcDecision = -999;

    TH1F *hist_mass_ospm[fIn_number];
    TH1F *hist_mass_lspp[fIn_number];
    TH1F *hist_mass_lsmm[fIn_number];
    TH1F *hist_mass_ospm_smeared[fIn_number];
    TH1F *hist_tauz_ospm[fIn_number];
    TH1F *hist_tauz_lspp[fIn_number];
    TH1F *hist_tauz_lsmm[fIn_number];
    TH1F *hist_pt[fIn_number];
    TH1F *hist_eta[fIn_number];
    TH1F *hist_fwdDcaX1[fIn_number];
    TH1F *hist_fwdDcaX2[fIn_number];
    TH1F *hist_fwdDcaY1[fIn_number];
    TH1F *hist_fwdDcaY2[fIn_number];
    TH1F *hist_cosPointingAngle[fIn_number];
    TH1F *hist_mass_sig[fIn_number];
    TH1F *hist_mass_bkg[fIn_number];
    TH1F *hist_tauz_sig[fIn_number];
    TH1F *hist_tauz_bkg[fIn_number];

    for (auto& fIn_name : fIn_names) {
        hist_mass_ospm[fIn_counter] = new TH1F("hist_mass_ospm", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_ospm[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_ospm[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_mass_lspp[fIn_counter] = new TH1F("hist_mass_lspp", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_lspp[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_lspp[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_mass_lsmm[fIn_counter] = new TH1F("hist_mass_lsmm", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_lsmm[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_lsmm[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_mass_ospm_smeared[fIn_counter] = new TH1F("hist_mass_ospm_smeared", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_ospm_smeared[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_ospm_smeared[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);
        
        hist_tauz_ospm[fIn_counter] = new TH1F("hist_tauz_ospm", "Dimuon tauz; #tau (ms); counts", 400, -0.02, 0.02);
        hist_tauz_ospm[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz_ospm[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_tauz_lspp[fIn_counter] = new TH1F("hist_tauz_lspp", "Dimuon tauz; #tau (ms); counts", 400, -0.02, 0.02);
        hist_tauz_lspp[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz_lspp[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_tauz_lsmm[fIn_counter] = new TH1F("hist_tauz_lsmm", "Dimuon tauz; #tau (ms); counts", 400, -0.02, 0.02);
        hist_tauz_lsmm[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz_lsmm[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_pt[fIn_counter] = new TH1F("hist_pt", "Dimuon pt; pT (GeV/c); counts", 100, 0., 20);
        hist_pt[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_pt[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);
        
        hist_eta[fIn_counter] = new TH1F("hist_eta", "Dimuon eta; #eta; counts", 100, -5, -2);
        hist_eta[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_eta[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_fwdDcaX1[fIn_counter] = new TH1F("hist_fwdDcaX1", "Dimuon fwdDcaX1; #DCA X #mu^{1}; counts", 1000, -10, 10);
        hist_fwdDcaX1[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_fwdDcaX1[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_fwdDcaX2[fIn_counter] = new TH1F("hist_fwdDcaX2", "Dimuon fwdDcaX2; #DCA X #mu^{2}; counts", 1000, -10, 10);
        hist_fwdDcaX2[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_fwdDcaX2[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_fwdDcaY1[fIn_counter] = new TH1F("hist_fwdDcaY1", "Dimuon fwdDcaY1; #DCA Y #mu^{1}; counts", 1000, -10, 10);
        hist_fwdDcaY1[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_fwdDcaY1[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_fwdDcaY2[fIn_counter] = new TH1F("hist_fwdDcaY2", "Dimuon fwdDcaY2; #DCA Y #mu^{2}; counts", 1000, -10, 10);
        hist_fwdDcaY2[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_fwdDcaY2[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_cosPointingAngle[fIn_counter] = new TH1F("hist_cosPointingAngle", "Dimuon CPA; CPA; counts", 100, -1, 1);
        hist_cosPointingAngle[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_cosPointingAngle[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_mass_sig[fIn_counter] = new TH1F("hist_mass_sig", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_sig[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_sig[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_mass_bkg[fIn_counter] = new TH1F("hist_mass_bkg", "Dimuon mass; m (GeV/c^{2}); counts", 100, 2., 5.);
        hist_mass_bkg[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_mass_bkg[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_tauz_sig[fIn_counter] = new TH1F("hist_tauz_sig", "Dimuon tauz; #tau (ms); counts", 400, -0.02, 0.02);
        hist_tauz_sig[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz_sig[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        hist_tauz_bkg[fIn_counter] = new TH1F("hist_tauz_bkg", "Dimuon tauz; #tau (ms); counts", 400, -0.02, 0.02);
        hist_tauz_bkg[fIn_counter] -> SetLineColor(color_list[fIn_counter]);
        hist_tauz_bkg[fIn_counter] -> SetMarkerColor(color_list[fIn_counter]);

        TFile *fIn_tree = new TFile(Form("%s", fIn_name.c_str()), "READ");
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
            tree -> SetBranchAddress("fPhi", &fPhi);
            tree -> SetBranchAddress("fPhi1", &fPhi1);
            tree -> SetBranchAddress("fPhi2", &fPhi2);
            tree -> SetBranchAddress("fSign", &fSign);
            tree -> SetBranchAddress("fTauz", &fTauz);
            tree -> SetBranchAddress("fFwdDcaX1", &fFwdDcaX1);
            tree -> SetBranchAddress("fFwdDcaX2", &fFwdDcaX2);
            tree -> SetBranchAddress("fFwdDcaY1", &fFwdDcaY1);
            tree -> SetBranchAddress("fFwdDcaY2", &fFwdDcaY2);
            tree -> SetBranchAddress("fCosPointingAngle", &fCosPointingAngle);
            tree -> SetBranchAddress("fTauxy", &fTauxy);
            tree -> SetBranchAddress("fChi21", &fChi21);
            tree -> SetBranchAddress("fChi22", &fChi22);
            tree -> SetBranchAddress("fChi2MatchMCHMID1", &fChi2MatchMCHMID1);
            tree -> SetBranchAddress("fChi2MatchMCHMID2", &fChi2MatchMCHMID2);
            tree -> SetBranchAddress("fChi2MatchMCHMFT1", &fChi2MatchMCHMFT1);
            tree -> SetBranchAddress("fChi2MatchMCHMFT2", &fChi2MatchMCHMFT2);
            tree -> SetBranchAddress("fMcDecision", &fMcDecision);

            for (int iEntry = 0;iEntry < tree -> GetEntries();iEntry++) {
                tree -> GetEntry(iEntry);

                if (fMass < 2 || fMass > 5) continue;
                if(fMcDecision == 0) continue; // selecting signal only
                if (TMath::Abs(fEta) < 2.5 || TMath::Abs(fEta) > 4) continue;
                if (TMath::Abs(fEta1) < 2.5 || TMath::Abs(fEta1) > 4) continue;
                if (TMath::Abs(fEta2) < 2.5 || TMath::Abs(fEta2) > 4) continue;
                if (fChi2MatchMCHMFT1 > 45 || fChi2MatchMCHMFT2 > 45) continue;

                if (fSign > 0) {
                    hist_mass_lspp[fIn_counter] -> Fill(fMass);
                    hist_tauz_lspp[fIn_counter] -> Fill(fTauz);
                }
                if (fSign < 0) {
                    hist_mass_lsmm[fIn_counter] -> Fill(fMass);
                    hist_tauz_lsmm[fIn_counter] -> Fill(fTauz);
                }


                if (fSign != 0) continue;
                hist_mass_ospm[fIn_counter] -> Fill(fMass);
                hist_tauz_ospm[fIn_counter] -> Fill(fTauz);
                hist_cosPointingAngle[fIn_counter] -> Fill(fCosPointingAngle);
                hist_pt[fIn_counter] -> Fill(fPt);
                hist_eta[fIn_counter] -> Fill(fEta);

                hist_fwdDcaX1[fIn_counter] -> Fill(fFwdDcaX1);
                hist_fwdDcaX2[fIn_counter] -> Fill(fFwdDcaX2);
                hist_fwdDcaY1[fIn_counter] -> Fill(fFwdDcaY1);
                hist_fwdDcaY2[fIn_counter] -> Fill(fFwdDcaY2);

                TLorentzVector mu1;
                mu1.SetPtEtaPhiM(fPt1, fEta1, fPhi1, muon_mass);
                double mu1_Px = mu1.Px() * gRandom->Uniform(0.96, 1.04);
                double mu1_Py = mu1.Py() * gRandom->Uniform(0.96, 1.04);
                double mu1_Pz = mu1.Pz() * gRandom->Uniform(0.96, 1.04);
                double mu1_P = TMath::Sqrt(mu1_Px * mu1_Px + mu1_Py * mu1_Py + mu1_Pz * mu1_Pz);
                double mu1_E = TMath::Sqrt(muon_mass * muon_mass + mu1_P * mu1_P);
                TLorentzVector mu1_smeared;
                mu1_smeared.SetPxPyPzE(mu1_Px, mu1_Py, mu1_Pz, mu1_E);

                TLorentzVector mu2;
                mu2.SetPtEtaPhiM(fPt2, fEta2, fPhi2, muon_mass);
                double mu2_Px = mu2.Px() * gRandom->Uniform(0.96, 1.04);
                double mu2_Py = mu2.Py() * gRandom->Uniform(0.96, 1.04);
                double mu2_Pz = mu2.Pz() * gRandom->Uniform(0.96, 1.04);
                double mu2_P = TMath::Sqrt(mu2_Px * mu2_Px + mu2_Py * mu2_Py + mu2_Pz * mu2_Pz);
                double mu2_E = TMath::Sqrt(muon_mass * muon_mass + mu2_P * mu2_P);
                TLorentzVector mu2_smeared;
                mu2_smeared.SetPxPyPzE(mu2_Px, mu2_Py, mu2_Pz, mu2_E);

                TLorentzVector dimuon_smeared = mu1_smeared + mu2_smeared;
                hist_mass_ospm_smeared[fIn_counter] -> Fill(dimuon_smeared.M());
            }
        }
        fIn_tree -> Close();
        fIn_counter++;
    }

    for (int i = 0;i < fIn_number;i++) {
        for (int iBin = 0;iBin < hist_mass_ospm[i] -> GetNbinsX();iBin++) {
            double OS = hist_mass_ospm[i] -> GetBinContent(iBin+1);
            double SDOS = hist_mass_ospm[i] -> GetBinError(iBin+1);
            double PP = hist_mass_lspp[i] -> GetBinContent(iBin+1);
            double SDPP = hist_mass_lspp[i]-> GetBinError(iBin+1);
            double MM = hist_mass_lsmm[i] -> GetBinContent(iBin+1);
            double SDMM = hist_mass_lsmm[i] -> GetBinError(iBin+1);
            double GM = 2 * TMath::Sqrt(PP * MM);
            //double SDGM = TMath::Sqrt(((GM - MM) * (GM - MM) + (GM - PP) * (GM - PP)) / 2.);
            double SDGM = GM * ((SDPP / PP) + (SDMM / MM));
            hist_mass_bkg[i] -> SetBinContent(iBin+1,GM);
            hist_mass_bkg[i] -> SetBinError(iBin+1, SDGM);
            hist_mass_sig[i] -> SetBinContent(iBin+1, OS - GM);
            hist_mass_sig[i] -> SetBinError(iBin+1, TMath::Sqrt(OS - GM));
        }

        for (int iBin = 0;iBin < hist_tauz_ospm[i] -> GetNbinsX();iBin++) {
            double OS = hist_tauz_ospm[i] -> GetBinContent(iBin+1);
            double SDOS = hist_tauz_ospm[i] -> GetBinError(iBin+1);
            double PP = hist_tauz_lspp[i] -> GetBinContent(iBin+1);
            double SDPP = hist_tauz_lspp[i]-> GetBinError(iBin+1);
            double MM = hist_tauz_lsmm[i] -> GetBinContent(iBin+1);
            double SDMM = hist_tauz_lsmm[i] -> GetBinError(iBin+1);
            double GM = 2 * TMath::Sqrt(PP * MM);
            //double SDGM = TMath::Sqrt(((GM - MM) * (GM - MM) + (GM - PP) * (GM - PP)) / 2.);
            double SDGM = GM * ((SDPP / PP) + (SDMM / MM));
            hist_tauz_bkg[i] -> SetBinContent(iBin+1,GM);
            hist_tauz_bkg[i] -> SetBinError(iBin+1, SDGM);
            hist_tauz_sig[i] -> SetBinContent(iBin+1, OS - GM);
            hist_tauz_sig[i] -> SetBinError(iBin+1, TMath::Sqrt(OS - GM));
        }
    }

    TCanvas *canvas_var = new TCanvas("canvas_mass", "", 1800, 1200);
    canvas_var -> Divide(3, 2);

    canvas_var -> cd(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_mass_ospm[i] -> Scale(1. / hist_mass_ospm[i] -> Integral());
        hist_mass_ospm[i] -> Draw("EP SAME");
        //hist_mass_ospm_smeared[i] -> Scale(1. / hist_mass_ospm_smeared[i] -> Integral());
        //hist_mass_ospm_smeared[i] -> Draw("H SAME");
    }

    canvas_var -> cd(2);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_tauz_ospm[i] -> Scale(1. / hist_tauz_ospm[i] -> Integral());
        hist_tauz_ospm[i] -> Draw("EP SAME");
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

    canvas_var -> cd(5);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_cosPointingAngle[i] -> Scale(1. / hist_cosPointingAngle[i] -> Integral());
        hist_cosPointingAngle[i] -> Draw("EP SAME");
    }

    TCanvas *canvas_dca = new TCanvas("canvas_dca", "", 1800, 1200);
    canvas_dca -> Divide(2, 2);

    canvas_dca -> cd(1);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_fwdDcaX1[i] -> Scale(1. / hist_fwdDcaX1[i] -> Integral());
        hist_fwdDcaX1[i] -> Draw("EP SAME");
    }

    canvas_dca -> cd(2);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_fwdDcaX2[i] -> Scale(1. / hist_fwdDcaX2[i] -> Integral());
        hist_fwdDcaX2[i] -> Draw("EP SAME");
    }

    canvas_dca -> cd(3);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_fwdDcaY1[i] -> Scale(1. / hist_fwdDcaY1[i] -> Integral());
        hist_fwdDcaY1[i] -> Draw("EP SAME");
    }

    canvas_dca -> cd(4);
    gPad -> SetLogy(1);
    for (int i = 0;i < fIn_number;i++) {
        hist_fwdDcaY2[i] -> Scale(1. / hist_fwdDcaY2[i] -> Integral());
        hist_fwdDcaY2[i] -> Draw("EP SAME");
    }

    TFile *fOut = new TFile("MC_signal.root", "RECREATE");
    for (int i = 0;i < fIn_number;i++) {
        hist_mass_ospm[i] -> Write(Form("%s_mass_ospm", hist_names[i].c_str()));
        hist_mass_lspp[i] -> Write(Form("%s_mass_lspp", hist_names[i].c_str()));
        hist_mass_lsmm[i] -> Write(Form("%s_mass_lsmm", hist_names[i].c_str()));
        hist_tauz_ospm[i] -> Write(Form("%s_tauz_ospm", hist_names[i].c_str()));
        hist_tauz_lspp[i] -> Write(Form("%s_tauz_lspp", hist_names[i].c_str()));
        hist_tauz_lsmm[i] -> Write(Form("%s_tauz_lsmm", hist_names[i].c_str()));
        hist_mass_ospm_smeared[i] -> Write(Form("%s_mass_ospm_smeared", hist_names[i].c_str()));
        hist_mass_sig[i] -> Write(Form("%s_mass_sig", hist_names[i].c_str()));
        hist_mass_bkg[i] -> Write(Form("%s_mass_bkg", hist_names[i].c_str()));
        hist_tauz_sig[i] -> Write(Form("%s_tauz_sig", hist_names[i].c_str()));
        hist_tauz_bkg[i] -> Write(Form("%s_tauz_bkg", hist_names[i].c_str()));
    }
    fOut -> Close();
}