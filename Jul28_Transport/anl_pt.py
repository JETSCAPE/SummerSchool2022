import argparse
import sys
import os
import smash_basic_scripts as sb
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("pdg_list", type=str)
parser.add_argument("file_to_analyze", type=str,
                    help="binary file containing collision history")
parser.add_argument("output_dir", type=str)
parser.add_argument("config_file", help="config file")

args = parser.parse_args()

pdg_list = np.array([int(sb.name_to_pdg(x, args.config_file)) for x in args.pdg_list.split(',')])
total_pdgs = pdg_list.shape[0]

# Binning in pt
n_bins = 70
bin_edges = np.linspace(0.0, 2.0, num=n_bins + 1)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0


def analyze_file(path):
    pt_lists = [[] for i in range(total_pdgs)]
    pt_sqr_lists = [[] for i in range(total_pdgs)]
    event_num = 0
    with sb.BinaryReader(path) as reader:
        smash_version = reader.smash_version

        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num += 1
                # print("In Event #", event_num, "found...")
                # for i in np.arange(total_pdgs):
                #     print(sb.pdg_to_name( pdg_list[i]), ":",int(mul[i]))
            if (block['type'] == b'p'):  # particles
                px = block['part']['p'][:,1]
                py = block['part']['p'][:,2]
                pt = np.sqrt(px*px + py*py)  # pt of all particles
                for i in np.arange(len(block['part'])):
                    part = block['part'][i]
                    if part['pdgid'] in pdg_list:
                        idx = np.where(pdg_list==part['pdgid'])
                        idx = idx[0][0]  # numpy where returns array
                        pt_lists[idx].append(pt[i])
                        pt_sqr_lists[idx].append(pt[i]*pt[i])

    for i in range(total_pdgs):
        pt_average = float(sum(pt_lists[i]))/len(pt_lists[i])
        pt_sqr_average = float(sum(pt_sqr_lists[i]))/len(pt_sqr_lists[i])
        pt_avg_err = np.sqrt((pt_sqr_average - pt_average * pt_average)/(len(pt_lists[i]) - 1))
        print("<pt>("+str(pdg_list[i])+") =", pt_average,"+-", pt_avg_err)
        hist, _ = np.histogram(pt_lists[i], bins=bin_edges)
        hist = hist/float(event_num)
        if not os.path.exists(args.output_dir): os.mkdir(args.output_dir)
        with open(args.output_dir+"/pt_"+str(pdg_list[i])+".txt", 'w') as f:
            f.write('# pt histogram for:\n' % pdg_list[i])
            f.write('%d\n' % pdg_list[i])
            f.write('# <pt> \n')
            f.write('%.5f \n' % (pt_average))
            f.write('# <pt>_err \n')
            f.write(' %.5f \n' %  pt_avg_err)
            f.write('# bin centers \n')
            for bin_center in bin_centers: f.write('%.3f ' % bin_center)
            f.write('\n')
            f.write('# hist counts \n')
            for j in np.arange(len(bin_centers)): f.write('%.5f ' % hist[j])
            f.write('\n')


analyze_file(args.file_to_analyze)
