import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/alice/"
PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"


template_file = ROOT.TFile(PATH_DATA + "template_tune_45_4-6.root")

ht_de = template_file.Get("ht")
ht_de.Scale(1. / ht_de.Integral())
htnon_de = template_file.Get("htnon")
htnon_de.Scale(1. / htnon_de.Integral())
hm_de = template_file.Get("hm")
hm_de.Scale(1. / hm_de.Integral())
hmnon_de = template_file.Get("hmnon")
hmnon_de.Scale(1. / hmnon_de.Integral())


data_file = ROOT.TFile(PATH_DATA + "data_tune_45_4-6.root")

ht_data_bg =  data_file.Get("ht_cut")
ht_data_bg.Scale(1. / ht_data_bg.Integral())

hm_data = data_file.Get("hm")
ht_data = data_file.Get("ht")




mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.003, 0.003)

mass.setRange("full", 2, 5)
mass.setRange("left", 2, 2.9)
mass.setRange("right", 3.2, 5)



datahist_m = ROOT.RooDataHist("datahistm", "DataHist m", ROOT.RooArgList(mass), hm_de)
datahist_m_non = ROOT.RooDataHist("datahistm_non", "DataHist m non", ROOT.RooArgList(mass), hmnon_de)
datahist_t = ROOT.RooDataHist("datahistt", "DataHist t", ROOT.RooArgList(tauz), ht_de)
datahist_t_non = ROOT.RooDataHist("datahistt_non", "DataHist t non", ROOT.RooArgList(tauz), htnon_de)
datahist_t_bg = ROOT.RooDataHist("datahistt_bg", "DataHist t bg", ROOT.RooArgList(tauz), ht_data_bg)

mass_pdf = ROOT.RooHistPdf("mass_pdf", "mass pdf", ROOT.RooArgList(mass), datahist_m)
mass_n_pdf = ROOT.RooHistPdf("mass_n_pdf", "mass n pdf", ROOT.RooArgList(mass), datahist_m_non)
tauz_pdf = ROOT.RooHistPdf("tauz_pdf", "tauz n pdf", ROOT.RooArgList(tauz), datahist_t)
tauz_n_pdf = ROOT.RooHistPdf("tauz_n_pdf", "tauz n pdf", ROOT.RooArgList(tauz), datahist_t_non)
tauz_bg_pdf = ROOT.RooHistPdf("tauz_bg_pdf", "tauz bg pdf", ROOT.RooArgList(tauz), datahist_t_bg)

datahist_data_m = ROOT.RooDataHist("datahistdatam", "DataHist data m", ROOT.RooArgList(mass), hm_data)
datahist_data_t = ROOT.RooDataHist("datahistdatat", "DataHist data t", ROOT.RooArgList(tauz), ht_data)


#mass crystal ball, chebyshev polynomials pt = 0-2
#----------------------------------------------------------------------------------------------------
# mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.8, -5, 10)
# n = ROOT.RooRealVar("n", "n", 2.2, -1, 10)
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
mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
alpha = ROOT.RooRealVar("alpha", "Alpha", 1, -10, 10)
n = ROOT.RooRealVar("n", "n", 1, -5, 10)
cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -2, 2) for i in range(6)]
cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
model_m_all = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

model_m_all.fitTo(datahist_data_m)
#-----------------------------------------------------------------------------------------------------
#mass crystal ball, chebyshev polynomials pt = 6-8
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
# #----------------------------------------------------------------------------------------------------
#mass crystal ball, chebyshev polynomials pt = 8-10
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


nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 10000,0,1e6)
nBkgVar = ROOT.RooRealVar("nBkg", "number of background", 100000,0,2e6)  
nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.1, 0, 1)

TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))



# fit with the histogram pdfs
#------------------------------------------------------------
model_t_all = ROOT.RooAddPdf("model_t_all", "tauz_n_pdf + tauz_pdf + bg_pdf", 
    ROOT.RooArgList(tauz_n_pdf, tauz_pdf, tauz_bg_pdf), 
    ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))
