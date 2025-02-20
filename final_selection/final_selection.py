import sys, os, glob, shutil, json, math, re, random, time
import ROOT
from config_final_selection import input_dir,output_dir, sig_processes, bckg_processes, cuts






def analyze(rdf):

    # make graphs and store
    graphs = []
    

    h_njets = rdf.Histo1D(("njets", ";njets", 10, 0, 10), "njets")
    h_jet_mass = rdf.Histo1D(("jet_mass", ";jets mass [GeV]", 200, 0, 500), "jet_mass")
    h_jet_pt = rdf.Histo1D(("jet_pt", ";jets p_{T} [GeV]", 100, 0, 500), "jet_pt")
    h_jet_eta = rdf.Histo1D(("jet_eta", ";jets \eta ", 200, -5, 5), "jet_eta")
    h_jet_phi = rdf.Histo1D(("jet_phi", ";jets \phi ", 200, 0, 5), "jet_phi")
    
    h_jet_d23 = rdf.Histo1D(("jet_d23", ";jet d23", 200, 0, 0.06), "jet_d23")
    h_jet_d34 = rdf.Histo1D(("jet_d34", ";jet_d34", 200, 0, 0.015), "jet_d34")
    h_jet_d45 = rdf.Histo1D(("jet_d45", ";jet_d45", 200, 0, 0.06), "jet_d45")
    h_jet_d56 = rdf.Histo1D(("jet_d56", ";jet_d56", 200, 0, 0.02), "jet_d56")

    h_BTag_80 = rdf.Histo1D(("BTag_80", ";BTag_80", 10, 0, 10), "BTag_80")
    h_BTag_70 = rdf.Histo1D(("BTag_70", ";BTag_70", 10, 0, 10), "BTag_70")
    h_BTag_50 = rdf.Histo1D(("BTag_50", ";BTag_50", 10, 0, 10), "BTag_50")

    h_highest_pt_jet_m = rdf.Histo1D(("highest_pt_jet_m", ";j1 mass [GeV]", 200, 0, 500), "highest_pt_jet_m")
    h_highest_pt_jet_pt = rdf.Histo1D(("highest_pt_jet_pt", ";j1 p_{T} [GeV]", 200, 0, 500), "highest_pt_jet_pt")
    h_highest_pt_jet_eta = rdf.Histo1D(("highest_pt_jet_eta", ";j1 \eta", 200, -5, 5), "highest_pt_jet_eta")
    h_highest_pt_jet_phi = rdf.Histo1D(("highest_pt_jet_phi", ";j1 \phi", 200, 0, 5), "highest_pt_jet_phi")

    h_FourJet_m = rdf.Histo1D(("FourJet_m", ";M_{4j} [GeV]", 200, 0, 500), "FourJet_m")
    h_FourJet_pt = rdf.Histo1D(("FourJet_pt", ";p_{T}^{4j} [GeV]", 200, 0, 500), "FourJet_pt")
    h_FourJet_eta = rdf.Histo1D(("FourJet_eta", ";\eta^{4j}", 200, -5, 5), "FourJet_eta")
    h_FourJet_phi = rdf.Histo1D(("FourJet_phi", ";\phi^{4j}", 200, 0, 5), "FourJet_phi")



    h_W_jets_ON_Mass = rdf.Histo1D(("jets_W_On_Mass", ";W mass [GeV]", 200, 0, 500), "jets_W_On_Mass")
    h_W_jets_OFF_Mass = rdf.Histo1D(("jets_W_OFF_Mass", ";W* mass [GeV]", 200, 0, 500), "jets_W_OFF_Mass")




    h_nmuons = rdf.Histo1D(("n_muons", ";number 0f muons", 10, 0, 10), "n_muons")
    h_muon_iso = rdf.Histo1D(("muon_iso", ";muon iso", 100, 0, 1), "muon_iso")
    h_muon_pt = rdf.Histo1D(("muon_pt", ";muon p_{T}", 100, 0, 500), "muon_pt")

    h_muon_eta = rdf.Histo1D(("muon_eta", ";muon \eta", 200, -5, 5), "muon_eta")
    h_muon_phi = rdf.Histo1D(("muon_phi", ";muon \phi", 200, 0, 8), "muon_phi")

    h_highestPT_muon_pt = rdf.Histo1D(("highest_pt_muon_pt", ";\mu 1 p_{T} [GeV]", 100, 0, 500), "highest_pt_muon_pt")
    h_highestPT_muon_m = rdf.Histo1D(("highest_pt_muon_m", ";\mu 1 mass [GeV]", 100, 0, 500), "highest_pt_muon_m")
    h_highestPT_muon_eta = rdf.Histo1D(("highest_pt_muon_eta", ";\mu 1 \eta", 200, -5, 5), "highest_pt_muon_eta")
    h_highestPT_muon_phi = rdf.Histo1D(("highest_pt_muon_phi", ";\mu 1 \phi", 200, 0, 8), "highest_pt_muon_phi")


    h_Dimuon_m= rdf.Histo1D(("Dimuon_m", ";M{\mu\mu} [GeV]", 200, 0, 500), "Dimuon_m")
    h_Dimuon_pt = rdf.Histo1D(("Dimuon_pt", ";p_{T}^{\mu\mu} [GeV]", 200, 0, 500), "Dimuon_pt")
    h_Dimuon_eta = rdf.Histo1D(("Dimuon_eta", ";\eta^{\mu\mu}", 200, -5, 5), "Dimuon_eta")
    h_Dimuon_phi = rdf.Histo1D(("Dimuon_phi", ";\phi^{\mu\mu}", 200, 0, 5), "Dimuon_phi")
  

    h_delR_mu_jet = rdf.Histo1D(("delR_mu_jet", "\Delta R^{j\mu}", 100, 0, 10), "delR_mu_jet")

    h_missingEt_met = rdf.Histo1D(("MissingET_met", ";missing_et [GeV]", 100, 0, 500), "MissingET_met")
    


    graphs.append(h_njets)    
    graphs.append(h_jet_pt)
    graphs.append(h_jet_mass)
    graphs.append(h_jet_eta)
    graphs.append(h_jet_phi)
    graphs.append(h_jet_d23)
    graphs.append(h_jet_d34)
    graphs.append(h_jet_d45)
    graphs.append(h_jet_d56)

    graphs.append(h_BTag_80)
    graphs.append(h_BTag_70)
    graphs.append(h_BTag_50)


    graphs.append(h_highest_pt_jet_pt)
    graphs.append(h_highest_pt_jet_m)
    graphs.append(h_highest_pt_jet_phi)
    graphs.append(h_highest_pt_jet_eta)

    graphs.append(h_FourJet_m)
    graphs.append(h_FourJet_eta)
    graphs.append(h_FourJet_pt)
    graphs.append(h_FourJet_phi)


    graphs.append(h_W_jets_ON_Mass)
    graphs.append(h_W_jets_OFF_Mass)


    graphs.append(h_nmuons)
    graphs.append(h_muon_pt)
    graphs.append(h_muon_eta)
    graphs.append(h_muon_phi)

    graphs.append(h_muon_iso)
    graphs.append(h_highestPT_muon_pt)
    graphs.append(h_highestPT_muon_eta)
    graphs.append(h_highestPT_muon_m)
    graphs.append(h_highestPT_muon_phi)

    graphs.append(h_Dimuon_m)
    graphs.append(h_Dimuon_pt)
    graphs.append(h_Dimuon_eta)
    graphs.append(h_Dimuon_phi)
    graphs.append(h_delR_mu_jet)
    graphs.append(h_missingEt_met)

    return graphs

    # execute the RDFs
    
    
    


if __name__ == "__main__":


    for process_name in sig_processes:
          input_file = f"{input_dir}/output_delphes_ee_{process_name}_ilc_500.root"
          print(f"Processing file:{input_file}")
          rdf = ROOT.RDataFrame("Delphes", input_file)
          rdf = rdf.Filter(cuts)
          histograms = analyze(rdf)

          ROOT.RDF.RunGraphs(histograms)

          output_file = f"{output_dir}/hist_delphes_ee_{process_name}_ilc_500.root" 
          fOut = ROOT.TFile(output_file, "RECREATE")
          for g in histograms: g.Write()
          fOut.Close()

    for process_name in bckg_processes:
          input_file = f"{input_dir}/output_delphes_ee_{process_name}_ilc_500.root"
          print(f"Processing file:{input_file}")
          rdf = ROOT.RDataFrame("Delphes", input_file)
          rdf = rdf.Filter(cuts)
          histograms = analyze(rdf)

          ROOT.RDF.RunGraphs(histograms)

          output_file = f"{output_dir}/hist_delphes_ee_{process_name}_ilc_500.root" 
          fOut = ROOT.TFile(output_file, "RECREATE")
          for g in histograms: g.Write()
          fOut.Close()
    
    
 
