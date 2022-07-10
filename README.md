# Preparation for the 2022 JETSCAPE School

Please carefully complete **all** of the below instructions **by Friday July 22**.

In case of problems please head to the slack (you can find the link on the indico page) and ask in the `software-install-problems` channel.

Due to a large number of participants and the online format, we will have limited capacity to address 
personal software installation questions during the school — it is therefore imperative to **carefully**
complete the below steps in advance of the school.
If you have any issues or questions, please post on the slack.

## (1) Download school material

We will use code from several git repositories throughout the course of the school,
which you will run in a controlled software environment (docker). 
Create a single directory to store all materials from the school:
```
mkdir jetscape-docker
cd jetscape-docker
```

In what follows we assume such a directory at `~/jetscape-docker`. You may decide to name your directory something else,
but if so **please be careful to substitute your directory name appropriately in the remainder of the instructions**.

Then download several pieces of software from git:
```bash
git clone https://github.com/JETSCAPE/JETSCAPE.git
git clone https://github.com/JETSCAPE/SummerSchool2022.git
git clone https://github.com/JETSCAPE/STAT.git

```

Additionally, download a few external physics packages:
```bash
cd JETSCAPE/external_packages
./get_music.sh
./get_iSS.sh
./get_freestream-milne.sh
./get_lbtTab.sh
```


## (2) Install docker

Docker is a software tool that allows one to deploy an application in a portable environment. 
A docker "image" can be created for the application, allowing any user to run a docker "container" from this image.
We have prepared a docker image for the JETSCAPE environment, which allows you to use JETSCAPE on any operating system without
installing a long list of pre-reqs or worrying about interference with software you already have installed.

To illustrate what this will look like, consider the following standard workflow. 
In a terminal on your machine (call it Terminal 1), you will clone JETSCAPE &mdash; this terminal is on your "host" machine &mdash; 
just a standard, typical terminal. In another terminal (call it Terminal 2), you will invoke a command that runs a pre-defined docker container. 
Terminal 2 then lives entirely inside this docker container, completely separated from your host machine. It can *only* access the files that 
are inside that pre-defined docker container &mdash; and not any of the files on your host machine &mdash; unless we explicitly share a 
folder between them. The standard workflow that we will use is the following: You will share the folder `jetscape-docker` between the 
host machine and the docker container. Then, anytime you want to **build** or **run** JETSCAPE, you *must* do it inside the docker container. 
But anytime you want to edit text files (e.g. to construct your own configuration file), you can do this from your 
host machine (which we recommend). Simple as that: Depending which action you want to do, perform it either on the host machine, 
or in the docker container, as appropriate &mdash; otherwise it will not work.

### Install

#### macOS

1. Install Docker Desktop for Mac: https://docs.docker.com/docker-for-mac/install/
2. Open Docker, go to Preferences --> Resources and 
    1. Set CPUs to one less than the max that your computer has (`sysctl -n hw.ncpu`),
    2. Set memory to what you are willing to give Docker (I use 12 out of 16 GB). It should always be a few GB
       less than the size of you memory.

#### linux

1. Install Docker: https://docs.docker.com/install/
2. Allow your user to run docker (requires admin privileges): 
    ```
    sudo groupadd docker
    sudo usermod -aG docker $USER
    ```
    Log out and log back in.
    
For **Windows**, please follow the analogous instructions: https://docs.docker.com/install/

Please note that if you have an older OS, you may need to download an older version of docker.

### Download the JETSCAPE docker container

The docker container will contain only the pre-requisite environment to build JETSCAPE, but will not actually contain JETSCAPE itself. 
Rather, we will share the directory from step (1) with the docker container. 
This will allow us to build and run JETSCAPE inside the docker container, but to easily edit macros and access the output files on our own machine. 

Create and start the docker container that contains all of the JETSCAPE pre-reqs: 

**macOS:**
```bash
docker run -it -v ~/jetscape-docker:/home/jetscape-user --name myJetscape -p 8888:8888 jetscape/base:stable
```

