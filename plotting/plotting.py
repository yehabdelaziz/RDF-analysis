import ROOT
import json
from config_plotting import input_dir,output_dir,process_info_file,Luminosity,bckg_process_names, sig_process_names, histogram_names



def plot_histograms_from_files(bckg_process_names,sig_process_names,process_info, hist_name, Luminosity,output_file="output.png"):
  
    stack = ROOT.THStack("stack", "ILC Simulation (Delphes)")
    canvas = ROOT.TCanvas("canvas", "Histograms", 800, 600)
    

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    bckg_histograms = []
    sig_histograms = []
    for process_name in bckg_process_names:
        file_name = f"{input_dir}/hist_delphes_ee_{process_name}_ilc_500.root"
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print(f"Error: Cannot open file {file_name}")
            continue
        total_nb_events = process_info['Background'][process_name]['total_nb_events']
        cross_section = process_info['Background'][process_name]['cross_section']
        legend_item = process_info['Background'][process_name]['legend']
        color = process_info['Background'][process_name]['color']

        hist = file.Get(hist_name)
        if not hist or not isinstance(hist, ROOT.TH1):
            print(f"Error: Histogram {hist_name} not found in file {file_name}")
            continue

        hist = hist.Clone(f"{process_name}")
        hist.SetDirectory(0)  # Detach the histogram from the file
        file.Close() 

        integral = hist.Integral()
        if integral > 0:
            hist.Scale(cross_section*Luminosity/total_nb_events)
        else:
            print(f"Warning: Histogram {hist_name} in file {file_name} has zero integral. Skipping normalization.")


        hist.SetLineColor(color)
        hist.SetFillColor(color)
        hist.SetLineWidth(2)
        hist.SetStats(0)
        print("hist_name is",hist.GetXaxis().GetTitle())

        bckg_histograms.append(hist)
        histogram_axis_label=hist.GetXaxis().GetTitle()
        stack.Add(hist)

        legend.AddEntry(hist, legend_item, "l")
        
    for process_name in sig_process_names:
        file_name = f"{input_dir}/hist_delphes_ee_{process_name}_ilc_500.root"
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print(f"Error: Cannot open file {file_name}")
            continue
        total_nb_events = process_info['Signal'][process_name]['total_nb_events']
        cross_section = process_info['Signal'][process_name]['cross_section']
        legend_item = process_info['Signal'][process_name]['legend']
        color = process_info['Signal'][process_name]['color']

        hist = file.Get(hist_name)
        if not hist or not isinstance(hist, ROOT.TH1):
            print(f"Error: Histogram {hist_name} not found in file {file_name}")
            continue

        hist = hist.Clone(f"{process_name}")
        hist.SetDirectory(0)  # Detach the histogram from the file
        file.Close() 

        integral = hist.Integral()
        if integral > 0:
            hist.Scale(cross_section*Luminosity/total_nb_events)
        else:
            print(f"Warning: Histogram {hist_name} in file {file_name} has zero integral. Skipping normalization.")


        hist.SetLineColor(color)
        hist.SetFillColor(0)

        hist.SetLineWidth(2)
        hist.SetStats(0)

        sig_histograms.append(hist)
        legend.AddEntry(hist, legend_item, "l")


    canvas.SetLogy()
    # This needs to be removed and replaced by stack.Draw("HIST")
    stack.Draw("HIST")
    stack.GetYaxis().SetTitle("Events")
    stack.GetXaxis().SetTitle(histogram_axis_label)
    stack.GetXaxis().SetTitleSize(0.05)
    stack.GetXaxis().SetTitleOffset(0.80)
    for hist in sig_histograms:
        hist.Draw("HIST SAME")

    legend.Draw()


    canvas.SaveAs(output_file)
    print(f"Canvas saved as {output_file}")

if __name__ == "__main__":
 
    with open(process_info_file, 'r') as file:
        process_info_dict = json.load(file)
    for histogram_name in histogram_names:
        output_image = f"{output_dir}/{histogram_name}_Normalized_ILC_500GeV.png"  # Output file for the canvas
        plot_histograms_from_files(bckg_process_names,sig_process_names,process_info_dict, histogram_name,Luminosity, output_image)