#------------------------------------------------------------

# fit with functions
#------------------------------------------------------------
workspace_file_nonprompt = ROOT.TFile(PATH_WORKSPACE + "tauz_nonprompt_landau_cheb_fit_workspace.root", "READ")
workspace_nonprompt = workspace_file_nonprompt.Get("tauz_nonprompt_fit_workspace")
model_t_nonprompt = workspace_nonprompt.pdf("model_nonprompt_pdf")
#model_t_nonprompt.fitTo(datahist_t_non)

workspace_file_prompt = ROOT.TFile(PATH_WORKSPACE + "tauz_prompt_bw_cheb_fit_workspace.root", "READ")
workspace_prompt = workspace_file_prompt.Get("tauz_prompt_fit_workspace")
model_t_prompt = workspace_prompt.pdf("model_prompt_pdf")
#model_t_prompt.fitTo(datahist_t)

workspace_file_background = ROOT.TFile(PATH_WORKSPACE + "tauz_background_bw_cheb_fit_workspace.root", "READ")
workspace_background = workspace_file_background.Get("tauz_background_fit_workspace")
model_t_background = workspace_background.pdf("model_background_pdf")
#model_t_background.fitTo(datahist_t_bg)

# model_t_all = ROOT.RooAddPdf("model_t_all", "tauz_n_pdf + tauz_pdf + bg_pdf",
#     ROOT.RooArgList(model_t_nonprompt, model_t_prompt, model_t_background),
#     ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))



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
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_all_pdf"), Slice=(cat, "massCat"), ProjWData=(cat,combData))
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_pdf"), Slice=(cat, "massCat"), Components="mass_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_n_pdf"), Slice=(cat, "massCat"), Components="mass_n_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
#simfit.plotOn(frame1, ROOT.RooFit.Name("mass_bg_pdf"), Slice=(cat, "massCat"), Components="model_bg_m", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)


frame2 = tauz.frame(ROOT.RooFit.Title("Pseudo Proper Decay Length Fit Result"), )
combData.plotOn(frame2, ROOT.RooFit.Cut("cat==cat::tauzCat"))
#data_t.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_all_pdf"), Slice=(cat, "tauzCat"), ProjWData=(cat,combData))
simfit.plotOn(frame2, ROOT.RooFit.Name("model_prompt_pdf"), Slice=(cat, "tauzCat"), Components="model_prompt_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
simfit.plotOn(frame2, ROOT.RooFit.Name("model_nonprompt_pdf"), Slice=(cat, "tauzCat"), Components="model_nonprompt_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
simfit.plotOn(frame2, ROOT.RooFit.Name("model_background_pdf"), Slice=(cat, "tauzCat"), Components="model_background_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)
model_t_prompt.plotOn(frame2, LineColor=ROOT.kRed+1)
model_t_background.plotOn(frame2, LineColor=ROOT.kGreen+1)
model_t_nonprompt.plotOn(frame2, LineColor=ROOT.kBlue+1)


canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

legend1 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
legend1.AddEntry(frame1.findObject("mass_all_pdf"), "Invariant mass fit", "l")

legend2 = ROOT.TLegend(0.55, 0.55, 0.85, 0.75)
legend2.AddEntry(frame2.findObject("tauz_all_pdf"), "PPDL fit", "l")
legend2.AddEntry(frame2.findObject("tauz_pdf"), "Prompt fraction", "l")
legend2.AddEntry(frame2.findObject("tauz_n_pdf"), "Non prompt fraction", "l")
legend2.AddEntry(frame2.findObject("tauz_bg_pdf"), "Background", "l")


canvas.Divide(2,1)
canvas.cd(1)
frame1.Draw()
legend1.Draw()

canvas.cd(2)#.SetLogy()
frame2.Draw()
legend2.Draw()

canvas.Update()
canvas.SaveAs(PATH_IMGS + "simul_fit_data_4-6.png")



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