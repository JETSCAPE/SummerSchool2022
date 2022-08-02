# Bayesian parameter estimation Overview

### For sessions on Aug 03, 2022

1. Most of the dependencies are already provided by the jetscape docker. For exercises on Aug. 2 and 3, you may need to install some packages by running the following from the jetscape docker:

```bash
pip3 install Gpy
pip3 install ptemcee
```

For Aug 3, download the pregenerated datafiles 

```bash
./get_data.sh
```

2. Since the materials is quite dense, please make sure before the hands-on session that all modules and essential data files can be loaded properly.
To do so, run the jupyter notebook from the jetscape docker as instructed in the main README

```bash
jupyter-notebook --ip 0.0.0.0 --no-browser
```

and then open this notebook 

```bash
Bayesian Parameter Estimation for Relativistic Heavy Ion Physics.ipynb
```

Try if you can run through the first few blocks which loads all necessary packages and the pregenerated emulator files. Please post on slack if you encounter any problems.


### Binder option

Since these exerercise only involves the jupyter notebook, we also provide the option to run it online, hosted by Binder. If you have difficulties with docker, you can simply go to the following link

[https://mybinder.org/v2/gh/keweiyao/JS22-binder/HEAD](https://mybinder.org/v2/gh/keweiyao/JS22-binder/HEAD)

It will take sometime to load the image and then you will see the jupyter-lab interface.

1. On the right panel, click the terminal icon to open a terminal, then download data and install ptemcee

```bash
./get_data.sh
pip3 install ptemcee
```

2. Go back to the left panel and click to start the notebook "Bayesian Parameter Estimation for Relativistic Heavy Ion Physics.ipynb".

3. However, do not try to run anything computational intensive on binder. It takes forever...
