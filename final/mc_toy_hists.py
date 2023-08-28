import ROOT
from ROOT import *

PATH = "/afs/cern.ch/user/l/lvicenik/private/summer_student_quarkonia_run3/root_files/"

templateFile = ROOT.TFile(PATH + "template.root")


hMassPromptDistr  = []
hMassNonPromptDistr = []
hTauzPromptDistr = []
hTauzNonPromptDistr = []

hMassPromptIntHist  = []
hMassNonPromptIntHist = []
hTauzPromptIntHist = []
hTauzNonPromptIntHist = []

ptMin = [0, 2, 4, 6]
ptMax = [2, 4, 6, 10]


mass = ROOT.RooRealVar("Dimuon mass", "Dimuon Invariant mass", 2, 5)
tauz = ROOT.RooRealVar("Dimuon tauz", "Dimuon pseudoproper decay length", -0.007, 0.007)

# normalize or not?

# for iPt in range(0, len(ptMin)):
#     hMassPromptDistr.append(ROOT.TH1F("hMassPromptDistr_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
#     hMassNonPromptDistr.append(ROOT.TH1F("hMassNonPromptDistr_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon mass ;m (GeV/c^2);#", 200, 2, 5))
#     hTauzPromptDistr.append(ROOT.TH1F("hTauzPromptDistr_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007))
#     hTauzNonPromptDistr.append(ROOT.TH1F("hTauzNonPromptDistr_{}_{}".format(ptMin[iPt], ptMax[iPt]),"Dimuon pseudoproper decay length ;m (GeV/c^2);#", 100, -0.007, 0.007))



for iPt in range(0, len(ptMin)):

    hMassPromptDistr = templateFile.Get(f"hMassPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hMassNonPromptDistr = templateFile.Get(f"hMassNonPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzPromptDistr = templateFile.Get(f"hTauzPrompt_{ptMin[iPt]}_{ptMax[iPt]}")
    hTauzNonPromptDistr = templateFile.Get(f"hTauzNonPrompt_{ptMin[iPt]}_{ptMax[iPt]}")

    hMassPromptHist = ROOT.RooDataHist("hMassPromptHist", "hMassPromptHist", ROOT.RooArgList(mass), hMassPromptDistr)
    hMassNonPromptHist = ROOT.RooDataHist("hMassNonPromptHist", "hMassNonPromptHist", ROOT.RooArgList(mass), hMassNonPromptDistr)
    hTauzPromptHist = ROOT.RooDataHist("hTauzPromptHist", "hTauzPromptHist", ROOT.RooArgList(tauz), hTauzPromptDistr)
    hTauzNonPromptHist = ROOT.RooDataHist("hTauzNonPromptHist", "hTauzNonPromptHist", ROOT.RooArgList(tauz), hTauzNonPromptDistr)

    massPromptPdf = ROOT.RooHistPdf("massPromptPdf", "mass prompt pdf", ROOT.RooArgList(mass), hMassPromptHist)
    massNonPromptPdf = ROOT.RooHistPdf("massNonPromptPdf", "mass non prompt pdf", ROOT.RooArgList(mass), hMassNonPromptHist)
    tauzPromptPdf = ROOT.RooHistPdf("tauzPromptPdf", "tauz prompt pdf", ROOT.RooArgList(tauz), hTauzPromptHist)
    tauzNonPromptPdf = ROOT.RooHistPdf("tauzNonPromptPdf", "tauz non prompt pdf", ROOT.RooArgList(tauz), hTauzNonPromptHist)


    entry_fracs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
    entry_fracs_len = len(entry_fracs) 


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
    canvas.SaveAs(f"mc_toy_recovery_{ptMin[iPt]}_{ptMax[iPt]}.png")