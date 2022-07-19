import argparse
import smash_basic_scripts as sb

parser = argparse.ArgumentParser()
parser.add_argument("files_to_analyze", nargs='+',
                    help="binary file(s) containing collision history")
args = parser.parse_args()

pdg_proton = 2212

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

                    pdg_scatt_partner = block["incoming"]["pdgid"][0] if (block["incoming"]["pdgid"][1] == pdg_proton) else block["incoming"]["pdgid"][1]
                    time = sb.get_block_time(block)

                    print(pdg_scatt_partner)

for file_to_analyze in args.files_to_analyze:
    analyze_file(file_to_analyze)
