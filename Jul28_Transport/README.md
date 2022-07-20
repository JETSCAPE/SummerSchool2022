## Hands-on: Hadronic transport approach SMASH

### Goals for this session
1. Learn how to run SMASH within JETSCAPE as a hadronic afterburner
2. Understand SMASH's in- and outputs
3. Learn how the afterburner effects the resulting spectra

If you have time before the session itself, it would be perfect, if you follow the instructions of section 1, since those take some time to compile and run.

<!-- ## Brief physics background on SMASH

See also lecture from yesterday. SMASH can also be used on its own for low-energy collisions. -->


#### Details and references for SMASH

A complete User Guide can be found [here](https://theory.gsi.de/~smash/userguide/current/). For a more
detailed development documentation, see
[here](http://theory.gsi.de/~smash/doc/current/).


### 1) Compile and run JETSCAPE with SMASH

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

To perform hydro calculations, we also need to download a hydro and a particlization package. At the latest, for the previous hydro session, you should have downloaded both by running within `jetscape-docker`

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

The getter script not only clones SMASH, but also takes care of compiling SMASH as shared library for JETSCAPE. On my Macbook from 2018 with 4 docker cores, this took about **4 mins**.

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


While the calculation is running, we have a look at the input, configuration and output of SMASH.

### 2) Input and output files of SMASH

#### Input

As usual for JETSCAPE modules, you can configure properties of the module in the JetScape configuration file `SummerSchool2022/Jul22_Transport/jetscape_user_smash.xml`. Open it, have a look and find the Afterburner section. There you see the three input files of SMASH the config, particles and decaymodes file. Locate those file and open them to see what they are about:

* The config file gives you all options to alter the setup of SMASH. When SMASH is used within JETSCAPE some of them are overwritten (dummy variables). The options are described in detail in [SMASH user guide](http://theory.gsi.de/~smash/userguide/current/).
* The particles file list all possible degrees of freedom (i.e. hadrons) with their properties, which is for example useful to look up the PDG number of particles.
* The decaymodes file list the possible decays of resonances in SMASH.

The last two files can be in principle freely edited without recompiling the code, even though we will not do this today. This is useful when you, for example, study resonance production
and want to vary branching ratios into of decays into this resonance, or
of decays of the resonance.



#### Output

_TBD_


### 3) Effect of a afterburner rescattering stage


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



> Note that running SMASH in such a setup is equivalent to just having a particlization modules like ISS and let it take care of the resonance decays. Additionally, for this specific setting, there is also a option in the JETSCAPE xml that achieves the same: For this one would set `<only_decays> 1 </only_decays>` in the <SMASH> section. As you will change the xml through-out the school frequently, the idea here is to get familiar with changing the SMASH config as well.

#### Comparing the pt spectra with and without rescattering stage

With our second run finished, we can plot the comparison after analizing again as follows.

```sh
# Analyze results without rescattering
python ${TRANSPORT_FOLDER}/anl_pt.py p,π⁻,K⁺ smash_output/particles_binary.bin results_wo_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml

# Plotting a comparison
 python ${TRANSPORT_FOLDER}/plot_pt.py results_with_rescatt,results_wo_rescatt ${TRANSPORT_FOLDER}/dummy_config.yaml
```

Look first at the pT spectra plot. **Answer**: What do you notice? Can you confirm you observation withe mean pT plot?



<!--

### Analysis Steps
4. Look at scatterings proton (More open question)

### Notes

* Check that JETSCAPE outputs are the same by comparing line numbers of test output and smash output (we use binary smash output as we have nice scripts taken from analysis suite)


-->
