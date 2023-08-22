import ROOT

PATH_DATA = "root_files/"
PATH_IMGS = "imgs/"

hm_data_file = ROOT.TFile(PATH_DATA + "data_tune_45_4-6_bkg_extr.root")
hm_data = hm_data_file.Get("hm")
#hm_data.Scale(1. / hm_data.Integral())

mass = ROOT.RooRealVar("mass", "mass", 2, 5)

datahist_data_m = ROOT.RooDataHist("datahistmdatabg", "DataHist m data bg", ROOT.RooArgList(mass), hm_data)

n_sig = ROOT.RooRealVar("n_sig", "n_sig", 1e2, 1, 1e6)
n_bkg = ROOT.RooRealVar("n_bkg", "n_bkg", 1e2, 10, 1e7)

mean = ROOT.RooRealVar("mean", "Mean", 3.0, 2.7, 3.3)
sigma = ROOT.RooRealVar("sigma", "Sigma", 0.05, 0.03, 0.12)
alpha = ROOT.RooRealVar("alpha", "Alpha", -1.2, -5, 10)
n = ROOT.RooRealVar("n", "n", 1.99, -1, 10)
cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -10, 10) for i in range(4)]
cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

tau = ROOT.RooRealVar("tau", "tau", 1., -100, 100)
expo_pdf = ROOT.RooExponential("expo_pdf", "expo_pdf", mass, tau)
cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)


background_pdf = ROOT.RooAddPdf("expo_cheb_poly", "Cheby + Exponential", ROOT.RooArgList(cheb_poly, expo_pdf), ROOT.RooArgList(cb_frac))
#model_m = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(n_sig, n_bkg))
model_m = ROOT.RooAddPdf("model_pdf", "Crystal Ball + Background", ROOT.RooArgList(cb_pdf, background_pdf), ROOT.RooArgList(n_sig, n_bkg))

model_m.fitTo(datahist_data_m)



frame = mass.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_data_m.plotOn(frame)
model_m.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "mass_data_fit.png")