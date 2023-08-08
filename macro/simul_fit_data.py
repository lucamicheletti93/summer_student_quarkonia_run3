import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/alice/"
PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/"

file1 = ROOT.TFile(PATH + "ht.root")
ht_de = file1.Get("ht")
ht_de.Scale(1. / ht_de.Integral())

file2 = ROOT.TFile(PATH + "htnon.root")
htnon_de = file2.Get("htnon")
htnon_de.Scale(1. / htnon_de.Integral())

ht_data_file_bg = ROOT.TFile(PATH_DATA + "ht_data_cut_tune_45_4-6.root")
ht_data_bg = ht_data_file_bg.Get("ht")
ht_data_bg.Scale(1. / ht_data_bg.Integral())



file3 = ROOT.TFile(PATH + "hm.root")
hm_de = file3.Get("hm")
hm_de.Scale(1. / hm_de.Integral())

file4 = ROOT.TFile(PATH + "hmnon.root")
hmnon_de = file4.Get("hmnon")
hmnon_de.Scale(1. / hmnon_de.Integral())

hm_data_file_bg = ROOT.TFile(PATH_DATA + "hm_data_bg_tune_45_4-6.root")
hm_data_bg = hm_data_file_bg.Get("hm")
hm_data_bg.Scale(1. / hm_data_bg.Integral())



file_data_m = ROOT.TFile(PATH_DATA + "hm_data_tune_45_4-6.root")
hm_data = file_data_m.Get("hm")
hm_data.Scale(1. / hm_data.Integral())


file_data_t = ROOT.TFile(PATH_DATA + "ht_data_tune_45_4-6.root")
ht_data = file_data_t.Get("ht")
ht_data.Scale(1. / ht_data.Integral())


mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
tau = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.01, 0.01)



lambda_param = ROOT.RooRealVar("lambda_param", "Exponential decay constant", 0, -5, 0)
model_bg_m = ROOT.RooExponential("model_bg_m", "Exponential PDF", mass, lambda_param)

mass.setRange("full", 2, 5)
mass.setRange("left", 2, 2.9)
mass.setRange("right", 3.2, 5)


datahist_m_databg = ROOT.RooDataHist("datahistmdatabg", "DataHist m data bg", ROOT.RooArgList(mass), hm_data_bg)
model_bg_m.fitTo(datahist_m_databg, Range="left,right", PrintLevel=-1)
roofit_dataset = model_bg_m.generate(ROOT.RooArgSet(mass), 10000)
blindedData = roofit_dataset.reduce(CutRange="left,right")
#lambda_param.setVal(-2.0)
model_bg_m.fitTo(blindedData, Range="left,right")
lambda_param.setConstant(True)


datahist_m = ROOT.RooDataHist("datahistm", "DataHist m", ROOT.RooArgList(mass), hm_de)
datahist_m_non = ROOT.RooDataHist("datahistm_non", "DataHist m non", ROOT.RooArgList(mass), hmnon_de)
datahist_t = ROOT.RooDataHist("datahistt", "DataHist t", ROOT.RooArgList(tau), ht_de)
datahist_t_non = ROOT.RooDataHist("datahistt_non", "DataHist t non", ROOT.RooArgList(tau), htnon_de)
datahist_t_bg = ROOT.RooDataHist("datahistt_bg", "DataHist t bg", ROOT.RooArgList(tau), ht_data_bg)

mass_pdf = ROOT.RooHistPdf("mass_pdf", "mass pdf", ROOT.RooArgList(mass), datahist_m)
mass_n_pdf = ROOT.RooHistPdf("mass_n_pdf", "mass n pdf", ROOT.RooArgList(mass), datahist_m_non)
tauz_pdf = ROOT.RooHistPdf("tauz_pdf", "tauz n pdf", ROOT.RooArgList(tau), datahist_t)
tauz_n_pdf = ROOT.RooHistPdf("tauz_n_pdf", "tauz n pdf", ROOT.RooArgList(tau), datahist_t_non)
tauz_bg_pdf = ROOT.RooHistPdf("tauz_bg_pdf", "tauz bg pdf", ROOT.RooArgList(tau), datahist_t_bg)

