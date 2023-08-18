import ROOT
from ROOT import *

PATH_DATA = "root_files/"
PATH_IMGS = "imgs/"


template_file = ROOT.TFile(PATH_DATA + "template_tune_45_6-10.root")

data_file = ROOT.TFile(PATH_DATA + "data_tune_45_6-10_bkg_extr.root")


hm_data = data_file.Get("hm")
ht_data = data_file.Get("ht")



mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.01, 0.01)

# mass.setRange("full", 2, 5)
# mass.setRange("left", 2, 2.9)
# mass.setRange("right", 3.2, 5)


datahist_data_m = ROOT.RooDataHist("datahistdatam", "DataHist data m", ROOT.RooArgList(mass), hm_data)
datahist_data_t = ROOT.RooDataHist("datahistdatat", "DataHist data t", ROOT.RooArgList(tauz), ht_data)


#mass crystal ball, chebyshev polynomials pt = 0-2
#----------------------------------------------------------------------------------------------------
# mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.8, -5, 10)
# n = ROOT.RooRealVar("n", "n", 2.2, -1, 50)
# cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -2, 2) for i in range(6)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

# cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
# model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

# model_m_all.fitTo(datahist_data_m)
# #----------------------------------------------------------------------------------------------------

#mass crystal ball, chebyshev polynomials pt = 2-4
#----------------------------------------------------------------------------------------------------
# mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.5, -5, 10)
# n = ROOT.RooRealVar("n", "n", 4, -1, 10)
# cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -2, 2) for i in range(6)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

# cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
# model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

# model_m_all.fitTo(datahist_data_m)
#----------------------------------------------------------------------------------------------------

#mass crystal ball, chebyshev polynomials pt = 4-6
#----------------------------------------------------------------------------------------------------
# mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.05, 0.03, 0.12)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.2, -10, 10)
# n = ROOT.RooRealVar("n", "n", 3, -5, 50)
# cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -3.5, 3.5) for i in range(6)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

# cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
# model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

# model_m_all.fitTo(datahist_data_m)
#-----------------------------------------------------------------------------------------------------
#mass crystal ball, chebyshev polynomials pt = 6-8
#----------------------------------------------------------------------------------------------------


mean_mass = ROOT.RooRealVar("mean_mass", "mean_mass", 3.08869e+00, 2.9, 3.5)
sigma_mass = ROOT.RooRealVar("sigma_mass", "Sigma",  9.67680e-02, 0, 1)
alpha_mass = ROOT.RooRealVar("alpha_mass", "Alpha", -9.21012e-01)
n_mass = ROOT.RooRealVar("n_mass", "n_mass",2.09918e+00)
cb_pdf_mass = ROOT.RooCBShape("cb_pdf_mass", "Crystal Ball PDF", mass, mean_mass, sigma_mass, alpha_mass, n_mass)

cheb_coeffs_mass = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -3.5, 3.5) for i in range(6)]

#coefs_mass = [-9.57813e-01, 6.21144e-02, 7.22575e-02, 4.49786e-02, -7.54956e-02,  3.04565e-02]
coefs_mass = [-9.18303e-01, 2.50965e-01, -1.47898e-02, -3.26950e-02, 5.06778e-03, 3.09662e-02]

for i, coef_value in enumerate(coefs_mass):
    cheb_coeffs_mass[i].setVal(coef_value)
    cheb_coeffs_mass[i].setConstant(True)

cheb_poly_mass = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs_mass))



# cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
# model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))



# model_m_all.fitTo(datahist_data_m)


# #----------------------------------------------------------------------------------------------------
#mass crystal ball, chebyshev polynomials pt = 8-10
#----------------------------------------------------------------------------------------------------
# mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.2, -5, 10)
# n = ROOT.RooRealVar("n", "n", 1, -1, 1000)
# cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -2, 2) for i in range(6)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

# cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
# model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

# model_m_all.fitTo(datahist_data_m)
#----------------------------------------------------------------------------------------------------

data_m = ROOT.RooDataSet("data_m", "Data Set m", ROOT.RooArgSet(mass),  ROOT.RooFit.Import(datahist_data_m))
data_t = ROOT.RooDataSet("data_t", "Data Set t", ROOT.RooArgSet(tauz),  ROOT.RooFit.Import(datahist_data_t))


event_num = 100000
signalToBackground = 0.1
fb = 0.1
nSig = event_num*signalToBackground
nBkg = event_num*(1-signalToBackground)

prompt_num = nSig*(1-fb)
non_prompt_num = nSig*fb 
entry_num = prompt_num + non_prompt_num
m_bg_num = nBkg
t_bg_num = nBkg


nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 4.05081e+04, 0, 1e6)
nBkgVar = ROOT.RooRealVar("nBkg", "number of background",  2.17768e+05, 2e4, 4e8)  
nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.15, 0, 1)

TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))

model_m_all = ROOT.RooAddPdf("model_m_all", "Crystal Ball + Chebyshev", 
    ROOT.RooArgList(cb_pdf_mass, cheb_poly_mass), 
    ROOT.RooArgList(nJPsi, nBkgVar))




# fit with the histogram pdfs
#------------------------------------------------------------
# model_t_all = ROOT.RooAddPdf("model_t_all", "tauz_n_pdf + tauz_pdf + bg_pdf", 
#     ROOT.RooArgList(tauz_n_pdf, tauz_pdf, tauz_bg_pdf), 
#     ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))
#------------------------------------------------------------

# fit with functions
#------------------------------------------------------------
# workspace_file_nonprompt = ROOT.TFile(PATH_WORKSPACE + "tauz_nonprompt_landau_cheb_fit_workspace.root", "READ")
# workspace_nonprompt = workspace_file_nonprompt.Get("tauz_nonprompt_fit_workspace")
# model_t_nonprompt = workspace_nonprompt.pdf("model_nonprompt_pdf")

# workspace_file_prompt = ROOT.TFile(PATH_WORKSPACE + "tauz_prompt_bw_cheb_fit_workspace.root", "READ")
# workspace_prompt = workspace_file_prompt.Get("tauz_prompt_fit_workspace")
# model_t_prompt = workspace_prompt.pdf("model_prompt_pdf")

# workspace_file_background = ROOT.TFile(PATH_WORKSPACE + "tauz_background_bw_cheb_fit_workspace.root", "READ")
# workspace_background = workspace_file_background.Get("tauz_background_fit_workspace")
# model_t_background = workspace_background.pdf("model_background_pdf")

# mean_bw_tauz_bkg = ROOT.RooRealVar("mean_bw_tauz_bkg", "mean_bw_tauz_bkg", 0.0)#2.35457e-04)
# width_bw_tauz_bkg = ROOT.RooRealVar("width_bw_tauz_bkg", "width_bw_tauz_bkg", 1.86791e-03)
# bw_pdf_tauz_bkg = ROOT.RooBreitWigner("bw_pdf_tauz_bkg", "bw_pdf_tauz_bkg", tauz, mean_bw_tauz_bkg, width_bw_tauz_bkg)

# cheb_coeffs_tauz_bkg = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -0.2, 0.2) for i in range(4)]
# cheb_poly_tauz_bkg = ROOT.RooChebychev("cheb_poly_tauz_bkg", "cheb_poly_tauz_bkg", tauz, ROOT.RooArgList(*cheb_coeffs_tauz_bkg))

# coefs_tauz_bkg = [ 8.99858e-03,-1.95669e-01, -4.76269e-02, -3.37895e-03]
# for i, coef_value in enumerate(coefs_tauz_bkg):
#     cheb_coeffs_tauz_bkg[i].setVal(coef_value)
#     cheb_coeffs_tauz_bkg[i].setConstant(True)

mean_bw_tauz_bkg = ROOT.RooRealVar("mean_bw_tauz_bkg", "Mean bw", 8.323918826602661e-05)
width_bw_tauz_bkg = ROOT.RooRealVar("width_bw_tauz_bkg", "Width bw", 0.0011265097652047307)
bw_pdf_tauz_bkg = ROOT.RooBreitWigner("bw_tauz_bkg", "Breit-Wigner Distribution", tauz, mean_bw_tauz_bkg, width_bw_tauz_bkg)


mean_cb_tauz_bkg = ROOT.RooRealVar("mean_cb_tauz_bkg", "Mean_cb",  0.0012540488964024599)
sigma_cb_tauz_bkg = ROOT.RooRealVar("sigma_cb_tauz_bkg", "Sigma",0.007821523272251163)
alpha_cb_tauz_bkg = ROOT.RooRealVar("alpha_cb_tauz_bkg", "Alpha", -6.8068415906107305)
n_cb_tauz_bkg = ROOT.RooRealVar("n_cb_tauz_bkg", "n", 9.53673999992688e-05)
cb_pdf_tauz_bkg = ROOT.RooCBShape("cb_pdf_tauz_bkg", "Crystal Ball PDF", tauz, mean_cb_tauz_bkg, sigma_cb_tauz_bkg, alpha_cb_tauz_bkg, n_cb_tauz_bkg)

