import os, sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from shutil import rmtree

#___ Initialising parameters ___ #
paramfile = open("param.h", "r")
paramdict = {}
for line in paramfile:
	name = line.split()[1]
	if name in ['dt']:
		value = float(line.split()[2])
		paramdict[name] = value
	else:
		value = int(line.split()[2])
		paramdict[name] = value


def fieldtopng(datarootdir = "FieldData"):
	number_step = paramdict['number_step']
	quantum = paramdict['quantum']
	Lsx = paramdict["Lsx"]
	Lsy = paramdict["Lsy"]
	dt = paramdict["dt"]
	latticearea = Lsx*Lsy
	
	cfield = np.zeros(shape = (Lsy, Lsx))
	
	# ---  If folder "pngmovie" already exists, delete and recreate !! --- #
	if os.path.exists("%s/pngmovie" %datarootdir):
		rmtree("%s/pngmovie" %datarootdir)
		listofdats = os.listdir(datarootdir)
	else:
		listofdats = os.listdir(datarootdir)
	os.mkdir("%s/pngmovie" %datarootdir)
		
	# --- Generate list with data file names, sans the extension .dat
	fnum = len(listofdats)	
	flist = [int(item.split(".")[0]) for item in listofdats]
	flist.sort()
	
	# --- Looping over all the .dat files in datarootdir --- #
	for j in range(fnum):
		 stepdata = open("%s/%i.dat" %(datarootdir,flist[j]), 'r')
		 
		 for k in np.arange(latticearea):
			 data = stepdata.readline().split()
			 if len(data) != 0:
				x = int(data[0]); y = int(data[1])
				cfield[y, x] = float(data[-1])
		 stepdata.close()	 
		 cfield = np.flipud(cfield) #Reversing the y axis, necessary for cfield.mp4 and particles.mp4 to match
		 
		 # --- Saving as PNG file --- #
		 #First, turn off on-screen display of plots. See http://stackoverflow.com/questions/15713279/calling-pylab-savefig-without-display-in-ipython
		 plt.ioff()
		 
		 fig = plt.figure()
		 plt.title("Time step %s, t = %f" %(j*quantum, dt*quantum*j))
		 plt.imshow(cfield, cmap = cm.summer)
		 plt.colorbar()
		 
		 plt.savefig('%s/pngmovie/%i.png' %(datarootdir, j))
		 plt.close(fig)
		 print("Snapshot of timestep %i written to PNG" %flist[j])
		
if __name__ == "__main__":
    datafolder = sys.argv[1]
    if os.path.exists(datafolder):
        fieldtopng(datafolder)
