''' Format of data file: 4 columns of space-delimited numbers:
    step number, x, y, direction
    
    The goal of this program is to read each *.dat file in [datafolder],
    and plot it as a PNG image
     
    Usage: python ParticleDataPrep.py [datafolder]
    
    Note to self: for more on commandline arguments, http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
'''

import os, sys
import matplotlib.pyplot as plt
import numpy as np
from shutil import rmtree

#___ Initialising parameters ___ #
paramfile = open("param.h", "r")
paramdict = {}
for line in paramfile:
	name = line.split()[1]
	if name in ['dt']: #List should contain all parameters which need to be floats
		value = float(line.split()[2])
		paramdict[name] = value
	else:
		value = int(line.split()[2])
		paramdict[name] = value
    
def steptopng(datarootdir): 
	''' Visualises the .dat of a single timestep, output to PNG image '''
    
	nparticles = paramdict["nparticles"]
	number_step = paramdict['number_step']
	quantum = paramdict['quantum']
	Lx = paramdict["Lx"]
	Ly = paramdict["Ly"]
	dt = paramdict["dt"]
    
    # --- These are the arrays to be plotted, pre-initialised ---
	xpos = np.zeros(shape = nparticles)
	ypos = np.zeros(shape = nparticles)
	
	# --- Assumption: datarootdir only contains .dat files --- #
	if os.path.exists("%s/pngmovie" %datarootdir):
		rmtree("%s/pngmovie" %datarootdir) 	# !! if folder "pngmovie" already exists, delete and recreate !!
		fnum = len(os.listdir(datarootdir))	#amount of .dat files in datarootdir
		flist = [int(item.split(".")[0]) for item in os.listdir(datarootdir)] #list of all .dat filenames, sans the extension
		flist.sort()
		os.mkdir("%s/pngmovie" %datarootdir)
	else:
		fnum = len(os.listdir(datarootdir)) 	
		flist = [int(item.split(".")[0]) for item in os.listdir(datarootdir)]
		flist.sort()
		os.mkdir("%s/pngmovie" %datarootdir)
	
	#variable j will be used to name the PNGs
	for j in range(fnum):
		 stepdata = open("%s/%i.dat" %(datarootdir,flist[j]), 'r')
		 
		 for k in range(nparticles):
			 data = stepdata.readline().split()
			 xpos[k] = data[1]
			 ypos[k] = data[2]
			 
	# --- Saving as PNG file --- #
	#First, turn off on-screen display of plots. See http://stackoverflow.com/questions/15713279/calling-pylab-savefig-without-display-in-ipython
		 plt.ioff()
		 fig = plt.figure()
		 DefaultDPI = fig.get_dpi(); fig.set_dpi(DefaultDPI*1.5)
		 DefaultInches = fig.get_size_inches(); fig.set_size_inches(DefaultInches[0]*1.5, DefaultInches[1]*1.5)
		 ax = fig.add_subplot(111, aspect = 'equal')
		 plt.axis([0, Lx, 0, Ly]); plt.title("Time step %i, t = %f" %(flist[j], j*quantum*dt))
		 plt.plot(xpos, ypos, 'r+')
		 plt.savefig('ParticleData/pngmovie/%i.png' %j)
         
		 plt.close(fig)
		 print("Snapshot of timestep %i written to PNG" %flist[j])
		 stepdata.close()

if __name__ == "__main__":
	datafolder = sys.argv[1]
	if os.path.exists(datafolder):
		steptopng(datafolder)
	else:
		print("Invalid path to the raw data file")
