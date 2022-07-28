############################################################################################################
# This code is based on https://github.com/jdmulligan/JETSCAPE-analysis.git (by James Mulligan @jdmulligan)
############################################################################################################

# General
import math
import tqdm
import argparse
import csv

# Fastjet via python (from external library heppy)
import fastjet as fj
import fjext

from reader import reader_ascii

# ---------------------------------------------------------------
input_file_hadrons = ''
output_file_jets = ''
jetR = 0.0
jetPtMin = 100.0 # Minimum value of jet pt
rapMax = 5.0 # Maximum value for abs of jet rapidity
minTrackPt=0.05 # Minimum value of track particle pt
# ---------------------------------------------------------------
# Main processing function
# ---------------------------------------------------------------
def analyze_jetscape_events():

    # Load JETSCAPE output file (James's Reader module is used)
    reader = reader_ascii.ReaderAscii(input_file_hadrons)

    # Show Progress Bar
    event_id = 0
    n_event_max = 1000
    pbar = tqdm.tqdm(range(n_event_max))

    # Read Events in JETSCAPE output file
    for event in reader(n_events=n_event_max):

        if not event:
            nstop = pbar.n
            pbar.close()
            print(f'End of file at event {nstop}.')

        analyze_event(event, event_id)
        event_id += 1
        pbar.update()


# ---------------------------------------------------------------
# Analyze a single event -- fill user-defined output objects
# ---------------------------------------------------------------
def analyze_event(event, event_id=1):

  # tag to create new output file
  new_file = False

  # Get Hadron List for a Event
  hadrons = event.hadrons(min_track_pt=minTrackPt)

  # Create list of fastjet::PseudoJets
  fj_hadrons = fill_fastjet_constituents(hadrons)

  # Set jet definition and a jet selector
  jet_def = fj.JetDefinition(fj.antikt_algorithm, jetR)
  jet_selector = fj.SelectorPtMin(jetPtMin) & fj.SelectorAbsRapMax(rapMax)

  if event_id == 0:
    print('jet definition is:', jet_def)
    print('jet selector is:', jet_selector, '\n')
    # Create new output file for the first event
    new_file = True

  # Do jet finding
  cs = fj.ClusterSequence(fj_hadrons, jet_def)
  jets = fj.sorted_by_pt(cs.inclusive_jets())
  n_jet = min([len(jets), 2])
  jets = jets[:n_jet]
  jets = jet_selector(jets)

  # Hole subtraction and get associated particles
  for jet in jets:
    holes_in_jet = fill_associated_particles(jet, hadrons, select_status='-', select_charged=False)    
    jet = hole_subtraction(jet,holes_in_jet)
    if jet.perp() > jetPtMin:
      charged_in_jet = fill_associated_particles(jet, hadrons, select_status=None, select_charged=True)
      new_file = write_output(jet, charged_in_jet, new_file)


# ---------------------------------------------------------------
# Write Output File
# ---------------------------------------------------------------
def write_output(jet, associated, new_file = False):

  # Data for reconstructed jet
  jet_status = 10
  jet_pid = 10  
  output_list = [[0, jet.perp(), jet.eta(), jet.phi(), jet_status, jet_pid]]

  # Data for associated particles
  for i, assoc in enumerate(associated):
    px = assoc.momentum.px
    py = assoc.momentum.py
    pz = assoc.momentum.pz
    e = assoc.momentum.e
    pj = fj.PseudoJet(px, py, pz, e)
      
    output = [i+1, pj.perp(), pj.eta(), pj.phi(), assoc.status, assoc.pid ]
    output_list.append(output)

  # Write Data
  mode = 'a'
  if new_file == True:
    mode = 'w'
  f = open(output_file_jets, mode, newline='')
  writer = csv.writer(f)
  writer.writerows(output_list)
  f.close()

  # Not to create new output file
  return False