model_frac_tauz_bkg = ROOT.RooRealVar("model_frac_tauz_bkg", "model_frac_tauz_bkg", 1.22147e-01)
model_tauz_bkg = ROOT.RooAddPdf("model_tauz_bkg", "model_tauz_bkg", ROOT.RooArgList(bw_pdf_tauz_bkg, cb_pdf_tauz_bkg), ROOT.RooArgList(model_frac_tauz_bkg))


mean_landau_tauz_nonprompt = ROOT.RooRealVar("mean_landau_tauz_nonprompt", "mean_landau_tauz_nonprompt",  4.00748e-04)
scale_landau_tauz_nonprompt = ROOT.RooRealVar("scale_landau_tauz_nonprompt", "scale_landau_tauz_nonprompt", 3.71723e-04)


landau_pdf_tauz_nonprompt = ROOT.RooLandau("landau", "Landau PDF", tauz, mean_landau_tauz_nonprompt, scale_landau_tauz_nonprompt)

cheb_coeffs_tauz_nonprompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.26, 0.26) for i in range(2)]
cheb_poly_tauz_nonprompt = ROOT.RooChebychev("cheb_poly_tauz_nonprompt", "cheb_poly_tauz_nonprompt", tauz, ROOT.RooArgList(*cheb_coeffs_tauz_nonprompt))

model_frac_tauz_nonprompt = ROOT.RooRealVar("model_frac_tauz_nonprompt", "model_frac_tauz_nonprompt", 7.44723e-01)

coefs_tauz_nonprompt = [-2.69301e-01, -3.80000e-01]
for i, coef_value in enumerate(coefs_tauz_nonprompt):
    cheb_coeffs_tauz_nonprompt[i].setVal(coef_value)
    cheb_coeffs_tauz_nonprompt[i].setConstant(True)

cheb_poly_tauz_nonprompt = ROOT.RooChebychev("cheb_poly_tauz_nonprompt", "cheb_poly_tauz_nonprompt", mass, ROOT.RooArgList(*cheb_coeffs_tauz_nonprompt))

model_tauz_nonprompt = ROOT.RooAddPdf("model_tauz_nonprompt", "model_tauz_nonprompt", ROOT.RooArgList(landau_pdf_tauz_nonprompt, cheb_poly_tauz_nonprompt), ROOT.RooArgList(model_frac_tauz_nonprompt))




mean_bw_tauz_prompt = ROOT.RooRealVar("mean_bw_tauz_prompt", "mean_bw_tauz_prompt", 9.08367e-06)
width_bw_tauz_prompt = ROOT.RooRealVar("width_bw_tauz_prompt", "width_bw_tauz_prompt",  3.21467e-04)
bw_pdf_tauz_prompt = ROOT.RooBreitWigner("bw_pdf_tauz_prompt", "bw_pdf_tauz_prompt", tauz, mean_bw_tauz_prompt, width_bw_tauz_prompt)

cheb_coeffs_tauz_prompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -0.2, 0.2) for i in range(3)]
cheb_poly_tauz_prompt = ROOT.RooChebychev("cheb_poly_tauz_prompt", "cheb_poly_tauz_prompt", tauz, ROOT.RooArgList(*cheb_coeffs_tauz_prompt))

model_frac_tauz_prompt = ROOT.RooRealVar("cb_frac_tauz_prompt", "cb_frac_tauz_prompt", 8.53754e-01)

coefs_tauz_prompt = [-9.80402e-02, -1.94740e-01, 8.03672e-02]
for i, coef_value in enumerate(coefs_tauz_prompt):
    cheb_coeffs_tauz_prompt[i].setVal(coef_value)
    cheb_coeffs_tauz_prompt[i].setConstant(True)

cheb_poly_tauz_prompt = ROOT.RooChebychev("cheb_poly_tauz_prompt", "cheb_poly_tauz_prompt", mass, ROOT.RooArgList(*cheb_coeffs_tauz_prompt))

model_tauz_prompt = ROOT.RooAddPdf("model_tauz_prompt", "model_tauz_prompt", ROOT.RooArgList(bw_pdf_tauz_prompt, cheb_poly_tauz_prompt), ROOT.RooArgList(model_frac_tauz_prompt))





model_t_all = ROOT.RooAddPdf("model_t_all", "tauz_n_pdf + tauz_pdf + tauz_bg_pdf",
    ROOT.RooArgList(model_tauz_nonprompt, model_tauz_prompt, model_tauz_bkg),
    ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))




#------------------------------------------------------------


cat = ROOT.RooCategory("cat", "cat")
cat.defineType("massCat")
cat.defineType("tauzCat")

simfit = ROOT.RooSimultaneous("simfit", "", cat)
#simfit.addPdf(model_m,"massCat")
simfit.addPdf(model_m_all, "massCat")
simfit.addPdf(model_t_all,"tauzCat")


