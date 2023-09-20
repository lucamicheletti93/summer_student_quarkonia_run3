import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/alice/"
PATH_DATA = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"
PATH_IMGS = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"
PATH_WORKSPACE = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/workspaces/"


ptMin = [4]
ptMax = [6]

for iPt in range(0, len(ptMin)):

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


    hMassDataHist= ROOT.RooDataHist("hMassDataHist", "hMassDataHist", ROOT.RooArgList(mass), hMassData)
    hTauzDataHist = ROOT.RooDataHist("hTauzDataHist", "hTauzDataHist", ROOT.RooArgList(tauz), hTauzData)

    
    
    mean = ROOT.RooRealVar("mean", "Mean", 3.09285e+00)
    sigma = ROOT.RooRealVar("sigma", "Sigma", 9.71202e-02)
    alpha = ROOT.RooRealVar("alpha", "Alpha", 8.44119e-01)
    n = ROOT.RooRealVar("n", "n", 2.99999e+01)
    cbMasspdf = ROOT.RooCBShape("cbMasspdf", "Crystal Ball PDF", mass, mean, sigma, alpha, n)

    chebCoeffsMass = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.01, -5, 5) for i in range(5)]
    

    coeffsMass = [-1.08591e+00, 2.06141e-01, -7.69411e-04, 4.86283e-02, -4.33958e-02]
    for i, coef_value in enumerate(coeffsMass):
        chebCoeffsMass[i].setVal(coef_value)
        chebCoeffsMass[i].setConstant(True)
    
    chebPolyMass = ROOT.RooChebychev("chebPoly", "Chebyshev Polynomial", mass, ROOT.RooArgList(*chebCoeffsMass))
    modelMassAll = ROOT.RooAddPdf("modelMassAll", "Crystal Ball + Chebyshev", ROOT.RooArgList(cbMasspdf, chebPolyMass ), ROOT.RooArgList(2.61285e+04, 1.02310e+05))

    #modelMassAll.fitTo(hMassDataHist)


    #-------------------------------PROMPT-----------------------------------------------------------------------
    
    
#       EXT PARAMETER                                INTERNAL      INTERNAL  
#   NO.   NAME      VALUE            ERROR       STEP SIZE       VALUE   
#    1  meanTauzPromptBw   5.29773e-05   3.48880e-05   5.01337e-06   5.29773e-04
#    2  meanTauzPromptGauss  -2.18095e-06   1.48062e-05   2.27925e-06  -2.18095e-05
#    3  modelFractionTauzPrompt   5.51011e-01   9.16203e-02   6.08587e-04   1.02200e-01
#    4  sigmaTauzPromptGauss   3.10378e-04   2.05001e-05   3.17186e-06  -1.52096e+00
#    5  widthTauzPrompt   1.42776e-03   3.01604e-04   8.43899e-06  -1.46387e+00
    
    
    meanBwtauzPrompt = ROOT.RooRealVar("meanBwtauzPrompt", "meanBwtauzPrompt", 5.29773e-05)
    widthBwTauzPrompt = ROOT.RooRealVar("widthBwTauzPrompt", "widthBwTauzPrompt",  1.42776e-03)
    pdfBwTauzPrompt = ROOT.RooBreitWigner("pdfBwTauzPrompt", "pdfBwTauzPrompt", tauz, meanBwtauzPrompt, widthBwTauzPrompt)
    meanGaussTauzPrompt = ROOT.RooRealVar("meanGaussTauzPrompt", "meanGaussTauzPrompt", -2.18095e-06)
    sigmaGaussTauzPrompt = ROOT.RooRealVar("sigmaGaussTauzPrompt", "sigmaGaussTauzPrompt", 3.10378e-04)
    pdfGaussTauzPrompt = ROOT.RooGaussian("pdfGaussTauzPrompt", "pdfGaussTauzPrompt", tauz, meanGaussTauzPrompt, sigmaGaussTauzPrompt)
    modelFracTauzPrompt = ROOT.RooRealVar("modelFracTauzPrompt", "modelFracTauzPrompt", 5.51011e-01)
    modelTauzPrompt = ROOT.RooAddPdf("modelTauzPrompt", "Breit Wiegner + Gauss", ROOT.RooArgList(pdfBwTauzPrompt, pdfGaussTauzPrompt), ROOT.RooArgList(modelFracTauzPrompt))


    #-------------------------------NONPROMPT------------------------------------------------------------------
    
    
