# Hands-on: Hadronic transport approach SMASH

### Goals for this session
1. Learn how to run SMASH within JETSCAPE as a hadronic afterburner
2. Understand SMASH's inputs and outputs
3. Learn how the afterburner affects the event particle spectra

It is strongly advised that you follow the instructions of section 1) before the hands-on session itself, as discussed also at the end of the transport lecture. This is because these instructions take a considerable time to compile and run.

> NOTE: We noticed that the calculations take a considerably longer time for new Macs with the Apple M1 chip. We suspect this is caused by some combination of settings for the JETSCAPE Docker container and the fact that the M1 architecture is unusual, but we haven't had enough time to test this hypothesis and provide a solution. The Apple M1 chip is very fast and ordinarily, SMASH runs very fast on new Macs. If you work on a machine with the M1 chip, please try to run all calculations before the hands-on session. Don't hesitate to ask for help if needed!

If you already have done section 1), you can restart the container for this session by running `docker start -ai JSSMASH` and continue with the hands-on.

Just in case any last-minute changes were made (which is highly likely), update your Summer School folder before doing anything else:

```bash
cd SummerSchool2022
git pull origin main
cd -
```

#### Background and more information on SMASH

SMASH (Simulating Many Accelerated Strongly-interacting Hadrons) is a hadronic transport code. In JETSCAPE, it simulates hadron-hadron scatterings that occur in the final dilute stage of the fireball evolution, and in this role it is often called an afterburner. To get a picture of the microscopic evolution of a medium with hadronic degrees of freedom, have a look at the visualization at the [official SMASH homepage](https://smash-transport.github.io/). As seen in the video, SMASH can be used not only as an afterburner, but also to simulate the entire span of a heavy-ion collision (as long as the collision energy is low enough).

Beyond the webpage, you can find more information on SMASH in the [Github repository](https://github.com/smash-transport/smash), in the [User Guide](https://theory.gsi.de/~smash/userguide/current/), and in the detailed [development documentation](http://theory.gsi.de/~smash/doc/current/). The main publication of SMASH is [Phys. Rev. C 94, 054905 (2016)](https://arxiv.org/abs/1606.06642)



## 1) Compile and run JETSCAPE with SMASH

#### Already done?

The following instructions assume that you have followed the initial steps from the [school's main README](https://github.com/JETSCAPE/SummerSchool2022/blob/main/README.md). You should have cloned the JETSCAPE and SummerSchool2022 repository in a directory called `jetscape-docker`. So when you run `ls` inside this directory, it looks like this:

```bash
~/jetscape-docker $ ls
JETSCAPE		STAT			SummerSchool2022
```

Note that the following examples assume that `jetscape-docker` is placed in the home directory (`~`). If you placed it in a different directory, substitute the path accordingly in the following.

To perform hydro calculations, we need to have access to a hydrodynamics ( music ) package and a particlization ( iSS ) package. Actually, you should have already downloaded both, either during the installation of JETSCAPE or during the hydro session, by running from within `jetscape-docker`

```
cd JETSCAPE/external_packages
./get_music.sh
./get_iSS.sh
```

To be sure, you can check that `ls` shows a `music` and `iSS` directory (among others).


#### Starting the docker container

The first step you need to do for this hands-on is to start a new docker container `JSSMASH`, which is done in the usual way (on macOS):

```
docker run -it -v ~/jetscape-docker:/home/jetscape-user --name JSSMASH jetscape/base:stable
```

On Windows, make sure to replace `~/jetscape-docker` with the full path. On Linux, in order to have the correct write permission to e.g. create directories you have to include the command line option `--user $(id -u):$(id -g)`, so the full command is

```
docker run -it -v ~/jetscape-docker:/home/jetscape-user --user $(id -u):$(id -g)` --name JSSMASH jetscape/base:stable
```

#### Downloading SMASH

To perform afterburner calculations with JETSCAPE, we now download SMASH from within the container:

```
cd JETSCAPE/external_packages/
./get_smash.sh
```

This getter script not only clones SMASH, but also takes care of compiling it as a shared library for JETSCAPE. On my Macbook from 2018 with 4 docker cores, this took about **4 mins**. (Note: we noticed that this can take a considerably longer times on new Macs with the Apple M1 chip.)


#### Compiling JETSCAPE with SMASH

To compile JETSCAPE with SMASH as the afterburner, MUSIC as the hydro module, and iSS to particlize, we go in the build directory and run

```
cd ~/JETSCAPE
mkdir -p build
cd build
cmake -DUSE_MUSIC=ON -DUSE_ISS=ON -DUSE_SMASH=ON ..
make -j4  # builds using 4 cores; adapt as appropriate
```

On my Macbook from 2018 with 4 docker cores, this took about **12 mins**. (We noticed that this can take a considerably longer times on new Macs with the Apple M1 chip.)

With this you are set to run JETSCAPE with SMASH.



#### Running JETSCAPE with SMASH

As later we will want to look at the collision output from SMASH (we will further explain this below), we need to create a `smash_output` directory inside the `build` directory:

```
cd ~/JETSCAPE/build
mkdir smash_output
```

Note: SMASH will only write to its own output (in addition to the JETSCAPE output) if this directory exists.

To produce the collision output, you have to request it in the SMASH config file. Open the `smash_config.yaml` file in the `~/SummerSchool2022/Jul28_Transport` directory. As shown below, search for the `Output` section and add a `Collisions` output section to the `Particles` output that is already there. In the end, the `Output` section should look like below. Be careful that the indentation is the same everywhere. (Note: some editors will substitue tabs for indentations composed out of series of blank spaces. Make sure this is not the case, as a configs with tab spaces will fail.)

```yaml
Output:
    Output_Interval:  5.0
    Particles:
        Format:          ["Oscar2013", "Binary"]
    Collisions:
        Format:          ["Oscar2013", "Binary"]
```

Now, you can start a JETSCAPE simulation with SMASH (from the `build` directory). With the following:

```
cd ~/JETSCAPE/build
./runJetscape ../../SummerSchool2022/Jul28_Transport/jetscape_user_smash.xml
```

We will run a Au-Au collision at sqrts = 200 GeV and 0-5% centrality. We will simulate one hydro event, and then we will sample discrete particles from the obtained hydro surface and evolve them within the SMASH afterburner; we will repeat the sampling 25 times, so that in the end we will have 25 hydro+afterburner events. All these options (and others) are specified in the given `jetscape_user_smash.xml` file.

While the calculation is running (it will take around 20 minutes), we have a look at the input, configuration, and output of SMASH.

> NOTE: This calculation takes a CONSIDERABLY longer time for new Macs with the Apple M1 chip: around 8 hours!

> Note: You will also see some warnings like `[Warning] bool Jetscape::Hadron::CheckOrForceHadron(int, double) ...`. You do not need to worry about them.



## 2) Input and output files of SMASH

#### Input

As usual for JETSCAPE modules, you can configure properties of the module in the JetScape configuration file `SummerSchool2022/Jul28_Transport/jetscape_user_smash.xml`. Open the file, have a look, and find the Hadronic Afterburner section. There you can see the three input files of SMASH: the config, particles, and decaymodes file. Locate those files and open them to see what are their functions:

* The `config.yaml` file gives you all options to alter the setup of SMASH. When SMASH is used within JETSCAPE, some of them are automatically overwritten (for this reason, we marked them here as "dummy variables"). The options are described in detail in the [SMASH user guide](http://theory.gsi.de/~smash/userguide/current/).
* The `particles.txt` file lists all possible degrees of freedom (i.e. hadrons) with their properties. Hint: this file can be very useful for "translating" the pdg numbers of particle species, and we will use that fact below.
* The `decaymodes.txt` file lists the possible decays of resonances in SMASH.

All of these files can be freely edited without recompiling the code, although today we will only edit the `config.yaml` file. Editing the other two may be useful, for example, if you want to study resonance production and dynamics, since you can freely vary branching ratios of decays for a given resonance, add or remove decaymodes, or limit your calculation to certain particle species by removing unwanted particle species from the list.


#### Output

##### SMASH outputs

SMASH has two main output contents: a list of particles (with their selected fundamental properties, such as charge, as well as positions and momenta that are specific to a given simulation) and a list of all interactions (collisions and decays). If your JETSCAPE run went as planned, you should find 4 files in the `smash_output` directory (which is itself in the `build` directory):

```
collisions_binary.bin
full_event_history.oscar  
particle_lists.oscar  
particles_binary.bin
```

The OSCAR format (`*.oscar` files) is a human-readable text output, while the binary format (`*.bin` files) is a smaller binary output that is not human-readable. Both contain the same information. If your calculation is already finished, you can go ahead and open the two OSCAR files in `~/JETSCAPE/build/smash_output` yourself. If not, you can just read on and look at the examples below.

If you open the `particle_lists.oscar` file, it looks like the excerpt shown below. The first line tells you what each value means (first value = t, second value = x and so on). Here, you get a list of all final hadrons (that is, all hadrons and their positions and momenta at the last time step of the simulation, t = 300 fm/c) for each event. It is also possible to save in the output the information on all hadrons at specified times during the simulation, but we will not use this today.

```
#!OSCAR2013 particle_lists t x y z mass p0 px py pz pdg ID charge
# Units: fm fm fm fm GeV GeV GeV GeV GeV none none e
# SMASH-2.2
# event 0 out 11537
300 -52.7671 58.0999 276.454 0.138 0.507409192 -0.0884423711 0.109450186 0.467566778 -211 0 -1
300 52.9803 52.7448 -288.923 0.138 2.92511924 0.557319744 0.531497917 -2.81854275 -211 15816 -1
300 -27.4531 20.54 -297.485 0.138 4.32975482 -0.34054657 0.394098553 -4.29609673 111 19666 0
300 113.582 120.583 199.725 1.116 2.32783453 0.864583053 0.950283431 1.58833723 3122 17346 0
300 51.3578 -123.028 265.351 0.138 1.48967666 0.274295276 -0.625890296 1.31647863 211 15209 1
300 -0.386508 5.77741 -299.932 0.138 18.0283727 -0.369376468 -0.0698212672 -18.0239248 -211 5 -1
(...)
```

The `full_event_history.oscar` file looks like the excerpt shown below. The lines containing information on interacting particles have the same structure as in `particle_lists.oscar` file shown above, but they are separated into individual interaction sections that show which particles have interacted and how. Below you see two decays (`1 out 2`) and one resonance formation (`2 out 1`) for example. The file includes the full record of all interactions for each event.

```
#!OSCAR2013 full_event_history t x y z mass p0 px py pz pdg ID charge
# Units: fm fm fm fm GeV GeV GeV GeV GeV none none e
# SMASH-2.2
# interaction in 1 out 2 rho    0.0000000 weight        0.095 partial    0.0090476 type     5
2.24647 8.18392 0.830245 -0.347499 1.83 2.39031262 1.25830883 -0.841468736 0.270709597 13126 8199 0
2.24647 8.18392 0.830245 -0.347499 1.189 1.50710769 0.920800885 -0.0947209957 -0.0283943303 3112 8241 -1
2.24647 8.18392 0.830245 -0.347499 0.138 0.883204936 0.337507943 -0.74674774 0.299103927 211 8242 1
# interaction in 1 out 2 rho    0.0000000 weight        0.054 partial    0.0180000 type     5
2.33223 -8.27632 -0.0970725 -1.37989 1.4264 3.44810737 -1.54663378 1.53759445 -2.25799794 20333 7940 0
2.33223 -8.27632 -0.0970725 -1.37989 0.138 1.796057 -0.89200515 1.04065007 -1.15245433 111 8243 0
2.33223 -8.27632 -0.0970725 -1.37989 0.911894 1.65205037 -0.654628634 0.496944372 -1.10554361 9000111 8244 0
# interaction in 2 out 1 rho    0.0000000 weight     20.19796 partial   15.1670382 type     2
2.41436 -8.51664 0.433705 0.999834 0.138 0.762386501 -0.509557728 -0.418497157 0.356931687 -211 1005 -1
2.41436 -8.12277 0.23413 0.973492 0.138 0.279774825 -0.0738591326 0.124533528 0.195617437 111 2846 0
2.41436 -8.3197 0.333918 0.986663 0.594979 1.04216133 -0.583416861 -0.293963628 0.552549123 -213 8245 -1
(...)
```

> Sidenote: There are also more specialized SMASH outputs like HepMC or a thermodynamic output. You can find more details [in the Output section of the User guide](http://theory.gsi.de/~smash/userguide/2.2/output_general_.html).



##### JETSCAPE output

The official JETSCAPE output `test_out.dat` contains the same information as the particle lists output in the section with the heading `# JetScape module: SMASH`. In this hands-on we will exclusively use the SMASH binary output. This is convenient as we can use existing analysis script infrastructure from the SMASH Analysis Suite, [available on Github](https://github.com/smash-transport/smash-analysis). You could naturally recreate the following pT analysis just as well with the `test_out.dat` file (or the SMASH OSCAR output). For an analysis of the scattering history, however, you always need to turn to the collision output of SMASH.


## 3) Effect of the afterburner rescattering stage

To illustrate one of the effects that rescattering has on final observable hadrons, in this session we focus on the transverse momentum spectra (pT) and, later, analyze the collision history. For this, we first have to analyze the particles output and create particle spectra. Follow the instructions below in the command line to produce them.


#### Quick example analysis of multiplicities

```sh
cd ~/JETSCAPE/build

# Let's set an alias for the transport school folder for convenience; the whole section will assume this variable to be set.
# Note: if you stop your container in between, you need to reset it
export TRANSPORT_FOLDER="../../SummerSchool2022/Jul28_Transport/"

# As a first simple example analysis, we output the particle multiplicities per event of given species of
# particles: Pions, Kaons, and Protons. You are free to replace them in the argument in order to see the output for other species
# (best by copying other hadron names as they are listed in the particles.txt)
python ${TRANSPORT_FOLDER}/quick_mul_count.py p,π⁻,K⁺ ${TRANSPORT_FOLDER}/dummy_config.yaml  smash_output/particles_binary.bin
```

**Question 1**: What hadron species dominate the medium?

Note that the three particle species that we chose to look at already contain the most abundant stable hadrons, as they are the lightest stable non-strange meson, strange meson, and non-strange baryon.

> You can find the answers to the questions below.



#### Analysis of the pT of final hadrons

```sh
python ${TRANSPORT_FOLDER}/anl_pt.py p,π⁻,K⁺ smash_output/particles_binary.bin results_with_rescattering ${TRANSPORT_FOLDER}/dummy_config.yaml
```
This script outputs the average pT value of the given particle species to the command line (`p,π⁻,K⁺`). After the run you should find analysis output files for the pT of each species in the directory `results_with_rescattering` within `~/JETSCAPE/build`. Those files have the average pT value and a pT histogram in it.

We can a have first look at the results, by plotting them as follows:

```sh
 python ${TRANSPORT_FOLDER}/plot_pt.py results_with_rescattering ${TRANSPORT_FOLDER}/dummy_config.yaml
```

You will find a `pt_spectra.pdf` and a `pt_avg.pdf` plot in the `build` directory of JETSCAPE. Open them and have a look.

**Question 2**: Can you deduce, based on looking at the spectra, how the mean transverse mass has to be ordered for the different species? For example, which species has to have the largest mean pT?


#### Run SMASH without rescattering and with only decays

As we want to study the effect of the afterburner, we need a calculation to compare with that does not include rescattering.

For this, we first save our previous SMASH output for later, as otherwise it will get overwritten by the new calculation (this is in the `JETSCAPE/build` folder):

```
mkdir smash_output_with_rescattering
cp smash_output/* smash_output_with_rescattering/
```

To disable all hadron collisions and only allow decays within SMASH, we change the used config file `~/SummerSchool2022/Jul28_Transport/smash_config.yaml`. You can search for the right option yourself in the [SMASH user guide](http://theory.gsi.de/~smash/userguide/current/). Hint: Click on the arrow to expand Input, then Configuration, and then click on Collision Term. Look for the relevant option there. If you are lazy (which is also fine :wink:), you can also just click below for the solution.

<details><summary><b> Click for Solution </b></summary>
<p>
You need to change the config so that it includes the following section:

```yaml
Collision_Term:
    No_Collisions: True
```
This disables all interactions except decays.
</p>
</details>

After making the appropriate changes in the config file, run JETSCAPE with SMASH again by executing

```sh
./runJetscape ../../SummerSchool2022/Jul28_Transport/jetscape_user_smash.xml
```

It will run faster this time as no collisions (which are computationally very expensive) are happening.

> This calculation takes a CONSIDERABLY longer time for new Macs with the Apple M1 chip: around 1 hour!

> Note that running SMASH in such a setup is equivalent to just using a particlization module like ISS after the hydro evolution and letting it take care of the resonance decays. Moreover, for this specific setting, there is also an option in the JETSCAPE xml that achieves the same: one would set `<only_decays> 1 </only_decays>` in the <SMASH> section. As you will change the xml throughout the school exercises frequently, here we want to make that you are also familiar with changing the SMASH config.


#### Comparing the pT spectra with and without rescattering stage

With our second run finished, we can plot the comparison, after running the analysis again, as follows:

```sh
# Analyze results without rescattering
python ${TRANSPORT_FOLDER}/anl_pt.py p,π⁻,K⁺ smash_output/particles_binary.bin results_wo_rescattering ${TRANSPORT_FOLDER}/dummy_config.yaml

# Plotting a comparison
python ${TRANSPORT_FOLDER}/plot_pt.py results_with_rescattering,results_wo_rescattering ${TRANSPORT_FOLDER}/dummy_config.yaml
```

First, look at the pT spectra plot.

**Question 3**: Can you notice something particular about the shape of the spectra (even though the statistics is limited)? Can you confirm you observation with the mean pT plot?


#### Investigate the scattering of protons

To see how the transverse momentum of protons is modified in the late rescattering stage, we can make use that transport approaches evolve the system microscopically. We can look at the microscopic scattering history of protons for this whole phase.

To do that, we can analyze the collision output of the first calculation we ran (the one with enabled rescattering). As a starting point, you can run the script `anl_proton_reactions.py` as shown below, which will print out all proton reaction partners in the different events as well as the number of total proton reactions.

```sh
python ${TRANSPORT_FOLDER}/anl_proton_reactions.py smash_output_with_rescattering/collisions_binary.bin
```

The numbers printed out are pdg numbers, which you can translate using the `particles.txt` file in the `~/SummerSchool2022/Jul28_Transport` directory.

Simply printing out the scattering partner pdgs is surely not very useful. Therefore, as the last part of this hands-on, it is your turn to investigate the scatterings of the protons a bit more. Think: How you could investigate the proton scatterings to learn more about what influences them, and in what way?

For this, take a look at the script and modify it according to your idea. Hint: Some properties of the scattering are already extracted but not yet used in the script. For example, you could count how often the proton scatters with a certain particle species, what type of scatterings occur most often, or what the outgoing products of the scatterings are.

If you are not familiar with python, you can also tell us about your idea and we will try to help you implement it.

This last step of the hands-on is more of an open question for you to explore. We are interested to learn your ideas.

***

### Answers to questions to check yourself

<details><summary><b>1. What hadron species dominates the medium? </b></summary>
<p>
Pions
</p>
</details>

<details><summary><b>2. Can you deduce, based on looking at the spectra, how the mean transverse mass has to be ordered for the different species? </b></summary>
<p>
Higher mean transverse mass leads to flatter spectra.
</p>
</details>

<details><summary><b>3. Can you notice something particular about the shape of the spectra (even though the statistics is limited)? Can you confirm you observation with the mean pT plot? </b></summary>
<p>
**The main result of this session: Mean pT of protons increases significantly (by around 30%) due to the afterburner rescattering stage.** This can also be seen as a flattening of the proton pT spectrum.
</p>
</details>
