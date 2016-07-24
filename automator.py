import os, sys, subprocess32, time

cmd_list = [["make", "clean"],
			["make", "dats"],
			["python", "CfieldDataPrep.py", "cfield.dat"],
			"ffmpeg -loglevel fatal -r 10 -f image2 -s 1024x768 -i ./FieldData/pngmovie/%d.png  -vcodec libx264 -crf 25  -pix_fmt yuv420p ./cfield.mp4".split(),
			["python", "ParticleDataPrep.py", "particles.dat"],
			"ffmpeg -loglevel fatal -r 10 -f image2 -s 1024x768 -i ./ParticleData/pngmovie/%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ./particle.mp4".split(),
			["rm", "cfield.dat", "particles.dat"],
			["python", "Quiver.py"],
			"ffmpeg -loglevel fatal -r 10 -f image2 -s 1024x768 -i ./QuiverData/%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p ./quiver.mp4".split()
			]

#sys.argv[1] is the folder in which the executable is located
if __name__ == "__main__":
	target_dir = sys.argv[1]
	os.chdir(target_dir)
	
	for command in cmd_list:
		subprocess32.call(command)
