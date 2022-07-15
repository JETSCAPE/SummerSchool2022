#!/usr/bin/env bash

folder=$1

echo "collect results into " $folder " ..."

mkdir -p $folder

mv meanpT_estimators_eta_-0.5_0.5.dat $folder/
mv meanpT_estimators_tau_0.64.dat $folder/
mv meanpT_estimators_tau_1.04.dat $folder/
mv eccentricities_evo_ed_tau_0.64.dat $folder/
mv eccentricities_evo_ed_tau_1.04.dat $folder/
mv eccentricities_evo_eta_-0.5_0.5.dat $folder/
mv eccentricities_evo_nB_tau_0.64.dat $folder/
mv eccentricities_evo_nB_tau_1.04.dat $folder/
mv momentum_anisotropy_tau_0.64.dat $folder/
mv momentum_anisotropy_tau_1.04.dat $folder/
mv momentum_anisotropy_eta_-0.5_0.5.dat $folder/
mv inverse_Reynolds_number_eta_-0.5_0.5.dat $folder/
mv surface_MUSIC.dat $folder/
mv evolution_all_xyeta_MUSIC.dat $folder/
mv test_out.dat $folder/
mv hadron_list.dat $folder/
mv particle_samples.bin $folder/