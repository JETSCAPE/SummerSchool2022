#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.core.display import display, HTML

#display(HTML("<style>.container {width:90% !important;}</style>"))


# In[2]:


#get_ipython().run_line_magic('matplotlib', 'notebook')

from numpy import *
import os
from os import path
home = path.expanduser("~")

import matplotlib.pyplot as plt

# define plot style
width = 0.05
plotMarkerSize = 8
labelfontsize = 15
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = [6., 4.5]
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['xtick.top'] = True
mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['xtick.major.width'] = 1.0
mpl.rcParams['xtick.minor.width'] = 0.8
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['xtick.direction'] = "in"
mpl.rcParams['ytick.right'] = True
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['ytick.major.width'] = 1.0
mpl.rcParams['ytick.minor.width'] = 0.8
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['ytick.direction'] = "in"
mpl.rcParams['legend.fontsize'] = 15
mpl.rcParams['legend.numpoints'] = 1
mpl.rcParams['font.size'] = 15
mpl.rcParams['savefig.format'] = "pdf"

working_path = os.getcwd()


# # change the following line to your result folder(s)

# In[3]:


results_path = os.path.dirname(working_path)


# In[4]:


plots_path = path.join(os.path.dirname(working_path), "plots")


# In[5]:


exercise_path = "run_exercise_3"


# In[6]:


# change the following line to your result folder(s)
RunFolder1 = "run_exercise_2"
RunFolder2 = "run_exercise_3"

# label our calculations
labels=[r"$\eta/s = 0.$", r"$\eta/s = 0.15$"]


# In[7]:


# load the data table(s)
data1 = loadtxt(path.join(results_path, RunFolder1, "momentum_anisotropy_eta_-0.5_0.5.dat"))
data2 = loadtxt(path.join(results_path, RunFolder2, "momentum_anisotropy_eta_-0.5_0.5.dat"))
ecc_data1 = loadtxt(path.join(results_path, RunFolder1, "eccentricities_evo_eta_-0.5_0.5.dat"))
ecc_data2 = loadtxt(path.join(results_path, RunFolder2, "eccentricities_evo_eta_-0.5_0.5.dat"))
Re_data1 = loadtxt(path.join(results_path, RunFolder1, "inverse_Reynolds_number_eta_-0.5_0.5.dat"))
Re_data2 = loadtxt(path.join(results_path, RunFolder2, "inverse_Reynolds_number_eta_-0.5_0.5.dat"))


# ## Averaged temperature evolution as a function of $\tau$
# 
# One interesting thermodyanmic quantity during the hydrodynamic simulations is temperature. Its evolution determines the fate of high energy partons travel through the medium.
# 
# In hydrodynamic simulations, temperature has a 3D distribution and evolves with time. To visualize the evolution of temperature, we will compute the system's averaged temperature $\langle T \rangle$ and plot it as a function of $\tau$. Here we define the averaged temperature using energy density as a weight.
# 
# <div class="math">
#     \begin{equation}
#         \langle T \rangle = \frac{\int d^2 x e(x, y) T(x, y)}{\int d^2 x e(x, y)}
#     \end{equation}
# </div>

# In[8]:


fig = plt.figure()

plt.plot(Re_data1[:, 0], Re_data1[:, -1], '-k', label=labels[0])
plt.plot(Re_data2[:, 0], Re_data2[:, -1], '--r', label=labels[1])

plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle T \rangle$ [GeV]")
plt.tight_layout()

plt.savefig(path.join(plots_path, "{0}_avgT_evo").format(exercise_path))


# ## Averaged velocity as a function of $\tau$
# 
# The local pressure gradients accelerate fluid. At low temperature where fluid cells are converted to individual hadrons, the local fluid velocity will boost particle's momentum. During this particlization stage, the spatial distribution of the fluid velocity is directly map to the momenta of emitted particles. Therefore, the experimental measured particle momentum distribution contains information about the fluid velocity at kinetic freeze-out. 
# 
# The radial flow of hydrodynamics can boost particles to higher momenta and increases their averaged transverse momentum. Here, we would like to understand how buil viscosity affects the development of radial flow in the hydrodynamic simulations.

# In[9]:


# compute the average transverse velocity
gamma = Re_data1[:, -2]
v_avg1 = sqrt(1. - 1./(gamma**2.))
gamma = Re_data2[:, -2]
v_avg2 = sqrt(1. - 1./(gamma**2.))

fig = plt.figure()

plt.plot(Re_data1[:, 0], v_avg1, '-k', label=labels[0])
plt.plot(Re_data2[:, 0], v_avg2, '--r', label=labels[1])

plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle v \rangle$")
plt.tight_layout()

plt.savefig(path.join(plots_path, "{0}_avgV_evo").format(exercise_path))


# ### Evolution of the spatial eccentricity
# 
# The acceleration of the fluid cell is driven by local pressure gradients. Hydrodynamics converts the spatial eccentricity of energy density profile into anistropy in fluid velocity and finally imprints to momentum of the emitted particles.
# 
# Here we would like to see how the spatial eccenticity evolution as a function of $\tau$ during the hydrodynamic simulations with different valued of viscosity.

# In[10]:


fig = plt.figure()

plt.plot(ecc_data1[:, 0], sqrt(ecc_data1[:, 3]**2+ecc_data1[:, 4]**2), '-k', label=labels[0])
plt.plot(ecc_data2[:, 0], sqrt(ecc_data2[:, 3]**2+ecc_data2[:, 4]**2), '--r', label=labels[1])

plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\epsilon_2$")
plt.tight_layout()

plt.savefig(path.join(plots_path, "{0}_ecc2_evo").format(exercise_path))


# ### Averaged momentum anisotropy as a function of $\tau$
# 
# The system's momentum anisotropy is defined as
# $\epsilon_p = \sqrt{\frac{\langle T^{xx} - T^{yy}\rangle^2 + 2 \langle T^{xy} \rangle^2}{\langle T^{xx} + T^{yy}\rangle^2}}$. This quantities is monotonically related to the charged hadron elliptic flow coefficient. Therefore, we can gain intuitive idea about how elliptic flow is develop during the collision by studying the evolution of momentum anistropy.

# In[11]:


fig = plt.figure()

plt.plot(data1[:, 0], sqrt(data1[:, 11]**2+data1[:, 12]**2), '-k', label=labels[0])
plt.plot(data2[:, 0], sqrt(data2[:, 11]**2+data2[:, 12]**2), '--r', label=labels[1])


plt.legend(loc=0)
plt.xlabel(r"$\tau$ [fm]")
plt.ylabel(r"$\langle \epsilon_p \rangle$")
plt.tight_layout()

plt.savefig(path.join(plots_path, "{0}_momentum_aniso_evo").format(exercise_path))

