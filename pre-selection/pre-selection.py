import sys, os, glob, shutil, json, math, re, random, time
import ROOT
from config_pre_selection import  sig_processes, bckg_processes, sig_input_dir, bckg_input_dir , output_dir

ROOT.gSystem.Load("libDelphes")
ROOT.gInterpreter.Declare('#include "../classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "functions.h"')




def analyze(rdf):
  

    rdf = rdf.Define("njets", "Jet_N4_size")
    
    
    rdf = rdf.Define("jet_pt", "Jet_N4.PT")
    rdf = rdf.Define("jet_eta", "Jet_N4.Eta")
    rdf = rdf.Define("jet_phi", "Jet_N4.Phi")
    rdf = rdf.Define("jet_mass", "Jet_N4.Mass")

    rdf = rdf.Define("jet_d23","Jet_N4.ExclYmerge23")
    rdf = rdf.Define("jet_d34","Jet_N4.ExclYmerge34")
    rdf = rdf.Define("jet_d45","Jet_N4.ExclYmerge45")
    rdf = rdf.Define("jet_d56","Jet_N4.ExclYmerge56")

    rdf = rdf.Define("BTag_80", "Jet.BTag & (1 << 0)") 
    rdf = rdf.Define("BTag_70", "(Jet.BTag & (1 << 1))/2") 
    rdf = rdf.Define("BTag_50", "(Jet.BTag & (1 << 2))/4")

    rdf = rdf.Define("jets_tlv","makeLorentzVectors(jet_pt,jet_eta,jet_phi,jet_mass)")
    rdf = rdf.Define("highest_pt_jet_tlv","GetHighestPT_particle(jets_tlv)")
    rdf = rdf.Define("highest_pt_jet_pt","highest_pt_jet_tlv.Pt()")
    rdf = rdf.Define("highest_pt_jet_phi","highest_pt_jet_tlv.Phi()")
    rdf = rdf.Define("highest_pt_jet_eta","highest_pt_jet_tlv.Eta()")
    rdf = rdf.Define("highest_pt_jet_m","highest_pt_jet_tlv.M()")
    
    rdf = rdf.Define("FourJet_mom4", "sumP4(jet_pt, jet_eta, jet_phi, jet_mass)")
    rdf = rdf.Define("FourJet_m", "FourJet_mom4.M()")
    rdf = rdf.Define("FourJet_eta", "FourJet_mom4.Eta()")
    rdf = rdf.Define("FourJet_pt", "FourJet_mom4.Pt()")
    rdf = rdf.Define("FourJet_phi", "FourJet_mom4.Phi()")



    rdf = rdf.Define("jets_W_tlv","Get_resonance_Pair(jets_tlv,80.0)")
    rdf = rdf.Define("jets_W_On_Mass","(jets_W_tlv[0]+jets_W_tlv[1]).M()")
    rdf = rdf.Define("jets_W_OFF_Mass","(jets_W_tlv[2]+jets_W_tlv[3]).M()")



    rdf = rdf.Define("n_muons","Muon_size")
    rdf = rdf.Filter("n_muons > 1")
    rdf = rdf.Define("muon_pt", "Muon.PT")
    rdf = rdf.Define("muon_eta", "Muon.Eta")
    rdf = rdf.Define("muon_phi", "Muon.Phi")
    rdf = rdf.Define("muon_iso", "Muon.IsolationVar")


    rdf = rdf.Define("muon_mass", "return ROOT::VecOps::RVec<float>(n_muons, MUON_MASS);")
    rdf = rdf.Define("muons_tlv","makeLorentzVectors(muon_pt,muon_eta,muon_phi,muon_mass)")
    rdf = rdf.Define("highest_pt_muon_tlv","GetHighestPT_particle(muons_tlv)")
    rdf = rdf.Define("highest_pt_muon_pt","highest_pt_muon_tlv.Pt()")
    rdf = rdf.Define("highest_pt_muon_m","highest_pt_muon_tlv.M()")
    rdf = rdf.Define("highest_pt_muon_phi","highest_pt_muon_tlv.Phi()")
    rdf = rdf.Define("highest_pt_muon_eta","highest_pt_muon_tlv.Eta()")


    rdf = rdf.Define("Dimuon_mom4", "sumP4(muon_pt, muon_eta, muon_phi, muon_mass)")
    rdf = rdf.Define("Dimuon_m", "Dimuon_mom4.M()")
    rdf = rdf.Define("Dimuon_eta", "Dimuon_mom4.Eta()")
    rdf = rdf.Define("Dimuon_pt", "Dimuon_mom4.Pt()")
    rdf = rdf.Define("Dimuon_phi", "Dimuon_mom4.Phi()")
    


    rdf = rdf.Define("delR_mu_jet","delR(Dimuon_mom4,FourJet_mom4)")

     
    rdf = rdf.Define("MissingET_met", "MissingET.MET[0]")
    rdf = rdf.Define("MissingET_eta", "MissingET.Eta")
    rdf = rdf.Define("MissingET_phi", "MissingET.Phi[0]")
   


    return rdf
branchlist = [
                      "njets",
                      "jet_pt",
                      "jet_eta",
                      "jet_phi",
                      "jet_mass",
                      "jet_d23",
                      "jet_d34",
                      "jet_d45",
                      "jet_d56",

                      "BTag_80",
                      "BTag_70",
                      "BTag_50",
                      "highest_pt_jet_pt",
                      "highest_pt_jet_eta",
                      "highest_pt_jet_phi",
                      "highest_pt_jet_m",
                      "FourJet_m",
                      "FourJet_eta",
                      "FourJet_pt",
                      "FourJet_phi",

                      "jets_W_On_Mass",
                      "jets_W_OFF_Mass",
                      "n_muons",
                      "muon_pt",
                      "muon_phi",
                      "muon_eta",
                      "muon_iso",
                      "highest_pt_muon_pt",
                      "highest_pt_muon_eta",
                      "highest_pt_muon_phi",
                      "highest_pt_muon_m",
                      "Dimuon_m",
                      "Dimuon_eta",
                      "Dimuon_pt",
                      "Dimuon_phi",
                      "delR_mu_jet",
                      "MissingET_met",
                      "MissingET_eta",
                      "MissingET_phi",
                      ]

   

if __name__ == "__main__":

   
    for process_name in sig_processes:
          print(f"Processing file: {process_name}")
          input_file = f"{sig_input_dir}/delphes_ee_{process_name}_ilc_500.root",
          df = ROOT.RDataFrame("Delphes", input_file)
          df = analyze(df)
          output_file = f"{output_dir}/output_delphes_ee_{process_name}_ilc_500.root"
          df.Snapshot("Delphes", output_file, branchlist)
          print("Analysis complete")
          print(f"Output saved to: {output_file}")
          print("-------------------------------------------------------------------")
 
    for process_name in bckg_processes:
          print(f"Processing file: {process_name}")
          input_file = f"{bckg_input_dir}/delphes_ee_{process_name}_ilc_500.root",
          df = ROOT.RDataFrame("Delphes", input_file)
          df = analyze(df)
          output_file = f"{output_dir}/output_delphes_ee_{process_name}_ilc_500.root"
          df.Snapshot("Delphes", output_file, branchlist)
          print("Analysis complete")
          print(f"Output saved to: {output_file}")
          print("-------------------------------------------------------------------")
 

