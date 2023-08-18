import ROOT

PATH_DATA = "root_files/"
PATH_IMGS = "imgs/"
#PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"

ht_data_cut_file = ROOT.TFile(PATH_DATA + "data_tune_45_6-10_bkg_extr.root")
ht_data = ht_data_cut_file.Get("ht_bkg")
#ht_data = ht_data_cut_file.Get("ht")
#ht_data.Scale(1. / ht_data.Integral())

tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.006, 0.006)

datahist_data_t = ROOT.RooDataHist("datahisttdatabg", "DataHist t data bg", ROOT.RooArgList(tauz), ht_data)

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



#cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -0.2, 0.2) for i in range(3)]
#cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", tauz, ROOT.RooArgList(*cheb_coeffs))


mean_bw_tauz_bkg = ROOT.RooRealVar("mean_bw_tauz_bkg", "Mean bw", 0, 0, 10)
width_bw_tauz_bkg = ROOT.RooRealVar("width_bw_tauz_bkg", "Width bw", 1.41068e-03, 0, 1)
bw_pdf_tauz_bkg = ROOT.RooBreitWigner("bw_tauz_bkg", "Breit-Wigner Distribution", tauz, mean_bw_tauz_bkg, width_bw_tauz_bkg)


mean_cb_tauz_bkg = ROOT.RooRealVar("mean_cb_tauz_bkg", "Mean_cb",  7.32785e-04, 0, 10)
sigma_cb_tauz_bkg = ROOT.RooRealVar("sigma_cb_tauz_bkg", "Sigma",9.92521e-03, 0, 10)
alpha_cb_tauz_bkg = ROOT.RooRealVar("alpha_cb_tauz_bkg", "Alpha", -3.75169e+00, -10, 10)
n_cb_tauz_bkg = ROOT.RooRealVar("n_cb_tauz_bkg", "n", 9.53674e-05, 0, 100)
cb_pdf_tauz_bkg = ROOT.RooCBShape("cb_pdf_tauz_bkg", "Crystal Ball PDF", tauz, mean_cb_tauz_bkg, sigma_cb_tauz_bkg, alpha_cb_tauz_bkg, n_cb_tauz_bkg)


model_frac_tauz_bkg = ROOT.RooRealVar("model_frac_tauz_bkg", "model_frac_tauz_bkg", 2.49807e-01 , 0, 1)
model_tauz_bkg = ROOT.RooAddPdf("model_tauz_bkg", "model_tauz_bkg", ROOT.RooArgList(bw_pdf_tauz_bkg, cb_pdf_tauz_bkg), ROOT.RooArgList(model_frac_tauz_bkg))


model_tauz_bkg.fitTo(datahist_data_t)




frame = tauz.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_data_t.plotOn(frame)
model_tauz_bkg.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "tauz_data_bkg_fit.png")

tauz_background_fit_workspace = ROOT.RooWorkspace("tauz_background_fit_workspace")
tauz_background_fit_workspace.Import(model_tauz_bkg)

print(
    mean_bw_tauz_bkg.getVal(),
    width_bw_tauz_bkg.getVal(),
    mean_cb_tauz_bkg.getVal(),
    sigma_cb_tauz_bkg.getVal(),
    alpha_cb_tauz_bkg.getVal(),
    n_cb_tauz_bkg.getVal(),
)

#workspace_file = ROOT.TFile(PATH_WORKSPACE + "tauz_background_bw_cheb_fit_workspace.root", "RECREATE")
#tauz_background_fit_workspace.Write()
#workspace_file.Close()