# ---------------------------------------------------------------
# Hole Subtraction
# ---------------------------------------------------------------
def hole_subtraction(jet, holes):

  # Total enrgy momentum of holes
  px = 0.0
  py = 0.0
  pz = 0.0
  e = 0.0

  for hole in holes:
    px = px + hole.momentum.px
    py = py + hole.momentum.py
    pz = pz + hole.momentum.pz
    e = e + hole.momentum.e

  # Subtract enrgy momentum of holes
  jet_px = jet.px() - px
  jet_py = jet.py() - py
  jet_pz = jet.pz() - pz
  jet_e = jet.e() - e
  jet.reset(jet_px, jet_py, jet_pz, jet_e)
  return jet

# ---------------------------------------------------------------
# Fill associated hadrons in jet cone
# ---------------------------------------------------------------
def fill_associated_particles(jet, hadrons, select_status=None, select_charged=False):

  # Pick only holes
  if select_status == '-':
    hadrons = list(filter(is_a_hole, hadrons))
  # Pick only particles
  elif select_status == '+':
    hadrons = list(filter(is_a_particle, hadrons))

  # Pick charged particles
  if select_charged == True:
    hadrons = list(filter(is_charged, hadrons))


  # Pick particles in jet cone
  associated = []
  for hadron in hadrons:

    px = hadron.momentum.px
    py = hadron.momentum.py
    pz = hadron.momentum.pz
    e = hadron.momentum.e

    fj_particle = fj.PseudoJet(px, py, pz, e)
    
    delta_eta = fj_particle.eta() - jet.eta()
    delta_phi = fj_particle.delta_phi_to(jet)
    delta_r = math.sqrt(delta_eta*delta_eta + delta_phi*delta_phi)
    #delta_r = fj_particle.delta_R(jet)

    # inside jet cone
    if delta_r < jetR:
      associated.append(hadron)

  return associated

# ---------------------------------------------------------------
# Fill hadrons into vector of fastjet pseudojets
# ---------------------------------------------------------------
def fill_fastjet_constituents(hadrons):

  # Create particle list (without holes)
  particles = list(filter(is_a_particle, hadrons))

  px = [particle.momentum.px for particle in particles]
  py = [particle.momentum.py for particle in particles]
  pz = [particle.momentum.pz for particle in particles]
  e = [particle.momentum.e for particle in particles]
        
  # Create a vector of fastjet::PseudoJets from arrays of px,py,pz,e
  fj_particles = fjext.vectorize_px_py_pz_e(px, py, pz, e)
        
  return fj_particles

# ---------------------------------------------------------------
# Find Hole Hadrons
# ---------------------------------------------------------------
def is_a_hole (hadron):
  if hadron.status == -1:
      return True
  else:
      return False

# ---------------------------------------------------------------
# Find Substantial Hadrons
# ---------------------------------------------------------------
def is_a_particle (hadron):
  if hadron.status == 1 or hadron.status == 0:
    return True
  else:
    return False

# ---------------------------------------------------------------
# Find Charged Hadrons
# ---------------------------------------------------------------
def is_charged (hadron):
  pid = hadron.pid
  # Charged hadrons: (pi+, K+, p+, Sigma+, Sigma-, Xi-, Omega-)  
  if abs(pid) in [211, 321, 2212, 3222, 3112, 3312, 3334]:
    return True
  else:
    return False



# ---------------------------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
      "-r", 
      "--jetconeSize",
      type=float, 
      metavar="jetconeSize",
      default=0.4,
      help="jet cone size")
    
    parser.add_argument(
      "-i", 
      "--inputFile",
      type=str, 
      metavar="inputFile",
      default="../../JETSCAPE/build/test_out_final_state_hadrons.dat",
      help="Input file of JETSCAPE hadron list")

    parser.add_argument(
      "-o", 
      "--outputFile",
      type=str, 
      metavar="outputFile",
      default="../data/jet_info.dat",
      help="Output file of reconstructed jet information")

    # Parse the arguments
    args = parser.parse_args()

    # jet cone size
    jetR = args.jetconeSize

    # input and output file names
    input_file_hadrons = args.inputFile
    output_file_jets = args.outputFile

    analyze_jetscape_events()
