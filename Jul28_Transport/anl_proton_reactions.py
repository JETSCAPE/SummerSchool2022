import argparse
import smash_basic_scripts as sb

parser = argparse.ArgumentParser()
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()

pdg_proton = 2212

scattering_partners_dict = {}

def analyze_file(path):
    print(path)
    event_num = 0
    intcounter = 0
    with sb.BinaryReader(path) as reader:
        smash_version = reader.smash_version

        for block in reader:
            if (block['type'] == b'f'):  # end of event
                event_num += 1
                print("event", event_num, intcounter, "proton interactions total in this event")
                intcounter = 0
            if (block['type'] == b'i'):  # interaction
                if block["nin"] != 2:
                    # not a scattering
                    continue
                if (block["incoming"]["pdgid"][0] == pdg_proton) or (block["incoming"]["pdgid"][1] == pdg_proton):
                    intcounter += 1

                    # proton scattering propterties
                    pdg_scatt_partner = block["incoming"]["pdgid"][0] if (block["incoming"]["pdgid"][1] == pdg_proton) else block["incoming"]["pdgid"][1]
                    time = sb.get_block_time(block)
                    outgoing_pdgs = block["outgoing"]["pdgid"]
                    process_type = block["process_type"]  # see documentation for process types http://theory.gsi.de/~smash/doc/2.2/namespacesmash.html#a4fe2931bde1378bf2ff49ccf40dbb08c

                    print(pdg_scatt_partner)

                    # If you managed to get until here, you get REWARDed by getting
                    # the already finished implementation of the counting of the scattering
                    # partners in a dictonary.
                    # Print it at the end and compare with the pdg numbers in the particles.txt
                    # to see the most likely interaction of protons.
                    if pdg_scatt_partner in scattering_partners_dict:
                        scattering_partners_dict[pdg_scatt_partner] += 1
                    else:
                        scattering_partners_dict[pdg_scatt_partner] = 1

for file_to_analyze in args.files_to_analyze:
    analyze_file(file_to_analyze)


# print(scattering_partners_dict)
# To print out the dictonary of scatterin partner counts ordered,
# have a look here https://stackoverflow.com/a/2258273
