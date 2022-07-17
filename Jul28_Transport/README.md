## Hands-on: Hadronic transport approach SMASH

### Goals for this session
1. Learn how to run SMASH within JETSCAPE as a hadronic afterburner
2. Understand SMASH's in- and outputs
3. Learn how the afterburner effects the resulting spectra

If you have time before the session itself, it would be perfect, if you follow the instructions of section 1, since those take some time to compile and run.

<!-- ## Brief physics background on SMASH

See also lecture from yesterday. SMASH can also be used on its own for low-energy collisions.


### Future references for SMASH -->


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


_Further instructions: TBD._

<!-- #### Running JETSCAPE with SMASH


While the calculation is running, we have a look at the SMASH inputs and configuration.

### 2) SMASH's in- and outputs

### 3) Afterburner effects on spectra -->
