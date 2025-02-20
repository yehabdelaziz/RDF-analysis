input_dir='../final_selection/histograms'
output_dir='plots'
process_info_file='process_data_ilc_500GeV.json'
Luminosity = 1000

bckg_process_names =[
             'jjH_HWW',  
             'llH_HWW',
#             'WW',
#             'ZZ',  
#             'ttbar',
]

sig_process_names =[
             'hh_mhh160_fw5_fww5_HWW',
             'hh_mhh160_fw10_fww10_HWW', 
]

histogram_names = ["highest_pt_jet_pt",
                       "highest_pt_jet_eta",
                       "FourJet_m",
                       "FourJet_pt",
                       "FourJet_eta",
                       "delR_mu_jet",
                       "jet_d23",
                       "jet_d34",
                       "jet_d45",
                       "jet_d56",
                       "muon_iso",
                       "highest_pt_muon_pt",
                       "highest_pt_muon_eta",
                       "Dimuon_m",
                       "Dimuon_pt",
                       "Dimuon_eta",
                       "BTag_80",
                       "BTag_70",
                       "BTag_50",
                       "MissingET_met",
                       "jet_pt",
                       "jets_W_On_Mass",
                       "jets_W_OFF_Mass",


    ]
