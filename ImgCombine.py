import Image, ImageDraw, os, os.path
from shutil import rmtree 

def main():
    if os.path.exists("CombinedPNGs"):
        rmtree("CombinedPNGs")
        os.mkdir("CombinedPNGs")
    else:
        os.mkdir("CombinedPNGs")
    
    #Folder 'pngmovie' is assumed to contain only PNG image files
    n = len(os.listdir("ParticleData/pngmovie"))
 
    for fnum in range(n):
        ''' fnum is used to identify the input and to name the output '''
    
        #1) Open the two source images, which should be of the same size
        particle_img = Image.open("ParticleData/pngmovie/%d.png" %fnum).convert("RGBA")
        cfield_img = Image.open("FieldData/pngmovie/%d.png" %fnum).convert("RGBA")

        #2) Combining the source images, with the cfield image half transparent
        temp_img = Image.blend(particle_img, cfield_img, 0.5)

        #3) Cropping temp_img to remove the axis labels
        w, h = temp_img.size
        w_offset = 164; h_offset = 58
        cropbox = (w_offset, h_offset, w - w_offset + 50, h - h_offset)
        temp_img = temp_img.crop(cropbox)

        #4) Finally, pasting temp_img over the original particle image, which has the desired axis labels
        particle_img.paste(temp_img, cropbox)
        particle_img.save("CombinedPNGs/%d.png" %fnum, "PNG")
        print("Combined image saved as %d.png" %fnum)

        cfield_img.close();particle_img.close();temp_img.close()

if __name__ == "__main__":
    main()