datahist_data_m = ROOT.RooDataHist("datahistdatam", "DataHist data m", ROOT.RooArgList(mass), hm_data)
datahist_data_t = ROOT.RooDataHist("datahistdatat", "DataHist data t", ROOT.RooArgList(tau), ht_data)


data_m = ROOT.RooDataSet("data_m", "Data Set m", ROOT.RooArgSet(mass),  ROOT.RooFit.Import(datahist_data_m))
data_t = ROOT.RooDataSet("data_t", "Data Set t", ROOT.RooArgSet(tau),  ROOT.RooFit.Import(datahist_data_t))

# prompt_num =  62963
# non_prompt_num = 131628

#data_m.merge(data_m_non)
#data_t.merge(data_t_non)

# combined_data_m = ROOT.RooDataHist("combined_data_m", "Combined Data m", ROOT.RooArgList(mass))
# combined_data_m.add(data_m, 1)
# combined_data_m.add(data_m_non, 1)

# combined_data_t = ROOT.RooDataHist("combined_data_t", "Combined Data t", ROOT.RooArgList(tau))
# combined_data_t.add(data_t, 1)
# combined_data_t.add(data_t_non, 1)

entry_fracs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
entry_fracs_len = len(entry_fracs) 


# for i in range(entry_fracs_len):


event_num = 100000
signalToBackground = 0.5
fb = 0.1
nSig = event_num*signalToBackground
nBkg = event_num*(1-signalToBackground)

prompt_num = nSig*(1-fb) #entry_fracs[i]
non_prompt_num = nSig*fb #entry_fracs[entry_fracs_len - i - 1]
entry_num = prompt_num + non_prompt_num
m_bg_num = nBkg
t_bg_num = nBkg



#nJPsiAll = ROOT.RooRealVar("nJPsi", "number of JPsi", entry_num)

nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 1000,0,2*entry_num)
nBkg = ROOT.RooRealVar("nBkg", "number of background", 1000,0,2*nBkg) 
nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.1, 0, 1)
#nonPrompFrac.setConstant(True)

TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))
#nJPsiNon = ROOT.RooRealVar("nJPsiNon", "number of non prompt JPsi", 1000,0,2*entry_num)
#nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.1,0,1)
#prompFrac = ROOT.RooFormulaVar("prompFrac", "1 - @0", ROOT.RooArgList(nonPrompFrac))
#TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "194591 - (@0 + @1)", ROOT.RooArgList(nJPsi,nJPsiNon))
#TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@2 - (@0 + @1)", ROOT.RooArgList(nJPsi,nJPsiNon, nJPsiAll))
# model_m = ROOT.RooAddPdf("model_m", "mass_pdf + mass_n_pdf", ROOT.RooArgList(mass_pdf,mass_n_pdf), ROOT.RooArgList(nJPsi,nJPsiNon))
# model_t = ROOT.RooAddPdf("model_t", "tauz_pdf + tauz_n_pdf", ROOT.RooArgList(tauz_pdf,tauz_n_pdf), ROOT.RooArgList(nJPsi,nJPsiNon))

model_m = ROOT.RooAddPdf("model_m", "mass_n_pdf + mass_pdf", ROOT.RooArgList(mass_n_pdf,mass_pdf), ROOT.RooArgList(nonPrompFrac))
model_t = ROOT.RooAddPdf("model_t", "tauz_n_pdf + tauz_pdf", ROOT.RooArgList(tauz_n_pdf,tauz_pdf), ROOT.RooArgList(nonPrompFrac))

# we will try to add another fraction that will measure how much signal and background are present
massSigBgFrac = ROOT.RooRealVar("massSigBgFrac", "signal background fraction", 0.1,0,1)
tauSigBgFrac = ROOT.RooRealVar("tauSigBgFrac", "signal background fraction", 0.1,0,1)

model_m_all = ROOT.RooAddPdf("model_m_all", "model_m + bg_pdf", ROOT.RooArgList(model_m,model_bg_m), ROOT.RooArgList(nJPsi,nBkg))
model_t_all = ROOT.RooAddPdf("model_t_all", "tauz_n_pdf + tauz_pdf + bg_pdf", ROOT.RooArgList(tauz_n_pdf, tauz_pdf, tauz_bg_pdf), ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkg))



cat = ROOT.RooCategory("cat", "cat")
cat.defineType("massCat")
cat.defineType("tauzCat")

