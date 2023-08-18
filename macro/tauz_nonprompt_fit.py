import ROOT
from ROOT import RooFit

PATH_DATA = "root_files/"
PATH_IMGS = "imgs/"
#PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"


ht_data_cut_file = ROOT.TFile(PATH_DATA + "template_tune_45_6-10.root")
ht_data = ht_data_cut_file.Get("htnon")
ht_data.Scale(1. / ht_data.Integral())

tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.003, 0.003)

datahist_data_t = ROOT.RooDataHist("datahisttdatabg", "DataHist t data bg", ROOT.RooArgList(tauz), ht_data)

# mean = ROOT.RooRealVar("mean", "Mean", 0.0, -1, 1)
# width = ROOT.RooRealVar("width", "Width", 0.001, -0.01, 10)
# bw_pdf = ROOT.RooBreitWigner("bw", "Breit-Wigner Distribution", tauz, mean, width)

# mean = ROOT.RooRealVar("mean", "Mean", 0.0, -0.1, 0.1)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.01, 0.0, 2)
# gauss_pdf = ROOT.RooGaussian("gaussian", "Gaussian Distribution", tauz, mean, sigma)

# Create variables for the mass and parameters of the Crystal Ball function
# mean = ROOT.RooRealVar("mean", "Mean", 0, 0, 1)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.04, 0.0001, 1.0)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.0, 0.5, 10.0)
# n = ROOT.RooRealVar("n", "n", 1.0, 0.1, 10.0)

# # Create the Crystal Ball PDF
# cb_pdf = ROOT.RooCBShape("crystal_ball", "Crystal Ball PDF", tauz, mean, sigma, alpha, n)

location = ROOT.RooRealVar("location", "Location", 0.0, -0.1, 0.1)
scale = ROOT.RooRealVar("scale", "Scale", 0.01, 0.00001, 0.1)

landau_pdf = ROOT.RooLandau("landau", "Landau PDF", tauz, location, scale)



cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.26, 0.26) for i in range(2)]
cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", tauz, ROOT.RooArgList(*cheb_coeffs))

# poly_coeffs = [ROOT.RooRealVar(f"poly_coeff_{i}", f"Coeff_{i}", 0.01, -0.05, 0.05) for i in range(5)]
# poly_sum = ROOT.RooArgList()
# for i in range(5):
#     term = ROOT.RooRealVar(f"poly_term_{i}", f"PolyTerm_{i}", 1.0)
#     term.setVal(poly_coeffs[i].getVal())
#     poly_sum.add(ROOT.RooPolynomial(f"poly_term_{i}", f"PolyTerm_{i}", tauz, ROOT.RooArgList(term)))
# poly = ROOT.RooAddPdf("poly", "Polynomials", poly_sum)

model_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
model_t = ROOT.RooAddPdf("model_nonprompt_pdf", "Breit Wiegner + Chebyshev", ROOT.RooArgList(landau_pdf, cheb_poly), ROOT.RooArgList(model_frac))

model_t.fitTo(datahist_data_t)




frame = tauz.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_data_t.plotOn(frame)
model_t.plotOn(frame)
#cheb_poly.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "tauz_template_nonprompt_fit.png")

tauz_nonprompt_fit_workspace = ROOT.RooWorkspace("tauz_nonprompt_fit_workspace")
tauz_nonprompt_fit_workspace.Import(model_t)

#workspace_file = ROOT.TFile(PATH_WORKSPACE + "tauz_nonprompt_landau_cheb_fit_workspace.root", "RECREATE")
#tauz_nonprompt_fit_workspace.Write()
#workspace_file.Close()
