import ROOT

PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
#PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"

ht_data_cut_file = ROOT.TFile(PATH_DATA + "template_tune_45_4-6.root")
ht_data = ht_data_cut_file.Get("ht")
#ht_data.Scale(1. / ht_data.Integral())

tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

datahist_data_t = ROOT.RooDataHist("datahisttdatabg", "DataHist t data bg", ROOT.RooArgList(tauz), ht_data)

mean = ROOT.RooRealVar("mean", "Mean", 0.0, -1, 1)
width = ROOT.RooRealVar("width", "Width", 0.001, 0.0, 10)
bw_pdf = ROOT.RooBreitWigner("bw", "Breit-Wigner Distribution", tauz, mean, width)

mean_gauss = ROOT.RooRealVar("mean_gauss", "Mean", 0.0, -0.1, 0.1)
sigma_gauss = ROOT.RooRealVar("sigma_gauss", "Sigma", 0.001, 0.0, 10)
gauss_pdf = ROOT.RooGaussian("gaussian", "Gaussian Distribution", tauz, mean_gauss, sigma_gauss)

#Create variables for the mass and parameters of the Crystal Ball function
# mean = ROOT.RooRealVar("mean", "Mean", 0, 0, 1)
# sigma = ROOT.RooRealVar("sigma", "Sigma", 0.04, 0.0001, 1.0)
# alpha = ROOT.RooRealVar("alpha", "Alpha", 1.0, -10, 10.0)
# n = ROOT.RooRealVar("n", "n", 1.0, 0.1, 10.0)
# # # Create the Crystal Ball PDF
# cb_pdf = ROOT.RooCBShape("crystal_ball", "Crystal Ball PDF", tauz, mean, sigma, alpha, n)

# cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -0.31, 0.31) for i in range(4)]
# cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", tauz, ROOT.RooArgList(*cheb_coeffs))

model_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
model_t = ROOT.RooAddPdf("model_prompt_pdf", "Breit Wiegner + Chebyshev", ROOT.RooArgList(bw_pdf, gauss_pdf), ROOT.RooArgList(model_frac))

model_t.fitTo(datahist_data_t)


frame = tauz.frame(ROOT.RooFit.Title("Invariant mass background")) 
datahist_data_t.plotOn(frame)
model_t.plotOn(frame)

canvas = ROOT.TCanvas("canvas", "Exponential Fit Canvas", 800, 600)
canvas.SetLogy()
frame.Draw()
canvas.Draw()

canvas.SaveAs(PATH_IMGS + "tauz_template_prompt_fit.png")

# tauz_prompt_fit_workspace = ROOT.RooWorkspace("tauz_prompt_fit_workspace")
# tauz_prompt_fit_workspace.Import(model_t)

#workspace_file = ROOT.TFile(PATH_WORKSPACE + "tauz_prompt_bw_cheb_fit_workspace.root", "RECREATE")
#tauz_prompt_fit_workspace.Write()
#workspace_file.Close()