print(entry_num)

combData = ROOT.RooDataSet("combData", "combined data",
    {mass, tauz}, 
    Index=cat, 
    Import={"massCat": data_m, "tauzCat": data_t},
)

fitResult = simfit.fitTo(combData, Extended=True, Save=True, PrintLevel=-1)
fitResult.Print()
# pr_res = "Prompt num: {0}/{1}".format(prompt_num, nJPsi)
# non_pr_res = "Non-Prompt num: {0}/{1}".format(non_prompt_num, nJPsiNon)

frac_res = "Prompt num: {0}/{1}".format(non_prompt_num/(prompt_num + non_prompt_num), nonPrompFrac)

print("-------------------------------------------------------------------")

# with open("mc_valid.txt", "a") as file:
#     file.write(f"{frac_res}")

frame1 = mass.frame(ROOT.RooFit.Title("Invariant Mass Fit Result"))
combData.plotOn(frame1, ROOT.RooFit.Cut("cat==cat::massCat"))
#data.plotOn(framep,RooFit.Cut("cat==cat::massCat"))
#data_m.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_all_pdf"), Slice=(cat, "massCat"), ProjWData=(cat,combData), Binning=200)
#simfit.plotOn(frame1, ROOT.RooFit.Name("mass_pdf"), Slice=(cat, "massCat"), Components="mass_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
#simfit.plotOn(frame1, ROOT.RooFit.Name("mass_n_pdf"), Slice=(cat, "massCat"), Components="mass_n_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
#simfit.plotOn(frame1, ROOT.RooFit.Name("mass_bg_pdf"), Slice=(cat, "massCat"), Components="model_bg_m", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)


frame2 = tauz.frame(ROOT.RooFit.Title("Pseudo Proper Decay Length Fit Result"), )
combData.plotOn(frame2, ROOT.RooFit.Cut("cat==cat::tauzCat"))
#data_t.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_all_pdf"), Slice=(cat, "tauzCat"), ProjWData=(cat,combData))
simfit.plotOn(frame2, ROOT.RooFit.Name("model_prompt_pdf"), Slice=(cat, "tauzCat"), Components="model_tauz_prompt", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
simfit.plotOn(frame2, ROOT.RooFit.Name("model_nonprompt_pdf"), Slice=(cat, "tauzCat"), Components="model_tauz_nonprompt", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
simfit.plotOn(frame2, ROOT.RooFit.Name("model_background_pdf"), Slice=(cat, "tauzCat"), Components="model_tauz_bkg", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)
# model_t_prompt.plotOn(frame2, LineColor=ROOT.kRed+1)
# model_t_background.plotOn(frame2, LineColor=ROOT.kGreen+1)
# model_t_nonprompt.plotOn(frame2, LineColor=ROOT.kBlue+1)

# yaxis = frame2.GetYaxis()
# y_min = 100  # Minimum y-axis value
# y_max = 1000  # Maximum y-axis value
# yaxis.SetRangeUser(y_min, y_max)


canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

legend1 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
legend1.AddEntry(frame1.findObject("mass_all_pdf"), "Invariant mass fit", "l")

legend2 = ROOT.TLegend(0.55, 0.80, 0.85, 0.90)
legend2.AddEntry(frame2.findObject("tauz_all_pdf"), "PPDL fit", "l")
legend2.AddEntry(frame2.findObject("model_prompt_pdf"), "Prompt fraction", "l")
legend2.AddEntry(frame2.findObject("model_nonprompt_pdf"), "Non prompt fraction", "l")
legend2.AddEntry(frame2.findObject("model_background_pdf"), "Background", "l")


canvas.Divide(2,1)
canvas.cd(1)
frame1.Draw()
legend1.Draw()

canvas.cd(2).SetLogy()
frame2.Draw()
legend2.Draw()

canvas.Update()
canvas.SaveAs(PATH_IMGS + "simul_fit_data_6-10_fc.png")



# workspace_file_prompt = ROOT.TFile(PATH_WORKSPACE + "tauz_prompt_bw_cheb_fit_workspace.root", "READ")
# workspace_prompt = workspace_file_prompt.Get("tauz_prompt_fit_workspace")
# model_t_prompt = workspace_prompt.pdf("model_prompt_pdf")

# f = tauz.frame(ROOT.RooFit.Title("Invariant mass background")) 
# #datahist_data_t.plotOn(frame)
# #model_t.plotOn(frame)
# model_t_prompt.plotOn(f)

# c = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
# f.Draw()
# c.Draw()

# c.SaveAs(PATH_IMGS + "tauz_template_prompt_fit_test.png")