import ROOT

PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"

ht_data_cut_file = ROOT.TFile(PATH_DATA + "data_tune_45_4-6_bkg_extr.root")
ht_data = ht_data_cut_file.Get("ht_bkg")
#ht_data.Scale(1. / ht_data.Integral())

tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.01, 0.01)

datahist_data_t = ROOT.RooDataHist("datahisttdatabg", "DataHist t data bg", ROOT.RooArgList(tauz), ht_data)

mean_bw = ROOT.RooRealVar("mean_bw", "Mean bw", 0.0)
width_bw = ROOT.RooRealVar("width_bw", "Width bw", 0.001, 0.0, 10)
bw_pdf = ROOT.RooBreitWigner("bw", "Breit-Wigner Distribution", tauz, mean_bw, width_bw)


mean_cb = ROOT.RooRealVar("mean_cb", "Mean_cb", 0, 0, 10)
sigma_cb = ROOT.RooRealVar("sigma_cb", "Sigma", 0.07, 0, 0.1)
alpha_cb = ROOT.RooRealVar("alpha_cb", "Alpha", -1.0, -5, 10)
n_cb = ROOT.RooRealVar("n_cb", "n", 0.0, 0, 100)
cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", tauz, mean_cb, sigma_cb, alpha_cb, n_cb)

# mean_gauss = ROOT.RooRealVar("mean_gauss", "Mean gauss", 0.0)
# sigma_gauss = ROOT.RooRealVar("sigma_gauss", "Sigma gauss", 0.01, 0.0, 100)
# gauss_pdf = ROOT.RooGaussian("gaussian", "Gaussian Distribution", tauz, mean_gauss, sigma_gauss)

# Create variables for the mass and parameters of the Crystal Ball function
# mean = ROOT.RooRealVar("mean", "Mean", 0, 0, 1)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.04, 0.0001, 1.0)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.0, 0.5, 10.0)
# n = ROOT.RooRealVar("n", "n", 1.0, 0.1, 10.0)

# # Create the Crystal Ball PDF
# cb_pdf = ROOT.RooCBShape("crystal_ball", "Crystal Ball PDF", tauz, mean, sigma, alpha, n)


# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -0.2, 0.2) for i in range(4)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", tauz, ROOT.RooArgList(*cheb_coeffs))

model_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
model_t = ROOT.RooAddPdf("model_background_pdf", "Breit Wiegner + Chebyshev", ROOT.RooArgList(bw_pdf, cb_pdf), ROOT.RooArgList(model_frac))

model_t.fitTo(datahist_data_t)



frame = tauz.frame(ROOT.RooFit.Title("Pseudo proper decay length background")) 
datahist_data_t.plotOn(frame)
model_t.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "tauz_data_cut_bkg_fit.png")

# tauz_background_fit_workspace = ROOT.RooWorkspace("tauz_background_fit_workspace")
# tauz_background_fit_workspace.Import(model_t)

# workspace_file = ROOT.TFile(PATH_WORKSPACE + "tauz_background_gauss_cheb_fit_workspace.root", "RECREATE")
# tauz_background_fit_workspace.Write()
# workspace_file.Close()