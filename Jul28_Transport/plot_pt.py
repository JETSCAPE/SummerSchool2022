import numpy as np
import matplotlib.pyplot as plt
import glob
import smash_basic_scripts as sb
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_dirs", type=str)
parser.add_argument("config_file", help="config file")
args = parser.parse_args()

l_styles   = ["-",  "--"]
m_styles   = []

input_dirs_list = args.input_dirs.split(',')

for i,input_dir in enumerate(input_dirs_list):
    #print(input_dir, i)
    input_files = glob.glob(input_dir+("/*.txt"))

    for j, input_file in enumerate(input_files):

        with open(input_file, 'r') as f:
            f.readline()
            pdg = int(f.readline())
            f.readline()
            avg_pt = f.readline()
            f.readline()
            avg_pt_err = f.readline()
            f.readline()
            f.readline()

            bins_and_hist = np.loadtxt(input_file, skiprows=6)
            bin_width = bins_and_hist[0][1] - bins_and_hist[0][0]

            scale = 1
            if pdg == -211:
                scale = 10
            if pdg == 321:
                scale = 5


            # plot dN/pTdpT
            if scale > 1:
                lab = sb.pdg_to_name(pdg, args.config_file)+" "+input_dir.replace("results_","") + " (x"+str(scale)+")"
            else:
                lab = sb.pdg_to_name(pdg, args.config_file)+" "+input_dir.replace("results_","")
            plt.plot(bins_and_hist[0],scale*bins_and_hist[1]/(bin_width*bins_and_hist[0]), label=lab, linestyle=l_styles[i])

plt.xlabel(r'$p_T$ [GeV]')
plt.ylabel(r'$dN/p_Tdp_T$ [1/GeV]')
plt.legend(ncol=2)
plt.yscale('log')
plt.savefig("pt_spectra.pdf")
plt.cla()


custom_xticks = []
custom_xticks_labels = []
shift = -0.05
found_wo = False
for i,input_dir in enumerate(input_dirs_list):
    input_files = glob.glob(input_dir+("/*.txt"))

    for j, input_file in enumerate(input_files):

        with open(input_file, 'r') as f:
            f.readline()
            pdg = int(f.readline())
            f.readline()
            avg_pt = float(f.readline())
            f.readline()
            avg_pt_err = float(f.readline())
            f.readline()
            f.readline()

            if "wo" in input_dir:
                plt.errorbar(float(j)+shift, avg_pt, yerr=avg_pt_err,marker='d', ms=10, mfc="w" ,label=sb.pdg_to_name(pdg, args.config_file)+" "+input_dir.replace("results_",""))
                found_wo = True
            else:
                plt.errorbar(float(j)+shift, avg_pt, yerr=avg_pt_err,marker='d', ms=10 ,label=sb.pdg_to_name(pdg, args.config_file)+" "+input_dir.replace("results_",""))

            custom_xticks.append(float(j))
            custom_xticks_labels.append(sb.pdg_to_name(pdg, args.config_file))
    shift+=0.1

if found_wo: plt.title("Empty symbols without rescattering")
plt.ylabel(r'$\langle p_T \rangle$ [GeV]')
plt.xlim(-0.5,2.5)
plt.xticks(ticks=custom_xticks, labels=custom_xticks_labels)
# plt.legend()
plt.savefig("pt_avg.pdf")
plt.cla()