#       NO.   NAME      VALUE            ERROR       STEP SIZE       VALUE   
#    1  cheb_coeff_0   5.84195e-02   2.11301e-01   5.16099e-05   5.84198e-03
#    2  locationTauzNonPrompt   6.95326e-04   1.85280e-05   2.79926e-06   6.95332e-03
#    3  modelFractionTauzNonPrompt   9.19871e-01   1.04215e-02   4.59575e-04   9.96808e-01
#    4  scaleTauzNonPrompt   4.74547e-04   1.23925e-05   4.82910e-06  -1.43293e+00
    
    
    locationLandauTauzNonPrompt = ROOT.RooRealVar("locationLandauTauzNonPrompt", "locationLandauTauzNonPrompt",  6.95326e-04 )
    scaleLandauTauzNonPrompt = ROOT.RooRealVar("scaleLandauTauzNonPrompt", "scaleLandauTauzNonPrompt", 4.74547e-04)
    pdfLandauTauzNonPrompt = ROOT.RooLandau("pdfLandauTauzNonPrompt", "pdfLandauTauzNonPrompt", tauz, locationLandauTauzNonPrompt, scaleLandauTauzNonPrompt)
    chebCoeffsTauzNonPrompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.46, 0.46) for i in range(1)]

    coeffsTauzNonPrompt = [5.84195e-02]
    for i, coef_value in enumerate(coeffsTauzNonPrompt):
        chebCoeffsTauzNonPrompt[i].setVal(coef_value)
        chebCoeffsTauzNonPrompt[i].setConstant(True)

    chebPolyTauzNonPrompt = ROOT.RooChebychev("chebPolyTauzNonPrompt", "chebPolyTauzNonPrompt", tauz, ROOT.RooArgList(*chebCoeffsTauzNonPrompt))
    modelFracTauzNonPrompt = ROOT.RooRealVar("modelFracTauzNonPrompt", "modelFracTauzNonPrompt", 9.19871e-01)
    modelTauzNonPrompt = ROOT.RooAddPdf("modelTauzNonPrompt", "modelTauzNonPrompt", ROOT.RooArgList(pdfLandauTauzNonPrompt, chebPolyTauzNonPrompt), ROOT.RooArgList(modelFracTauzNonPrompt))
    #---------------------------------BKG---------------------------------------------------------------------

    meanBwtauzBkg = ROOT.RooRealVar("meanBwtauzBkg", "meanBwtauzBkg", 9.31848e-05 )
    widthBwTauzBkg = ROOT.RooRealVar("widthBwTauzBkg", "widthBwTauzBkg", 1.27135e-03)
    pdfBwTauzBkg= ROOT.RooBreitWigner("pdfBwTauzBkg", "pdfBwTauzBkg", tauz, meanBwtauzBkg, widthBwTauzBkg)

    meanCbTauzBkg = ROOT.RooRealVar("meanCbTauzBkg", "meanCbTauzBkg",   5.86639e-04 )
    sigmaCbTauzBkg = ROOT.RooRealVar("sigmaCbTauzBkg", "sigmaCbTauzBkg", 8.75250e-03)
    alphaCbTauzBkg = ROOT.RooRealVar("alphaCbTauzBkg", "alphaCbTauzBkg", -3.72729e+00 )
    nCbTauzBkg = ROOT.RooRealVar("nCbTauzBkg", "nCbTauzBkg", 6.40637e-01)
    pdfCbTauzBkg = ROOT.RooCBShape("pdfCbTauzBkg", "pdfCbTauzBkg", tauz, meanCbTauzBkg, sigmaCbTauzBkg, alphaCbTauzBkg, nCbTauzBkg)

    modelFracTauzBkg = ROOT.RooRealVar("modelFracTauzBkg", "modelFracTauzBkg", 1.56427e-01)
    modelTauzBkg = ROOT.RooAddPdf("modelTauzBkg", "modelTauzBkg", ROOT.RooArgList(pdfBwTauzBkg, pdfCbTauzBkg), ROOT.RooArgList(modelFracTauzBkg))


    massData = ROOT.RooDataSet("massData", "Data Set m", ROOT.RooArgSet(mass),  ROOT.RooFit.Import(hMassDataHist))
    tauzData = ROOT.RooDataSet("tauzData", "Data Set t", ROOT.RooArgSet(tauz),  ROOT.RooFit.Import(hTauzDataHist))


    nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 2.61285e+04)
    nBkgVar = ROOT.RooRealVar("nBkg", "number of background", 1.02310e+05)  
    nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.5, 0 ,1)

    TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
    TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))


    # fit with the histogram pdfs
    #------------------------------------------------------------
    modelTauzAll = ROOT.RooAddPdf("modelTauzAll", " tauzNonPromptPdf  + tauzPromptPdf + tauzBkgPdf", 
        ROOT.RooArgList(modelTauzNonPrompt, modelTauzPrompt, modelTauzBkg), 
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
    simfit.plotOn(frame2, ROOT.RooFit.Name("modelTauzPrompt"), Slice=(cat, "tauzCat"), Components="modelTauzPrompt", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
    simfit.plotOn(frame2, ROOT.RooFit.Name("modelTauzNonPrompt"), Slice=(cat, "tauzCat"), Components="modelTauzNonPrompt", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)
    simfit.plotOn(frame2, ROOT.RooFit.Name("modelTauzBkg"), Slice=(cat, "tauzCat"), Components="modelTauzBkg", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kGreen+2)


    canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

    legend1 = ROOT.TLegend(0.53, 0.65, 0.83, 0.85)
    legend1.AddEntry(frame1.findObject("massAllPdf"), "Invariant mass fit", "l")

    legend2 = ROOT.TLegend(0.55, 0.55, 0.80, 0.75)
    legend2.AddEntry(frame2.findObject("tauzAllPdf"), "OS Tauz fit", "l")
    legend2.AddEntry(frame2.findObject("modelTauzPrompt"), "Prompt fraction", "l")
    legend2.AddEntry(frame2.findObject("modelTauzNonPrompt"), "Non prompt fraction", "l")
    legend2.AddEntry(frame2.findObject("modelTauzBkg"), "Background", "l")


    canvas.Divide(2,1)
    canvas.cd(1)
    frame1.Draw()
    legend1.Draw()

    canvas.cd(2).SetLogy()
    frame2.Draw()
    legend2.Draw()

    canvas.Update()
    canvas.SaveAs(PATH_IMGS + f"simul_fit_pdf_smeared_{ptMin[iPt]}_{ptMax[iPt]}.png")
