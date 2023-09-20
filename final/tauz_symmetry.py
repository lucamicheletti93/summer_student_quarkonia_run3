import ROOT
from ROOT import *
import os

PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
os.remove(f"{PATH_DATA}tauzPromptMirror.root")
hTauz = []
hTauzSig = []


ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]

color_set = [ ROOT.kRed+1,  ROOT.kBlue+1 , ROOT.kGreen+1 , ROOT.kMagenta+1]



tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

hTauzDataNonPromptDistrSum = ROOT.TH1F(f"hTauzDataNonPromptDistrSum","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)

def LoadStyle():
    ROOT.gStyle.SetPadLeftMargin(0.15)
    ROOT.gStyle.SetPadBottomMargin(0.15)
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetEndErrorSize(0.0)
    ROOT.gStyle.SetTitleSize(0.05,"X")
    ROOT.gStyle.SetTitleSize(0.045,"Y")
    ROOT.gStyle.SetLabelSize(0.045,"X")
    ROOT.gStyle.SetLabelSize(0.045,"Y")
    ROOT.gStyle.SetTitleOffset(1.2,"X")
    ROOT.gStyle.SetTitleOffset(1.35,"Y")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetHatchesSpacing(0.3)

for iPt in range(0, len(ptMin)):
    
    hTauzDataPromptDistr = ROOT.TH1F(f"hTauzDataPromptDistr_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    hTauzDataNonPromptDistr = ROOT.TH1F(f"hTauzDataNonPromptDistr_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    
    dataFile = ROOT.TFile(PATH_DATA + "data.root")
    templateFile = ROOT.TFile(PATH_DATA + "template.root")
    
    hTauzPromptTemplate = templateFile.Get(f"hTauzPrompt_{ptMin[iPt]}_{ptMax[iPt]}") 
    hTauzNonPromptTemplate = templateFile.Get(f"hTauzNonPrompt_{ptMin[iPt]}_{ptMax[iPt]}") 
    
    hTauzData = dataFile.Get(f"hTauz_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzSigDistr = dataFile.Get(f"hTauzSig_{ptMin[iPt]}_{ptMax[iPt]}")
    
    bin_start = -0.007
    bin_end = 0.007
    
    
    for iBin in range(1, hTauzSigDistr.GetNbinsX() + 1):
        if iBin <= 50:
            binValPrompt1 = hTauzSigDistr.GetBinContent(iBin) 
            hTauzDataPromptDistr.SetBinContent(iBin, binValPrompt1)
        if iBin > 50:
            binValPrompt2 = hTauzDataPromptDistr.GetBinContent(101 - iBin) 
            hTauzDataPromptDistr.SetBinContent(iBin, binValPrompt2)
        
        binValNonPrompt = hTauzSigDistr.GetBinContent(iBin) - hTauzDataPromptDistr.GetBinContent(iBin)
        hTauzDataNonPromptDistr.SetBinContent(iBin, binValNonPrompt)
    
    hTauzDataNonPromptDistrSum.Add(hTauzDataNonPromptDistr)
        
    hTauzDataHist = ROOT.RooDataHist("hTauzDataHist", "hTauzDataHist", ROOT.RooArgList(tauz), hTauzData)
    hTauzSigHist = ROOT.RooDataHist("hTauzSigHist", "hTauzSigHist", ROOT.RooArgList(tauz), hTauzSigDistr)
    hTauzDataPromptHist = ROOT.RooDataHist("hTauzDataPromptHist", "hTauzDataPromptHist", ROOT.RooArgList(tauz), hTauzDataPromptDistr)
    hTauzDataNonPromptHist = ROOT.RooDataHist("hTauzDataNonPromptHist", "hTauzDataNonPromptHist", ROOT.RooArgList(tauz), hTauzDataNonPromptDistr)

    
    #-----------------------------FITTING-----------------------------------------
    # mean_bw_tauz_data_prompt = ROOT.RooRealVar("mean_bw_tauz_data_prompt", "Mean bw", 0, -1, 1)
    # width_bw_tauz_data_prompt = ROOT.RooRealVar("width_bw_tauz_data_prompt", "Width bw", 0.9e-03, 0.1e-03, 1e-02)
    # lead_pdf_tauz_data_prompt = ROOT.RooBreitWigner("bw_tauz_data_prompt", "Breit-Wigner Distribution", tauz, mean_bw_tauz_data_prompt, width_bw_tauz_data_prompt)

    # lead_pdf_tauz_data_prompt.fitTo(hTauzDataPromptHist)
    

    
    # cheb_coeffs_data_prompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -10, 10) for i in range(2)]
    # cheb_poly_data_prompt = ROOT.RooChebychev("cheb_poly_data_prompt", "Chebyshev Polynomial", tauz, ROOT.RooArgList(*cheb_coeffs_data_prompt))
    
    # cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
    # combined_pdf = ROOT.RooAddPdf("combined_pdf ", "Cheby + Main PDF", ROOT.RooArgList(cheb_poly_data_prompt, lead_pdf_tauz_data_prompt), ROOT.RooArgList(cb_frac))
    
    #-----------------------------------PLOTTING----------------------------------
    
    LoadStyle()
    letexTitle = ROOT.TLatex()
    letexTitle.SetTextSize(0.05)
    letexTitle.SetNDC()
    letexTitle.SetTextFont(42)
    
    
    c = ROOT.TCanvas(f"c_{ptMin[iPt]}_{ptMax[iPt]}", f"_{ptMin[iPt]}_{ptMax[iPt]}", 800, 600)
    c.SetTickx(1)
    c.SetTicky(1)
    # frame = tauz.frame(ROOT.RooFit.Title("Tauz data left side Mirrored"))
    
    # hTauzSigHist.plotOn(frame, ROOT.RooFit.Name("hTauzSigHist"), ROOT.RooFit.MarkerColor(color_set[0]), ROOT.RooFit.LineColor(color_set[0]))  
    # hTauzDataPromptHist.plotOn(frame, ROOT.RooFit.Name("hTauzDataPromptHist"), ROOT.RooFit.MarkerColor(color_set[1]), ROOT.RooFit.LineColor(color_set[1]))
    # hTauzDataNonPromptHist.plotOn(frame, ROOT.RooFit.Name("hTauzDataNonPromptHist"), ROOT.RooFit.MarkerColor(color_set[2]),  ROOT.RooFit.LineColor(color_set[2]))
    #combined_pdf.plotOn(frame, ROOT.RooFit.Name("combined_pdf"), ROOT.RooFit.MarkerColor(color_set[3]))
    
    hTauzSigDistr.SetLineColor(ROOT.kGreen)
    hTauzDataPromptDistr.SetLineColor(ROOT.kRed)
    hTauzDataNonPromptDistr.SetLineColor(ROOT.kBlue)
    
    hTauzSigDistr.Draw()
    hTauzSigDistr.GetXaxis().SetTitleSize(0.05)
    hTauzSigDistr.GetYaxis().SetTitleSize(0.05)
    hTauzSigDistr.GetXaxis().SetLabelSize(0.05)
    hTauzSigDistr.GetYaxis().SetLabelSize(0.05)
    hTauzSigDistr.GetXaxis().SetTitle(r"Pseudo proper decay time")
    hTauzSigDistr.GetYaxis().SetTitle(r"Events")
    hTauzDataPromptDistr.Draw("EP SAME")
    hTauzDataNonPromptDistr.Draw("EP SAME")
    
    legend = ROOT.TLegend(0.55, 0.65, 0.95, 0.85)
    legend.AddEntry(hTauzSigDistr, "OS data signal", "l")
    legend.AddEntry(hTauzDataPromptDistr, "Mirrored OS data signal", "l")
    legend.AddEntry(hTauzDataNonPromptDistr, "Subtracted non prompt", "l")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    #frame.Draw()
    
    letexTitle.DrawLatex(0.17, 0.88, "This study, pp, #sqrt{#it{s}} = 13.6 TeV")
    letexTitle.DrawLatex(0.17, 0.82, "J/#psi #rightarrow #mu^{+}#mu^{-}, 2.5 < #it{y} < 4")
    letexTitle.DrawLatex(0.17, 0.76, "MFT-MCH-MID tracks")
    
    c.Draw()
    legend.Draw()
    
    c.SaveAs(f"{PATH_IMGS}tauz_left_mirror_{ptMin[iPt]}_{ptMax[iPt]}.pdf")

    fl = ROOT.TFile(f"{PATH_DATA}tauzPromptMirror.root", "UPDATE")
    hTauzData.Write()
    hTauzSigDistr.Write()
    hTauzDataPromptDistr.Write()
    hTauzDataNonPromptDistr.Write()
    
    
    hTauzPromptTemplateInt = ROOT.TH1F(f"hTauzPromptTemplateInt_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    hTauzPromptTemplateInt.Add(hTauzPromptTemplate)
    hTauzPromptTemplateInt.Scale(1. / hTauzPromptTemplateInt.Integral())
    hTauzPromptTemplateInt.Write()
    
    hTauzNonPromptTemplateInt = ROOT.TH1F(f"hTauzNonPromptTemplateInt_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    hTauzNonPromptTemplateInt.Add(hTauzNonPromptTemplate)
    hTauzNonPromptTemplateInt.Scale(1. / hTauzNonPromptTemplateInt.Integral())
    hTauzNonPromptTemplateInt.Write()
    
    hTauzDataPromptDistrInt = ROOT.TH1F(f"hTauzDataPromptDistrInt_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    hTauzDataPromptDistrInt.Add(hTauzDataPromptDistr)
    hTauzDataPromptDistrInt.Scale(1. / hTauzDataPromptDistrInt.Integral())
    hTauzDataPromptDistrInt.Write()
    
    hTauzDataNonPromptDistrInt = ROOT.TH1F(f"hTauzDataNonPromptDistrInt_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
    hTauzDataNonPromptDistrInt.Add(hTauzDataNonPromptDistr)
    hTauzDataNonPromptDistrInt.Scale(1. / hTauzDataNonPromptDistrInt.Integral())
    hTauzDataNonPromptDistrInt.Write()
    fl.Close()

fl = ROOT.TFile(f"{PATH_DATA}tauzPromptMirror.root", "UPDATE")
hTauzDataNonPromptDistrSum.Write()
hTauzDataNonPromptDistrIntSum = ROOT.TH1F(f"hTauzDataNonPromptDistrIntSum_{ptMin[iPt]}_{ptMax[iPt]}","Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007)
hTauzDataNonPromptDistrIntSum.Add(hTauzDataNonPromptDistr)
hTauzDataNonPromptDistrIntSum.Scale(1. / hTauzDataNonPromptDistrIntSum.Integral())
hTauzDataNonPromptDistrIntSum.Write()
fl.Close()