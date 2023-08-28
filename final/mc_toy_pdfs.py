import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/imgs/"


ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]


mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

for iPt in range(0, len(ptMin)):

    #---------------------------- MASS FITTING --------------------------------------------------------------
    #------------------------------- MASS PROMPT FIT -------------------------------------------------------------
    mean_bw_mass_prompt = ROOT.RooRealVar("mean_bw_mass_prompt", "Mean",  3.10451e+00)
    width_bw_mass_prompt = ROOT.RooRealVar("width_mass_prompt", "Width", 1.31552e-01)
    massPromptPdf = ROOT.RooBreitWigner("massPromptPdf", "Breit-Wigner Distribution", mass, mean_bw_mass_prompt, width_bw_mass_prompt)


    #------------------------------- MASS NON PROMPT FIT ---------------------------------------------------------
    mean_bw_mass_nonprompt = ROOT.RooRealVar("mean_bw_mass_nonprompt", "Mean",   3.10213e+00)
    width_bw_mass_nonprompt = ROOT.RooRealVar("width_mass_nonprompt", "Width",  1.36300e-01)
    massNonPromptPdf = ROOT.RooBreitWigner("massNonPromptPdf", "Breit-Wigner Distribution", mass, mean_bw_mass_nonprompt, width_bw_mass_nonprompt)

    #---------------------------- TAUZ FITTING --------------------------------------------------------------
    #------------------------------- TAUZ PROMPT FIT -------------------------------------------------------------
    mean_bw_tauz_prompt = ROOT.RooRealVar("mean_bw_tauz_prompt", "mean_bw_tauz_prompt", -1.29422e-04)
    width_bw_tauz_prompt = ROOT.RooRealVar("width_bw_tauz_prompt", "width_bw_tauz_prompt",  7.13980e-03)
    pdf_bw_tauz_prompt = ROOT.RooBreitWigner("pdf_bw_tauz_prompt", "pdf_bw_tauz_prompt", tauz, mean_bw_tauz_prompt, width_bw_tauz_prompt)
    mean_gauss_tauz_prompt = ROOT.RooRealVar("mean_gauss_tauz_prompt", "mean_gauss_tauz_prompt", 4.81673e-06)
    sigma_gauss_tauz_prompt = ROOT.RooRealVar("sigma_gauss_tauz_prompt", "sigma_gauss_tauz_prompt", 1.43266e-04)
    pdf_gauss_tauz_prompt = ROOT.RooGaussian("pdf_gauss_tauz_prompt", "pdf_gauss_tauz_prompt", tauz, mean_gauss_tauz_prompt, sigma_gauss_tauz_prompt)
    model_frac_tauz_prompt = ROOT.RooRealVar("model_frac_tauz_prompt", "model_frac_tauz_prompt", 2.42878e-01 )
    tauzPromptPdf = ROOT.RooAddPdf("tauzPromptPdf", "Breit Wiegner + Gauss", ROOT.RooArgList(pdf_bw_tauz_prompt, pdf_gauss_tauz_prompt), ROOT.RooArgList(model_frac_tauz_prompt))

    #------------------------------- TAUZ NON PROMPT FIT ---------------------------------------------------------
    location_landau_tauz_nonprompt = ROOT.RooRealVar("location_landau_tauz_nonprompt", "location_landau_tauz_nonprompt",  4.62731e-04 )
    scale_landau_tauz_nonprompt = ROOT.RooRealVar("scale_landau_tauz_nonprompt", "scale_landau_tauz_nonprompt", 3.62567e-04)
    pdf_landau_tauz_nonprompt = ROOT.RooLandau("pdf_landau_tauz_nonprompt", "pdf_landau_tauz_nonprompt", tauz, location_landau_tauz_nonprompt, scale_landau_tauz_nonprompt)
    cheb_coeffs_landau_tauz_nonprompt = [ROOT.RooRealVar(f"cheb_coeff_{i}", f"Coeff_{i}", 0.05, -0.46, 0.46) for i in range(0)]

    cheb_poly_landau_tauz_nonprompt = ROOT.RooChebychev("cheb_poly_landau_tauz_nonprompt", "cheb_poly_landau_tauz_nonprompt", tauz, ROOT.RooArgList(*cheb_coeffs_landau_tauz_nonprompt))
    model_frac_tauz_nonprompt = ROOT.RooRealVar("cb_frac_tauz_nonprompt", "CB Fraction", 7.58468e-01)
    tauzNonPromptPdf = ROOT.RooAddPdf("tauzNonPromptPdf", "Landau + Chebyshev", ROOT.RooArgList(pdf_landau_tauz_nonprompt, cheb_poly_landau_tauz_nonprompt), ROOT.RooArgList(model_frac_tauz_nonprompt))



    # entry_fracs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
    #     entry_fracs_len = len(entry_fracs) 


        # for i in range(entry_fracs_len):


    event_num = 10000
    signalToBackground = 0.5
    fb = 0.1
    nSig = event_num*signalToBackground
    nBkg = event_num*(1-signalToBackground)

    promptNum = 5000#nSig*(1-fb) #entry_fracs[i]
    nonPromptNum = 5000#nSig*fb #entry_fracs[entry_fracs_len - i - 1]
    entryNum = promptNum + nonPromptNum


    nJPsi = ROOT.RooRealVar("nJPsi", "number of JPsi", 1000,0,2*entryNum)
    nBkg = ROOT.RooRealVar("nBkg", "number of background", 1000,0,2*nBkg) 
    nonPrompFrac = ROOT.RooRealVar("nonPrompFrac", "non prompt fraction", 0.1,0,1)

    TotalnJPsi = ROOT.RooFormulaVar("prompFrac", "@0*(1-@1)", ROOT.RooArgList(nJPsi,nonPrompFrac))
    TotalnJPsiNon = ROOT.RooFormulaVar("nonprompFrac", "@0*@1", ROOT.RooArgList(nJPsi,nonPrompFrac))


    modelMass = ROOT.RooAddPdf("modelMass", "massNonPromptPdf + massPromptPdf", ROOT.RooArgList(massNonPromptPdf,massPromptPdf), ROOT.RooArgList(nonPrompFrac))
    modelTauz = ROOT.RooAddPdf("modelTauz", "tauzNonPromptPdf + tauzPromptPdf", ROOT.RooArgList(tauzNonPromptPdf,tauzPromptPdf), ROOT.RooArgList(nonPrompFrac))


    cat = ROOT.RooCategory("cat", "cat")
    cat.defineType("massCat")
    cat.defineType("tauzCat")

    simfit = ROOT.RooSimultaneous("simfit", "", cat)
    simfit.addPdf(modelMass, "massCat")
    simfit.addPdf(modelTauz,"tauzCat")

    genMass = massPromptPdf.generate(ROOT.RooArgSet(mass), promptNum)
    genMassNonPrompt = massNonPromptPdf.generate(ROOT.RooArgSet(mass), nonPromptNum)

    genTauz = tauzPromptPdf.generate(ROOT.RooArgSet(tauz), promptNum)
    genTauzNonPrompt = tauzNonPromptPdf.generate(ROOT.RooArgSet(tauz), nonPromptNum)

    genMass.append(genMassNonPrompt)
    genTauz.append(genTauzNonPrompt)


    combData = ROOT.RooDataSet("combData", "combined data",
        {mass, tauz}, 
        Index=cat, 
        Import={"massCat": genMass, "tauzCat": genTauz},
    )

    fitResult = simfit.fitTo(combData, Extended=True, Save=True, PrintLevel=-1)
    fitResult.Print()
    # pr_res = "Prompt num: {0}/{1}".format(promptNum, nJPsi)
    # non_pr_res = "Non-Prompt num: {0}/{1}".format(nonPromptNum, nJPsiNon)

    # frac_res = "Prompt num: {0}/{1}".format(nonPromptNum/(promptNum + nonPromptNum), nonPrompFrac)
    # print("This is the fraction: ",frac_res)
    # print("-------------------------------------------------------------------")

    # with open("mc_valid.txt", "a") as file:
    #     file.write(f"{frac_res}")

    frame1 = mass.frame(ROOT.RooFit.Title("Invariant Mass Fit Result"))
    combData.plotOn(frame1, ROOT.RooFit.Cut("cat==cat::massCat"))
    #data.plotOn(framep,RooFit.Cut("cat==cat::massCat"))
    #genMassPrompt.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))
    simfit.plotOn(frame1, ROOT.RooFit.Name("massAllPdf"), Slice=(cat, "massCat"), ProjWData=(cat,combData))
    simfit.plotOn(frame1, ROOT.RooFit.Name("massPromptPdf"), Slice=(cat, "massCat"), Components="massPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
    simfit.plotOn(frame1, ROOT.RooFit.Name("massNonPromptPdf"), Slice=(cat, "massCat"), Components="massNonPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)



    frame2 = tauz.frame(ROOT.RooFit.Title("Pseudo Proper Decay Length Fit Result"))
    combData.plotOn(frame2, ROOT.RooFit.Cut("cat==cat::tauzCat"))
    #genTauzPrompt.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzAllPdf"), Slice=(cat, "tauzCat"), ProjWData=(cat,combData))
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzPromptPdf"), Slice=(cat, "tauzCat"), Components="tauzPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kRed+1)
    simfit.plotOn(frame2, ROOT.RooFit.Name("tauzNonPromptPdf"), Slice=(cat, "tauzCat"), Components="tauzNonPromptPdf", ProjWData=(cat,combData), LineStyle="--", LineColor=ROOT.kAzure+4)




    canvas = ROOT.TCanvas("canvas", "Fit Plot", 1280, 720)

    legend1 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
    legend1.AddEntry(frame1.findObject("massAllPdf"), "Invariant mass fit", "l")
    legend1.AddEntry(frame1.findObject("massPromptPdf"), "Prompt fraction", "l")
    legend1.AddEntry(frame1.findObject("massNonPromptPdf"), "Non prompt fraction", "l")

    legend2 = ROOT.TLegend(0.55, 0.65, 0.85, 0.85)
    legend2.AddEntry(frame2.findObject("tauzAllPdf"), "PPDL fit", "l")
    legend2.AddEntry(frame2.findObject("tauzPromptPdf"), "Prompt fraction", "l")
    legend2.AddEntry(frame2.findObject("tauzNonPromptPdf"), "Non prompt fraction", "l")



    canvas.Divide(2,1)
    canvas.cd(1)
    frame1.Draw()
    legend1.Draw()

    canvas.cd(2)
    frame2.Draw()
    legend2.Draw()

    canvas.Update()
    canvas.SaveAs(PATH + f"mc_toy_pdf_{ptMin[iPt]}_{ptMax[iPt]}.png")