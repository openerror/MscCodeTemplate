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
    listofdats = os.listdir(datarootdir) #pre-assign to save time
	
	# --- Assumption: datarootdir only contains .dat files --- #
    if os.path.exists("%s/pngmovie" %datarootdir):
        rmtree("%s/pngmovie" %datarootdir) 	# !! if folder "pngmovie" already exists, delete and recreate !!
        fnum = len(listofdats)	#amount of .dat files in datarootdir
        flist = [int(item.split(".")[0]) for item in listofdats] #list of all .dat filenames, sans the extension
        flist.sort()
        os.mkdir("%s/pngmovie" %datarootdir)
    else:
        fnum = len(listofdats) 	
        flist = [int(item.split(".")[0]) for item in listofdats]
        flist.sort()
        os.mkdir("%s/pngmovie" %datarootdir)
	
	# --- Looping over all the .dat files in datarootdir --- #
    for j in range(fnum):
        stepdata = open("%s/%i.dat" %(datarootdir,flist[j]), 'r')
        
        for k in np.arange(latticearea):
            data = stepdata.readline().split()
            if len(data) != 0:
                x = int(data[0]); y = int(data[1])
                cfield[y, x] = float(data[-1])
                
        cfield = np.flipud(cfield) #Reversing the y axis, necessary for cfield.mp4 and particles.mp4 to match
        stepdata.close()	          
		 # --- Saving as PNG file --- #
		 #First, turn off on-screen display of plots. See http://stackoverflow.com/questions/15713279/calling-pylab-savefig-without-display-in-ipython
        plt.ioff()
		 
        fig = plt.figure()
        DefaultDPI = fig.get_dpi(); fig.set_dpi(DefaultDPI*1.5)
        DefaultInches = fig.get_size_inches(); fig.set_size_inches(DefaultInches[0]*1.5, DefaultInches[1]*1.5)
        plt.title("Time step %s, t = %f" %(j*quantum, dt*quantum*j))
        plt.imshow(cfield, cmap = cm.summer)
        plt.savefig('%s/pngmovie/%i.png' %(datarootdir, j))
        plt.close(fig)
        print("Snapshot of timestep %i written to PNG" %flist[j])
		
if __name__ == "__main__":
    datafolder = sys.argv[1]
    if os.path.exists(datafolder):
        fieldtopng(datafolder)
