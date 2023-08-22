import ROOT
from ROOT import TFile, RooRealVar, RooDataHist, RooArgList, RooFit, RooHistPdf
import time
import concurrent.futures
import math
import numpy as np
import numpy

PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"


ls_fit_file = ROOT.TFile(PATH_DATA + "data_tune_45_4-6_bkg_extr.root")
ht_ls_sig_data = ls_fit_file.Get("ht_sig")
ht_ls_bkg_data = ls_fit_file.Get("ht_bkg")
#ht_sig.Scale(1. / ht_sig.Integral())

ht_template_file = ROOT.TFile(PATH_DATA + "template_tune_45_4-6.root")
ht_template_prompt = ht_template_file.Get("ht")
ht_template_nonprompt = ht_template_file.Get("htnon")


tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

datahist_ls_sig = ROOT.RooDataHist("datahist_ls_sig", "datahist_ls_sig", ROOT.RooArgList(tauz), ht_ls_sig_data)
datahist_prompt = ROOT.RooDataHist("datahist_prompt", "datahist_prompt", ROOT.RooArgList(tauz), ht_template_prompt)
datahist_nonprompt = ROOT.RooDataHist("datahist_nonprompt", "datahist_nonprompt", ROOT.RooArgList(tauz), ht_template_nonprompt)
datahist_bkg = ROOT.RooDataHist("datahist_bkg", "datahist_bkg", ROOT.RooArgList(tauz), ht_ls_bkg_data)

#-------------------------------PROMPT-----------------------------------------
mean_bw_tauz_prompt = ROOT.RooRealVar("mean_bw_tauz_prompt", "mean_bw_tauz_prompt", -1.29422e-04)
width_bw_tauz_prompt = ROOT.RooRealVar("width_bw_tauz_prompt", "width_bw_tauz_prompt",  7.13980e-03)
pdf_bw_tauz_prompt = ROOT.RooBreitWigner("pdf_bw_tauz_prompt", "pdf_bw_tauz_prompt", tauz, mean_bw_tauz_prompt, width_bw_tauz_prompt)
mean_gauss_tauz_prompt = ROOT.RooRealVar("mean_gauss_tauz_prompt", "mean_gauss_tauz_prompt", 4.81673e-06)
sigma_gauss_tauz_prompt = ROOT.RooRealVar("sigma_gauss_tauz_prompt", "sigma_gauss_tauz_prompt",  2.03266e-04)
pdf_gauss_tauz_prompt = ROOT.RooGaussian("pdf_gauss_tauz_prompt", "pdf_gauss_tauz_prompt", tauz, mean_gauss_tauz_prompt, sigma_gauss_tauz_prompt)
model_frac_tauz_prompt = ROOT.RooRealVar("model_frac_tauz_prompt", "model_frac_tauz_prompt", 2.42878e-01 )
model_tauz_prompt = ROOT.RooAddPdf("model_tauz_prompt", "Breit Wiegner + Gauss", ROOT.RooArgList(pdf_bw_tauz_prompt, pdf_gauss_tauz_prompt), ROOT.RooArgList(model_frac_tauz_prompt))



#-------------------------------NONPROMPT----------------------------------------
location_landau_tauz_nonprompt = ROOT.RooRealVar("location_landau_tauz_nonprompt", "location_landau_tauz_nonprompt", 3.95811e-04 )
scale_landau_tauz_nonprompt = ROOT.RooRealVar("scale_landau_tauz_nonprompt", "scale_landau_tauz_nonprompt", 3.60112e-04)
pdf_landau_tauz_nonprompt = ROOT.RooLandau("pdf_landau_tauz_nonprompt", "pdf_landau_tauz_nonprompt", tauz, location_landau_tauz_nonprompt, scale_landau_tauz_nonprompt)
cheb_coeffs_landau_tauz_nonprompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.46, 0.46) for i in range(2)]

coefs_tauz_nonprompt = [-6.33903e-02, -3.60000e-01]
for i, coef_value in enumerate(coefs_tauz_nonprompt):
    cheb_coeffs_landau_tauz_nonprompt[i].setVal(coef_value)
    cheb_coeffs_landau_tauz_nonprompt[i].setConstant(True)

cheb_poly_landau_tauz_nonprompt = ROOT.RooChebychev("cheb_poly_landau_tauz_nonprompt", "cheb_poly_landau_tauz_nonprompt", tauz, ROOT.RooArgList(*cheb_coeffs_landau_tauz_nonprompt))
model_frac_tauz_nonprompt = ROOT.RooRealVar("cb_frac_tauz_nonprompt", "CB Fraction",  7.45875e-01)
model_tauz_nonprompt = ROOT.RooAddPdf("model_tauz_nonprompt", "Landau + Chebyshev", ROOT.RooArgList(pdf_landau_tauz_nonprompt, cheb_poly_landau_tauz_nonprompt), ROOT.RooArgList(model_frac_tauz_nonprompt))
#---------------------------------BKG-------------------------------------------

# cheb_coeffs_tauz_bkg = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.35, 0.35) for i in range(4)]
# cheb_poly_tauz_bkg = ROOT.RooChebychev("cheb_poly_tauz_bkg", "cheb_poly_tauz_bkg", tauz, ROOT.RooArgList(*cheb_coeffs_tauz_bkg))

