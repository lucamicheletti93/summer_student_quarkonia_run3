import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/alice/"
PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"


ptMin = [0]
ptMax = [2]

for iPt in range(0, len(ptMin)):

    templateFile = ROOT.TFile(PATH_DATA + "template.root")
    hMassPromptDistr = templateFile.Get(f"hMassPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hMassPromptDistr.Scale(1. / hMassPromptDistr.Integral())
    hMassNonPromptDistr = templateFile.Get(f"hMassNonPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hMassNonPromptDistr.Scale(1. / hMassNonPromptDistr.Integral())
    hTauzPromptDistr = templateFile.Get(f"hTauzPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzPromptDistr.Scale(1. / hTauzPromptDistr.Integral())
    hTauzNonPromptDistr = templateFile.Get(f"hTauzNonPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzNonPromptDistr.Scale(1. / hTauzNonPromptDistr.Integral())

    dataFile = ROOT.TFile(PATH_DATA + "data.root")

    hTauzBkgDistr =  dataFile.Get(f"hTauzBkg_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzBkgDistr.Scale(1. / hTauzBkgDistr.Integral())

    hMassData = dataFile.Get(f"hMass_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzData = dataFile.Get(f"hTauz_{ptMin[iPt]}_{ptMax[iPt]}")


    mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
    tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

    mass.setRange("full", 2, 5)
    mass.setRange("left", 2, 2.9)
    mass.setRange("right", 3.2, 5)

    hMassPromptHist = ROOT.RooDataHist("hMassPromptHist", "hMassPromptHist", ROOT.RooArgList(mass), hMassPromptDistr)
    hMassNonPromptHist  = ROOT.RooDataHist("hMassNonPromptHist", "hMassNonPromptHist", ROOT.RooArgList(mass), hMassNonPromptDistr)
    hTauzPromptHist = ROOT.RooDataHist("hTauzPromptHist", "hTauzPromptHist", ROOT.RooArgList(tauz), hTauzPromptDistr)
    hTauzNonPromptHist  = ROOT.RooDataHist("hTauzNonPromptHist", "hTauzNonPromptHist", ROOT.RooArgList(tauz), hTauzNonPromptDistr)
    hTauzBkgHist = ROOT.RooDataHist("hTauzDataHist", "hTauzDataHist", ROOT.RooArgList(tauz), hTauzBkgDistr)

    massPromptPdf = ROOT.RooHistPdf("massPromptPdf", "massPromptPdf", ROOT.RooArgList(mass), hMassPromptHist)
    massNonPromptPdf = ROOT.RooHistPdf("massNonPromptPdf", "massNonPromptPdf", ROOT.RooArgList(mass), hMassNonPromptHist)
    tauzPromptPdf = ROOT.RooHistPdf("tauzPromptPdf", "tauzPromptPdf", ROOT.RooArgList(tauz), hTauzPromptHist)
    tauzNonPromptPdf = ROOT.RooHistPdf("tauzNonPromptPdf", "tauzNonPromptPdf", ROOT.RooArgList(tauz), hTauzNonPromptHist)
    tauzBkgPdf = ROOT.RooHistPdf("tauzBkgPdf", "tauzBkgPdf", ROOT.RooArgList(tauz), hTauzBkgHist)

    hMassDataHist= ROOT.RooDataHist("hMassDataHist", "hMassDataHist", ROOT.RooArgList(mass), hMassData)
    hTauzDataHist = ROOT.RooDataHist("hTauzDataHist", "hTauzDataHist", ROOT.RooArgList(tauz), hTauzData)


    #mass crystal ball, chebyshev polynomials pt = 4-6
    #----------------------------------------------------------------------------------------------------
    mean = ROOT.RooRealVar("mean", "Mean", 3.1, 2.9, 3.3)
    sigma = ROOT.RooRealVar("sigma", "Sigma", 0.08, 0, 0.15)
    alpha = ROOT.RooRealVar("alpha", "Alpha", 0.1, 0, 1)
    n = ROOT.RooRealVar("n", "n", 1, 0, 50)
    cb_pdf = ROOT.RooCBShape("cb_pdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

    cheb_coeffs = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -10, 10) for i in range(6)]
    cheb_poly = ROOT.RooChebychev("cheb_poly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*cheb_coeffs))

    cb_frac = ROOT.RooRealVar("cb_frac", "CB Fraction", 0.5, 0, 1)
    modelMassAll = ROOT.RooAddPdf("modelMassAll", "Crystal Ball + Chebyshev", ROOT.RooArgList(cb_pdf, cheb_poly), ROOT.RooArgList(cb_frac))

    modelMassAll.fitTo(hMassDataHist)

    massData = ROOT.RooDataSet("massData", "Data Set m", ROOT.RooArgSet(mass),  ROOT.RooFit.Import(hMassDataHist))
    tauzData = ROOT.RooDataSet("tauzData", "Data Set t", ROOT.RooArgSet(tauz),  ROOT.RooFit.Import(hTauzDataHist))


    event_num = 100000
    signalToBackground = 0.1
    fb = 0.1
    nSig = event_num*signalToBackground
    nBkg = event_num*(1-signalToBackground)

    promptNum = nSig*(1-fb)
    nonPromptNum = nSig*fb 
    entryNum = promptNum + nonPromptNum


    nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 10000,0,1e6)
    nBkgVar = ROOT.RooRealVar("nBkg", "number of background", 100000,0,2e6)  
    nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.17, 0 ,1)

    TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
    TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))



    # fit with the histogram pdfs
    #------------------------------------------------------------
    modelTauzAll = ROOT.RooAddPdf("modelTauzAll", " tauzNonPromptPdf  + tauzPromptPdf + tauzBkgPdf", 
        ROOT.RooArgList(tauzNonPromptPdf, tauzPromptPdf, tauzBkgPdf), 
        ROOT.RooArgList(TotalnJPsiNon, TotalnJPsi, nBkgVar))
    #------------------------------------------------------------


    cat = ROOT.RooCategory("cat", "cat")
    cat.defineType("massCat")
    cat.defineType("tauzCat")

    simfit = ROOT.RooSimultaneous("simfit", "", cat)
    simfit.addPdf(modelMassAll, "massCat")
    simfit.addPdf(modelTauzAll,"tauzCat")


    combData = ROOT.RooDataSet("combData", "combined data",
        {mass, tauz}, 
        Index=cat, 
        Import={"massCat": massData, "tauzCat": tauzData},
    )

    fitResult = simfit.fitTo(combData, Extended=True, Save=True, PrintLevel=-1)
    fitResult.Print()


    frame1 = mass.frame(ROOT.RooFit.Title("Invariant Mass Fit Result"))
    combData.plotOn(frame1, ROOT.RooFit.Cut("cat==cat::massCat"))
    simfit.plotOn(frame1, ROOT.RooFit.Name("massAllPdf"), Slice=(cat, "massCat"), ProjWData=(cat,combData))


    frame2 = tauz.frame(ROOT.RooFit.Title("Pseudo Proper Decay Length Fit Result"))
    combData.plotOn(frame2, ROOT.RooFit.Cut("cat==cat::tauzCat"))
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzAllPdf"), Slice=(cat, "tauzCat"), ProjWData=(cat,combData))
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzPromptPdf"), Slice=(cat, "tauzCat"), Components="tauzPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzNonPromptPdf"), Slice=(cat, "tauzCat"), Components="tauzNonPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzBkgPdf"), Slice=(cat, "tauzCat"), Components="tauzBkgPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)


    canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

    legend1 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
    legend1.AddEntry(frame1.findObject("massAllPdf"), "Invariant mass fit", "l")

    legend2 = ROOT.TLegend(0.55, 0.55, 0.85, 0.75)
    legend2.AddEntry(frame2.findObject("tauzAllPdf"), "PPDL fit", "l")
    legend2.AddEntry(frame2.findObject("tauzPromptPdf"), "Prompt fraction", "l")
    legend2.AddEntry(frame2.findObject("tauzNonPromptPdf"), "Non prompt fraction", "l")
    legend2.AddEntry(frame2.findObject("tauzBkgPdf"), "Background", "l")


    canvas.Divide(2,1)
    canvas.cd(1)
    frame1.Draw()
    legend1.Draw()

    canvas.cd(2).SetLogy()
    frame2.Draw()
    legend2.Draw()

    canvas.Update()
    canvas.SaveAs(PATH_IMGS + f"simul_fit_data_{ptMin[iPt]}_{ptMax[iPt]}.png")
