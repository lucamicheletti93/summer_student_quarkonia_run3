import ROOT

PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"

hm_data_file = ROOT.TFile(PATH_DATA + "data_tune_45_4-6_bkg_extr.root")
hm_data = hm_data_file.Get("hm")

mass = ROOT.RooRealVar("mass", "mass", 2, 5)

datahist_data_m = ROOT.RooDataHist("datahistmdatabg", "DataHist m data bg", ROOT.RooArgList(mass), hm_data)

mean = ROOT.RooRealVar("mean", "Mean", 3.0, 0, 10)
sigma = ROOT.RooRealVar("sigma", "Sigma", 0.07, 0, 10)
alpha = ROOT.RooRealVar("alpha", "Alpha", -1.0, -5, 10)
n = ROOT.RooRealVar("n", "n", 2.0, 0, 100)
cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -2, 2) for i in range(6)]
cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

#cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
nJPsi =  ROOT.RooRealVar("nJpsi", "nJpsi", 100000, 0, 1000000)
bkg =  ROOT.RooRealVar("background", "background", 1000000, 0, 10000000)
model_m = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(nJPsi, bkg))

model_m.fitTo(datahist_data_m)



frame = mass.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_data_m.plotOn(frame)
model_m.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "mass_data_fit.png")