**linux:**
```bash
docker run -it -v ~/jetscape-docker:/home/jetscape-user --name myJetscape -p 8888:8888 --user $(id -u):$(id -g) jetscape/base:stable
```

**windows:**
For example open a Windows command window using the 'cmd' command then:
```bash
docker run -it -v <fullpath>/jetscape-docker:/home/jetscape-user --name myJetscape -p 8888:8888 jetscape/base:stable
```
where `<fullpath>` would be c:\users\...\documents\ or wherever the `jetscape-docker` folder was placed.

This is what the `docker run` command does:
- `docker run` creates and starts a new docker container from a pre-defined image jetscape/base:stable, which will be downloaded if necessary.
- `-it` runs the container with an interactive shell.
- `-v` mounts a shared folder between your machine (at ~/jetscape-docker) and the container (at /home/jetscape-user), through which you can transfer files to and from the container. You can edit the location of the folder on your machine as you like.
- `--name` (optional) sets a name for your container, for convenience. Edit it as you like.
- `--user $(id -u):$(id -g)` (only needed on linux) runs the docker container with the same user permissions as the current user on your machine (since docker uses the same kernel as your host machine, the UIDs are shared). Note that the prompt will display "I have no name!", which is normal.
- `-p 8888:8888` forwards port 8888 from inside the container to outside.

Some useful commands:
- To see the containers you have running, and get their ID: `docker container ls` (`-a` to see also stopped containers)
- To stop the container: `docker stop <container>` or `exit`
- To re-start the container: `docker start -ai <container>`
- To delete a container: `docker container rm <container>`

Practice exiting and re-entering the docker container:
```
[From inside the container]
exit

[Now we are outside the container]
docker container ls -a
...
docker start -ai myJetscape

[Now we are inside the container again]
```

You may find it useful to keep two terminals open — one inside the docker container, and one outside the container —
so that you can easily execute commands either inside or outside the container, as appropriate.

## (3) Test run of JETSCAPE 

From **inside** the docker container, we can now build JETSCAPE:
```bash
cd JETSCAPE
mkdir build
cd build
cmake ..
make -j4     # Builds using 4 cores; adapt as appropriate
```

*That's it!* You are now inside the docker container, with JETSCAPE and all of its prerequisites installed. 
You can run JETSCAPE executables or re-compile code. Moreover, since we set up the jetscape-docker folder to be shared between your 
host and the docker container, you can do text-editing etc. on your host machine, and then immediately build JETSCAPE in the docker container. 
Output files are also immediately accessible on your host machine if desired.

To test that everything is working, run an example to generate some pp events:
```bash
cd JETSCAPE/build
./runJetscape ../config/jetscape_user_PP19.xml
```

This should take a couple minutes to run, and will print out a variety of information to stdout.
Once done, it will produce a HepMC file test_out.hepmc in the same directory -- success!

## (4) Install ROOT

We will also make use of GUI interactions from time to time. 
This is done most easily directly from your laptop (i.e. not via docker).
Therefore, you should make sure you have a working installation of ROOT on your laptop:
https://root.cern/install/. It is typically easiest to install ROOT via one of the package managers (for macOS
and linux), conda, or else from the pre-compiled binaries.


## (5) Install some missing python packages and test open jupyter notebook through docker

Inside docker container, run
```bash
pip3 install corner pyDOE
pip3 install --upgrade emcee==3.0.2
pip3 install --upgrade seaborn==0.11.0
```
to install some extra python packages needed for the Bayesian part of the school.  The above only needs be done once.

Then...let's try opening the jupyter notebook.

Again when inside docker container, run
````bash
jupyter-notebook --ip 0.0.0.0 --no-browser
````

There will be some printouts, and at the end there will be a URL like

````
http://127.0.0.1:8888/?token=....
````

Copy the full address (including the token) into a web browser, and verify that you can see a jupyter notebook page with directories.

If you are working on a remote machine, we need to forward the correct port, for example

````bash
ssh -L 8888:127.0.0.1:8888 XXX@XXX.XX
````




