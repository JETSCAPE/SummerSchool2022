import argparse
import sys
import smash_basic_scripts as sb
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("pdg_list", type=str)
parser.add_argument("config_file", help="config file")
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()

pdg_list = np.array([int(sb.name_to_pdg(x, args.config_file)) for x in args.pdg_list.split(',')])
total_pdgs = pdg_list.shape[0]


def analyze_file(path):
    mul     = np.zeros(total_pdgs)
    mul_sqr = np.zeros(total_pdgs)
    event_num = 0
    with sb.BinaryReader(path) as reader:
        smash_version = reader.smash_version

        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num += 1
                print("In event #", event_num, "found...")
                for i in np.arange(total_pdgs):
                    print(sb.pdg_to_name(pdg_list[i]), ":",int(mul[i]))
            if (block['type'] == b'p'):  # particles
                for i in np.arange(total_pdgs):
                    part_num = sb.count_pdg_in_block(block, pdg_list[i])
                    mul[i] = part_num
                    mul_sqr[i] = part_num*part_num
                print("Total number of particles in event #", event_num,":", len(block['part']))

for file_to_analyze in args.files_to_analyze:
    analyze_file(file_to_analyze)