simfit = ROOT.RooSimultaneous("simfit", "", cat)
#simfit.addPdf(model_m,"massCat")
simfit.addPdf(model_m_all, "massCat")
simfit.addPdf(model_t_all,"tauzCat")

# data_m = mass_pdf.generate(ROOT.RooArgSet(mass), prompt_num)
# data_m_non = mass_n_pdf.generate(ROOT.RooArgSet(mass), non_prompt_num)
# data_bg_m = model_bg_m.generate(ROOT.RooArgSet(mass), m_bg_num)

# data_t = tauz_pdf.generate(ROOT.RooArgSet(tau), prompt_num)
# data_t_non = tauz_n_pdf.generate(ROOT.RooArgSet(tau), non_prompt_num)
# data_bg_t = tauz_bg_pdf.generate(ROOT.RooArgSet(tau), t_bg_num)


# data_m.append(data_m_non)
# data_m.append(data_bg_m)
# data_t.append(data_t_non)
# data_t.append(data_bg_t)



print(entry_num)

combData = ROOT.RooDataSet("combData", "combined data",
    {mass, tau}, 
    Index=cat, 
    Import={"massCat": data_m, "tauzCat": data_t},
)

fitResult = simfit.fitTo(combData, Extended=True, Save=True, PrintLevel=-1)
fitResult.Print()
# pr_res = "Prompt num: {0}/{1}".format(prompt_num, nJPsi)
# non_pr_res = "Non-Prompt num: {0}/{1}".format(non_prompt_num, nJPsiNon)

frac_res = "Prompt num: {0}/{1}".format(non_prompt_num/(prompt_num + non_prompt_num), nonPrompFrac)

print("-------------------------------------------------------------------")

with open("mc_valid.txt", "a") as file:
    file.write(f"{frac_res}")

frame1 = mass.frame(ROOT.RooFit.Title("Invariant Mass Fit Result"))
combData.plotOn(frame1, ROOT.RooFit.Cut("cat==cat::massCat"))
#data.plotOn(framep,RooFit.Cut("cat==cat::massCat"))
#data_m.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_all_pdf"), Slice=(cat, "massCat"), ProjWData=(cat,combData))
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_pdf"), Slice=(cat, "massCat"), Components="mass_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_n_pdf"), Slice=(cat, "massCat"), Components="mass_n_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
simfit.plotOn(frame1, ROOT.RooFit.Name("mass_bg_pdf"), Slice=(cat, "massCat"), Components="model_bg_m", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)


frame2 = tau.frame(ROOT.RooFit.Title("Pseudo Proper Decay Length Fit Result"))
combData.plotOn(frame2, ROOT.RooFit.Cut("cat==cat::tauzCat"))
#data_t.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_all_pdf"), Slice=(cat, "tauzCat"), ProjWData=(cat,combData))
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_pdf"), Slice=(cat, "tauzCat"), Components="tauz_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_n_pdf"), Slice=(cat, "tauzCat"), Components="tauz_n_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
simfit.plotOn(frame2, ROOT.RooFit.Name("tauz_bg_pdf"), Slice=(cat, "tauzCat"), Components="tauz_bg_pdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)




canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

legend1 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
legend1.AddEntry(frame1.findObject("mass_all_pdf"), "Invariant mass fit", "l")
legend1.AddEntry(frame1.findObject("mass_pdf"), "Prompt fraction", "l")
legend1.AddEntry(frame1.findObject("mass_n_pdf"), "Non prompt fraction", "l")
legend1.AddEntry(frame1.findObject("mass_bg_pdf"), "Background", "l")

legend2 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
legend2.AddEntry(frame2.findObject("tauz_all_pdf"), "PPDL fit", "l")
legend2.AddEntry(frame2.findObject("tauz_pdf"), "Prompt fraction", "l")
legend2.AddEntry(frame2.findObject("tauz_n_pdf"), "Non prompt fraction", "l")
legend2.AddEntry(frame2.findObject("tauz_bg_pdf"), "Background", "l")


canvas.Divide(2,1)
canvas.cd(1)
frame1.Draw()
legend1.Draw()

canvas.cd(2)
frame2.Draw()
legend2.Draw()

canvas.Update()
canvas.SaveAs("simul_fit_norm_new.png")