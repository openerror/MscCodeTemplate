import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from shutil import rmtree
import os

#___ Initialising parameters ___ #
paramfile = open("param.h", "r")
paramdict = {}
try:
	for line in paramfile:
		name = line.split()[1]
		if name in ['dt']: #List should contain all parameters which need to be floats
			value = float(line.split()[2])
			paramdict[name] = value
		else:
			value = int(line.split()[2])
			paramdict[name] = value
except IndexError:
	print("Opps - IndexError encountered. Are there blank lines below the parameters?\n")
paramfile.close()

nparticles = paramdict["nparticles"]
quantum = paramdict["quantum"]
scaling = paramdict["scaling"]
Lx = paramdict["Lx"]
Ly = paramdict["Ly"]
dt = paramdict["dt"]
lattice_pts_x = complex(Lx * scaling)
lattice_pts_y = complex(Ly * scaling)

#___ Create a sorted list of input file names, sans the extension (.dat) ___#
flist = []
for item in os.listdir("ParticleData"):
	if item != "pngmovie":
		datname = int(item.split(".")[0])
		flist.append(datname)
flist.sort()

if os.path.exists("QuiverData"):
	rmtree("QuiverData")
	os.mkdir("QuiverData")
else:
	os.mkdir("QuiverData")

n = 0 #Integer value to be used for naming the PNGs
for fname in flist:
	n += 1
	X, Y = np.mgrid[0:Lx:lattice_pts_x, 0:Ly:lattice_pts_y]
	U = np.zeros(shape = X.shape)
	V = np.zeros(shape = Y.shape)
	
	datafile = open("ParticleData/%s.dat" %fname, "r")
	N = np.arange(nparticles) #Pre-allocate for efficiency
	
	for particle_id in N:
		data = datafile.readline().split()
		x = float(data[1])*scaling; y = float(data[2])*scaling; phi = float(data[-1])
		x = int(np.round(x, 0)) - 1; y = int(np.round(y, 0)) - 1
		
		# __ Altering the vector magnitudes to adjust the quivers' colors __ #
		# By design, only the shortest and the longest vectors stand out in the plot
				
		if particle_id == 0:								#Sacrifice one particle to set the scale right
			U[x, y] = 0.595*np.cos(phi); V[x, y] = 0.595*np.sin(phi)
		elif particle_id in np.arange(0, nparticles, 100):	#Tracer particles
			U[x, y] = np.cos(phi); V[x, y] = np.sin(phi)
		else:												#The rest
			U[x, y] = 0.2*np.cos(phi); V[x, y] = 0.2*np.sin(phi)
	
	datafile.close()
	M = U**2 + V**2 #M for magnitude. This array will determine the quivers' colours '''
	
	''' ___ Code for plotting ___ '''
	plt.ioff()
	fig = plt.figure()
	ax = fig.add_subplot(111, aspect = 'equal')
	
	# ___ Enlarge the plot beyond default size; useful for nparticle > O(10^2) ___ #
	DefaultDPI = fig.get_dpi();fig.set_dpi(DefaultDPI*1.1)
	DefaultInches = fig.get_size_inches(); fig.set_size_inches(DefaultInches[0]*1.1, DefaultInches[1]*1.1)
	
	plt.quiver(X, Y, U, V, 
		   M, cmap = cm.seismic,
		   #color = "Teal", #for when quivers are of a single colour
		   units = "width", 
		   width = 0.001,
		   headwidth = 15, headlength = 15, 
		   scale = 8)
	
	#plt.colorbar()
	#plt.tick_params(axis='both', which='minor', labelsize=12)
	plt.tick_params(axis='both', which='major', labelsize=12)
	plt.title("Time step %i, t = %f" %(fname, n*quantum*dt))
	plt.savefig("QuiverData/%d.png" %n)
	plt.close(fig)
	
	print("Quiver plot saved to %d.png" %n)
