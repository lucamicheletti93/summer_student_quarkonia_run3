import ROOT

hm_data_file_bg = ROOT.TFile("hm_data_bg_tune_45_4-6.root")
hm_data_bg = hm_data_file_bg.Get("hm")
hm_data_bg.Scale(1. / hm_data_bg.Integral())


hm_data_file= ROOT.TFile("hm_tune_45_4-6.root")
hm_data = hm_data_file.Get("hm")
hm_data.Scale(1. / hm_data.Integral())


hmnon_data_file = ROOT.TFile("hmnon_tune_45_4-6.root")
hmnon_data = hmnon_data_file.Get("hmnon")
hmnon_data.Scale(1. / hmnon_data.Integral())


mass = ROOT.RooRealVar("Dimuon mass", "Dimuon invariant mass background", 2, 5)

lambda_param = ROOT.RooRealVar("lambda_param", "Exponential decay constant", 0, -5, 0)
exp_model = ROOT.RooExponential("exp_model", "Exponential PDF", mass, lambda_param)

mass.setRange("full", 2, 5)
mass.setRange("left", 2, 2.9)
mass.setRange("right", 3.2, 5)


datahist_m_databg = ROOT.RooDataHist("datahistmdatabg", "DataHist m data bg", ROOT.RooArgList(mass), hm_data_bg)
exp_model.fitTo(datahist_m_databg, Range="left,right", PrintLevel=-1)
roofit_dataset = exp_model.generate(ROOT.RooArgSet(mass), 10000)
blindedData = roofit_dataset.reduce(CutRange="left,right")
#lambda_param.setVal(-2.0)
exp_model.fitTo(blindedData, Range="left,right")


datahist_m = ROOT.RooDataHist("datahist_m", "DataHist m", ROOT.RooArgList(mass), hm_data)
datahist_non_m = ROOT.RooDataHist("datahist_non_m", "DataHist non m", ROOT.RooArgList(mass), hmnon_data)
mass_pdf = ROOT.RooHistPdf("mass_pdf", "mass PDF", ROOT.RooArgList(mass), datahist_m)
mass_non_pdf = ROOT.RooHistPdf("mass_non_pdf", "mass non PDF", ROOT.RooArgList(mass), datahist_non_m)




frame = mass.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_m_databg.plotOn(frame)
exp_model.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs("mass_bg_fit.png")