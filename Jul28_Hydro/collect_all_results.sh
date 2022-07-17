#!/usr/bin/env bash

folder=$1

echo "collect results into " $folder " ..."

mkdir -p $folder

mv meanpT_estimators_eta_-0.5_0.5.dat $folder/ 2> /dev/null
mv meanpT_estimators_tau_*.dat $folder/ 2> /dev/null
mv eccentricities_evo_ed_tau_*.dat $folder/ 2> /dev/null
mv eccentricities_evo_eta_-0.5_0.5.dat $folder/ 2> /dev/null
mv eccentricities_evo_nB_tau_*.dat $folder/ 2> /dev/null
mv momentum_anisotropy_tau_*.dat $folder/ 2> /dev/null
mv momentum_anisotropy_eta_-0.5_0.5.dat $folder/ 2> /dev/null
mv inverse_Reynolds_number_eta_-0.5_0.5.dat $folder/ 2> /dev/null
mv global_conservation_laws.dat $folder/ 2> /dev/null
mv surface_MUSIC.dat $folder/ 2> /dev/null
mv evolution_all_xyeta_MUSIC.dat $folder/ 2> /dev/null
mv test_out.dat $folder/ 2> /dev/null
mv hadron_list.dat $folder/ 2> /dev/null
mv particle_samples.bin $folder/ 2> /dev/null

mv $folder hydro_session/$folder