# mean_gauss_tauz_bkg = ROOT.RooRealVar("mean_gauss_tauz_bkg", "mean_gauss_tauz_bkg", 0, -0.1, 0.1)
# sigma_gauss_tauz_bkg = ROOT.RooRealVar("sigma_gauss_tauz_bkg", "sigma_gauss_tauz_bkg", 0.005, 0, 0.1)
# pdf_gauss_tauz_bkg = ROOT.RooGaussian("pdf_gauss_tauz_bkg", "pdf_gauss_tauz_bkg", tauz, mean_gauss_tauz_bkg, sigma_gauss_tauz_bkg)


mean_bw_tauz_bkg = ROOT.RooRealVar("mean_bw_tauz_bkg", "Mean bw", 9.31848e-05 )
width_bw_tauz_bkg = ROOT.RooRealVar("width_bw_tauz_bkg", "Width bw", 1.27135e-03)
bw_pdf_tauz_bkg = ROOT.RooBreitWigner("bw_tauz_bkg", "Breit-Wigner Distribution", tauz, mean_bw_tauz_bkg, width_bw_tauz_bkg)


mean_cb_tauz_bkg = ROOT.RooRealVar("mean_cb_tauz_bkg", "Mean_cb",   5.86639e-04 )
sigma_cb_tauz_bkg = ROOT.RooRealVar("sigma_cb_tauz_bkg", "Sigma", 8.75250e-03)
alpha_cb_tauz_bkg = ROOT.RooRealVar("alpha_cb_tauz_bkg", "Alpha",  -3.72729e+00 )
n_cb_tauz_bkg = ROOT.RooRealVar("n_cb_tauz_bkg", "n", 6.40637e-01)
cb_pdf_tauz_bkg = ROOT.RooCBShape("cb_pdf_tauz_bkg", "Crystal Ball PDF", tauz, mean_cb_tauz_bkg, sigma_cb_tauz_bkg, alpha_cb_tauz_bkg, n_cb_tauz_bkg)


model_frac_tauz_bkg = ROOT.RooRealVar("model_frac_tauz_bkg", "model_frac_tauz_bkg", 1.56427e-01)
model_tauz_bkg = ROOT.RooAddPdf("model_tauz_bkg", "model_tauz_bkg", ROOT.RooArgList(bw_pdf_tauz_bkg, cb_pdf_tauz_bkg), ROOT.RooArgList(model_frac_tauz_bkg))
#-------------------------------------------------------------------------------

nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 1e4, 1e3, 1e7)
nBkgVar = ROOT.RooRealVar("nBkg", "number of background",  2.17768e+05, 2e4, 4e8)  
nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.15, 0 ,1)

TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))

model_tauz_prompt_nonprompt  = ROOT.RooAddPdf("model_tauz_prompt_nonprompt", "tauz_n_pdf + tauz_pdf",
    ROOT.RooArgList(model_tauz_nonprompt, model_tauz_prompt, model_tauz_bkg),
    ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))

# model_tauz_prompt.fitTo(datahist_prompt)
# model_tauz_nonprompt.fitTo(datahist_nonprompt)
# model_tauz_bkg.fitTo(datahist_bkg)
model_tauz_prompt_nonprompt.fitTo(datahist_ls_sig)

frame = tauz.frame(ROOT.RooFit.Title("")) 
datahist_ls_sig.plotOn(frame, ROOT.RooFit.MarkerColor(ROOT.kRed+1))
datahist_prompt.plotOn(frame, ROOT.RooFit.MarkerColor(ROOT.kBlue+1))
datahist_nonprompt.plotOn(frame,  ROOT.RooFit.MarkerColor(ROOT.kGreen+1))
datahist_bkg.plotOn(frame,  ROOT.RooFit.MarkerColor(ROOT.kMagenta+1))

model_tauz_prompt.plotOn(frame,ROOT.RooFit.Name("model_tauz_prompt"),LineStyle="--", LineColor=ROOT.kBlue+1)
model_tauz_nonprompt.plotOn(frame,ROOT.RooFit.Name("model_tauz_nonprompt"),LineStyle="--", LineColor=ROOT.kGreen+1)
model_tauz_bkg.plotOn(frame,ROOT.RooFit.Name("model_tauz_bkg"),LineStyle="--", LineColor=ROOT.kMagenta+1)
model_tauz_prompt_nonprompt.plotOn(frame,ROOT.RooFit.Name("model_tauz_prompt_nonprompt"),LineColor=ROOT.kRed+1)
#cheb_poly.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 1280, 720)

legend = ROOT.TLegend(0.55, 0.80, 0.85, 0.90)
legend.AddEntry(frame.findObject("model_tauz_prompt_nonprompt"), "Like sign signal", "l")
legend.AddEntry(frame.findObject("model_tauz_prompt"), "Prompt fraction", "l")
legend.AddEntry(frame.findObject("model_tauz_nonprompt"), "Non prompt fraction", "l")
legend.AddEntry(frame.findObject("model_tauz_bkg"), "Background", "l")


#canvas.SetLogy()
frame.Draw()
canvas.Draw()
legend.Draw()

canvas.SaveAs(PATH_IMGS + "tauz_ls_no_bkg_fit.png")

