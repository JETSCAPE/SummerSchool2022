## Hands-on: Hadronic transport approach SMASH

### Goals for this session
1. Learn how to run SMASH within JETSCAPE as a hadronic afterburner
2. Understand SMASH's in- and outputs
3. Learn how the afterburner effects the resulting spectra

If you have time before the hands-on session itself, it would be perfect, if you follow the instructions of section 1), since the instructions there take some time to compile and run.

#### Background and more information on SMASH

SMASH is a hadronic transport code. In JETSCAPE it simulates multiple hadron-hadron scatterings
in the final dilute stage of the fireball evolution as so called afterburner. To get a picture of the microscopic evolution of the hadronic medium, have a look at the visualization at the [official SMASH homepage](https://smash-transport.github.io/). As seen in the video, SMASH can also be used on its own for lower energy collisions.

Apart from the webpage, you find more information on SMASH in the [Github repository](https://github.com/smash-transport/smash), in the [User Guide](https://theory.gsi.de/~smash/userguide/current/) and in the detailed [development documentation](http://theory.gsi.de/~smash/doc/current/). The main publication of SMASH is [Phys. Rev. C 94, 054905 (2016)](https://arxiv.org/abs/1606.06642)


## 1) Compile and run JETSCAPE with SMASH

#### Already done?

The following instructions assume that you have followed the initial steps from the [school's main README](../README). You should have cloned the JETSCAPE and SummerSchool2022 repository in a directory called `jetscape-docker`. So when you run `ls` inside this directory, it looks like this:

```bash
~/jetscape-docker $ ls
JETSCAPE		STAT			SummerSchool2022
```

Note that the following examples assume that `jetscape-docker` is placed in the home directory (`~`). If you placed it in the directory substitute the path accordingly in the following.

Just in case update your Summer School folder

```bash
cd SummerSchool2022
git pull origin main
cd -
```

To perform hydro calculations, we also need to download a hydro and a particlization package. At the latest, for the previous hydro session, you should have downloaded both by running from within `jetscape-docker`

```
cd JETSCAPE/external_packages
./get_music.sh
./get_iSS.sh
```

You can check that `ls` shows a `music` and `iSS` directory among others.

#### Starting the docker container

Before we download and compile SMASH, we start a docker container in the usual way

```
docker run -it -v ~/code/SummerSchool2022-test-dir/jetscape-docker:/home/jetscape-user --name JSSMASH jetscape/base:stable
```

> You should be able to restart the school's myJetscape or the previous sessions JSHYDRO container by running `docker start -ai myJetscape` or `docker start -ai JSHYDRO`

#### Downloading SMASH

To perform afterburner calculation within JETSCAPE, we now download SMASH from within the container.

```
cd JETSCAPE/external_packages/
./get_smash.sh
```

The getter script not only clones SMASH, but also takes care of compiling it as a shared library for JETSCAPE. On my Macbook from 2018 with 4 docker cores, this took about **4 mins**.

#### Compiling JETSCAPE with SMASH

To compile JETSCAPE with SMASH, MUSIC as the hydro module and iSS to particlize, we go into the build directory and run

```
cd ~/JETSCAPE
mkdir -p build
cd build
cmake -DUSE_MUSIC=ON -DUSE_ISS=ON -DUSE_SMASH=ON ..
make -j4  # builds using 4 cores; adapt as appropriate
```

On my Macbook from 2018 with 4 docker cores, this took about **12 mins**. With this you are set to run JETSCAPE with SMASH.

#### Running JETSCAPE with SMASH

As we later one want to look at the collision output from SMASH, we need to create a `smash_output` directory inside the `build` directory.

```
cd ~/JETSCAPE/build
mkdir smash_output
```

Note: SMASH will only write to its own output in addition to the JETSCAPE output, if this directory exists.

To produce the collision output, you have to add it the SMASH config file. Look for output section in the `smash_config.yaml` file in the `Jul28_Transport` directory. Add a `Collisions` section in the same way a particles section is already there. In the end, the section should look like this. Be careful that the indentation is the same everywhere.

```
Output:
    Output_Interval:  5.0
    Particles:
        Format:          ["Oscar2013", "Binary"]
    Collisions:
        Format:          ["Oscar2013", "Binary"]

```

Now, you can start the JETSCAPE run with SMASH

```
./runJetscape ../../SummerSchool2022/Jul28_Transport/jetscape_user_smash.xml
```


While the calculation is running (it will take around 20 minutes), we have a look at the input, configuration and output of SMASH.

## 2) Input and output files of SMASH

#### Input

As usual for JETSCAPE modules, you can configure properties of the module in the JetScape configuration file `SummerSchool2022/Jul22_Transport/jetscape_user_smash.xml`. Open it, have a look and find the Afterburner section. There you see the three input files of SMASH the config, particles and decaymodes file. Locate those file and open them to see what they are about:

* The `config.yaml` file gives you all options to alter the setup of SMASH. When SMASH is used within JETSCAPE some of them are overwritten (dummy variables). The options are described in detail in the [SMASH user guide](http://theory.gsi.de/~smash/userguide/current/).
* The `particles.txt` file list all possible degrees of freedom (i.e. hadrons) with their properties, which is for example also useful to look up the PDG number of particles.
* The `decaymodes.txt` file list the possible decays of resonances in SMASH.

The last two files can be in principle freely edited without recompiling the code, even though we will not do this today. This is useful when you, for example, study resonance production and want to vary branching ratios into of decays into this resonance, or of decays of the resonance.


#### Output

##### SMASH outputs

SMASH has two main output contents: a list of particles and a list of all interactions. If your JETSCAPE run went as planned you will have 4 files in the `smash_output` directory at the end.

```
collisions_binary.bin
full_event_history.oscar  
particle_lists.oscar  
particles_binary.bin
```

The OSCAR format (`*.oscar` files) is a human-readable text output, the binary format is a smaller binary output (`*.bin` files), but they are not human-readable. Both contain the same information. If your calculation is already finished, you can go ahead and open the two OSCAR files in `~//ETSCAPE/build/smash_output` yourself. If not you can just read on and look at the examples below.

If you open the `particle_lists.oscar` file, it looks like shown below. The first line tells you what each value means (first value = t, second value = x and so on). You get the a list of all final hadrons for each event. It is also possible to print out the list of hadrons over time, but we will not use this today.

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

The `full_event_history.oscar` file looks like shown below. The particles line are the same, but they are included in interaction sections that show what and how particles have interacted. Below you see t2 decays (`1 out 2`) and one resonance formation (`2 out 1`). The file includes the full record of all interactions for each event.

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

> Sidenote: There are also more specialized SMASH outputs as you can see [in the Output section of the User guide](http://theory.gsi.de/~smash/userguide/2.2/output_general_.html).


##### JETSCAPE output

The official JETSCAPE output `test_out.dat` contains the same information as the particle lists output. In the `# JetScape module: SMASH` section. In this hands-on, we use for convenience the SMASH binary output as we can use some nice existing script from the SMASH Analysis Suite, which is is also [available on Github](https://github.com/smash-transport/smash-analysis). You could recreate the following pt analysis just as well with the `test_out.dat` file. For analysis of the scattering history, you need to turn to the collision output of SMASH.


## 3) Effect of a afterburner rescattering stage


To illustrate one effect that rescattering has on the final observable hadrons, we focus in this session on the transverse momentum spectra (pT) and latter analyze the collision history. For this we first have to analyze the particles output and create our spectra. Follow the instructions below in the command line to produce them


#### Quick test analysis of multiplicities

```sh
cd ~/JETSCAPE/build

# Let's set the transport school folder for convienence
export TRANSPORT_FOLDER="../../SummerSchool2022/Jul28_Transport/"

# As a first simple test analysis, we output the particle multiplicities per event of some
# particles (Pions, Kaons, Protons). You are free to replace them in the argument
# (best by copying other hadron names from the particles.txt)
python ${TRANSPORT_FOLDER}/quick_mul_count.py p,π⁻,K⁺ ${TRANSPORT_FOLDER}/dummy_config.yaml  smash_output/particles_binary.bin
```

**Answer**: What hadron species dominate the medium? Note that the three given species are already the most abundant stable hadrons as they are the lightest stable non-strange meson, strange meson and non-strange baryon.

#### Analyze pt of final hadrons

```sh
python ${TRANSPORT_FOLDER}/anl_pt.py p,π⁻,K⁺ smash_output/particles_binary.bin results_with_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml
```
This script outputs the average pt value of the given particles species to the command line (the numbers are the integer pdg values of the particles) and you should find in the directory `results_with_rescatt` analysis output files for the pT for each species that has the average pt value and a pt histogram in it.

We can a have first look at the results, by plotting as follows

```sh
 python ${TRANSPORT_FOLDER}/plot_pt.py results_with_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml

```

You find a `pt_spectra.pdf` and a `pt_avg.pdf` plot in the build directory of JETSCAPE. Open them and have look.

**Answer**: Can you already decide from looking at the spectra, how the mean transverse mass has to be ordered for the different species? If yes, how?


#### Run SMASH without rescattering and with only decays

As we want to see the effect of the afterburner, we need a calculation to compare to that does not inlcude the effect of rescattering.

For this, we first save our SMASH output for latter, as it will get overwritten by the new calculation

```
mkdir smash_output_with_rescatt
cp smash_output/* smash_output_with_rescatt/
```

To disable all hadron collisions and only allow decays within SMASH, we change the used config file that is found here `~/SummerSchool2022/Jul28_Transport/smash_config.yaml`. If you are motivated, you can search for the right option yourself [SMASH user guide](http://theory.gsi.de/~smash/userguide/current/). Hint: Click on the arrow to expand Input, then Configuration and then click on Collision Term. Look for the option there.

<details><summary><b> Click for Solution </b></summary>
<p>
You need to add or change the config to include the following section

```yaml
Collision_Term:
    No_Collisions: True
```
This disables all interactions except decays.
</p>
</details>

Re-run SMASH after changing the config accordingly by  again executing

```sh
./runJetscape ../../SummerSchool2022/Jul28_Transport/jetscape_user_smash.xml
```

It will run much faster this time as no collisions are happening.

> Note that running SMASH in such a setup is equivalent to just having a particlization modules like ISS and let it take care of the resonance decays. Additionally, for this specific setting, there is also a option in the JETSCAPE xml that achieves the same: For this one would set `<only_decays> 1 </only_decays>` in the <SMASH> section. As you will change the xml through-out the school frequently, the idea here is to get familiar with changing the SMASH config as well.

#### Comparing the pt spectra with and without rescattering stage

With our second run finished, we can plot the comparison after analizing again as follows.

```sh
# Analyze results without rescattering
python ${TRANSPORT_FOLDER}/anl_pt.py p,π⁻,K⁺ smash_output/particles_binary.bin results_wo_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml

# Plotting a comparison
python ${TRANSPORT_FOLDER}/plot_pt.py results_with_rescatt,results_wo_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml
```

Look first at the pT spectra plot. **Answer**: Even though statistics is limited, what do you notice, in particular about the shape of the spectra? Can you confirm you observation withe mean pT plot?


#### Investigate the scattering of protons

To see how the protons transverse momentum is effected in the late, rescattering stage, we can look at at the microscopic scattering history of the protons in this phase.

To do that we can analyze the collision output of the first calculation with SMASH. As a starting point, you can run the script `anl_proton_reactions.py`, which will print out all proton reaction partners in the different events and the number of total proton reactions.

```sh
python ${TRANSPORT_FOLDER}/anl_proton_reactions.py smash_output_with_rescatt/collisions_binary.bin
```

The printed out numbers are pdg numbers, you can translate them with the particles.txt file in the `SummerSchool2022/Jul28_Transport` directory.

Just printing out the scattering partner pdgs is surely not very useful. Therefore, as the last part of this hands-on, it is your turn to investigate the scatterings of the protons a bit more. Think yourself about how you would investigate the proton's scatterings to learn more how and what influences them.

For this, take a look at the script and modify it according to your idea. Some properties of the scattering are already extracted but not yet used in the script.

For example, you could count how often the proton scatters with a certain particle species, what type of scatterings occur or what the outgoing products of the scatterings are. If your not familiar with python, you can also tell us your idea and we can try to help you with it.

This last step of the hands-on is on purpose more an open question for you to explore. We are interested to learn your ideas.
