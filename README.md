# Analysis of Monte-Carlo Simulated events with Root data frame
Data analysis of Monte-Carlo generated events from electron-positron collisions at the international linear collider (ILC).
Events are generated by WHIZARD. A generic ILC detector is simulated by DELPHES (fast simulation).
The analysis takes three steps: preselection, final selection and plotting. The delphes output files are named in the following way: delphes_ee_{process_name}_ilc_500.root
To run the analysis, you need to have an installation of ROOT and DELPHES. Then it is essential to include DELPHES environment variables:
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<path/to/delphes>
export ROOT_INCLUDE_PATH=<path/to/delphes>:$ROOT_INCLUDE_PATH
```
The analysis is performed in pyROOT using ROOT data frames (RDF). Operations on the data columns are performed by C++ functions, which are defined in function.h.

## Pre-selection
The preselection of events aims at selecting the interesting objects(electron,muon,jet,...etc) from the delphes ROOT Tree.
And applying the neccessary operations on them (computing mass, finding highest pt jet,...etc) using the functions defined in function.h.
The {process_names} for which you want to run the analysis are stored in config_pre-selection.py. Where a list is defined for the signal and the background processes.
The output is then stored in a root tree called "events". To run pre-selection simply do:
```python
python pre-selection.py
```


## Final selectio 
In this step, final selection cuts are applied to discriminate signal from background. After that, histogram objects are created from the defined branches.
The cuts and process_names are defined in the file config_final_selection.py. To run final selection simply do:
```python
python final_selection.py
```


## Plotting
In this step, plots are created from the defined histograms. The background histograms are stacked, while the signal histograms are overlayed.
Histograms are normalized to the corresponding cross-section and total integrated luminosity. A dictionary is provided in process_data_ilc_500GeV.json,
where the process_name is the key and the cross-section, total number of generated events and other plotting variables are the values.
You can edit config_plotting.py to provide the list of histograms, the total integrated luminosity and the signal and background process_names.
To run the plotting step, simply do: 
```python
python plotting.py
```
