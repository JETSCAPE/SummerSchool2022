# Bayesian parameter estimation code for Relativistic Heavy Ion Collisions

This exercise is modified from JETSCAPE Summer School 2021. It provides pre-generated bulk observables (both design and validation) used in the JETSCAPE publications [PRL126(2021)242301](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.126.242301) and [PRC103(2021)054904](https://journals.aps.org/prc/abstract/10.1103/PhysRevC.103.054904). We will use these data to go over a full-scale Bayesian analysis and obtain the posterior distribution of shear and bulk viscosity by calibrating JS simulations to bulk observables in Pb-Pb collisions at 2.76 TeV. 

We have provided pre-generated data for the time-consuming parts (MCMC, computation of design observables, etc). We will emphasize 1) the importance of prior distribution 2) using emulator and PCA to assist the complex model analysis 3) validation of the workflow 4) the understanding of the posterior in terms of information gain.

### For sessions on Aug 03, 2022

1. Once you pull from the summer-schoool repository again, you will see the folder Aug03_BulkBayes. Go to this folder and run

```bash
./get_data.sh
```

to download the pregenerated data files.


2. Most of the dependencies are already provided by the jetscape docker. For exercises on Aug02, you may need to install Gpy by running the following from the jetscape docker:

```bash
pip3 install Gpy
```

3. Since the materials is quite dense, please makesure before the hands-on session that all modules and essential data files can be loaded properly.
To do so, run the jupyter notebook from the jetscape docker as instructed in the main README, and then open this notebook 

```bash
Bayesian Parameter Estimation for Relativistic Heavy Ion Physics.ipynb
```

Try if you can run through the first few blocks which loads all necessary packages and the pregenerated emulator files. Please post on slack if you encounter any problems.

4. You are encouraged to do a first pull this weekend to test the dependencies. We will do another pull right before Aug03 just in case there are updates (without changing any dependencies).


