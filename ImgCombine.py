import Image, ImageDraw, os, os.path
from shutil import rmtree 

datafolder = "CombinedPNGs" #Where the output will be stored

def combine(fnum):
    ''' 
        Take fnum, the PNG's file name sans the extension,
        and do wonderful things with the PNG. Acts on single file only.  
    '''

    #1) Open the two source images, which should be of the same size
    particle_img = Image.open("ParticleData/pngmovie/%d.png" %fnum).convert("RGBA")
    cfield_img = Image.open("FieldData/pngmovie/%d.png" %fnum).convert("RGBA")

    #3) Crop both images to remove the axis labels, then blend together
    data_w = 484; data_h = 484
    particle_w_offset = 170; particle_h_offset = 58
    cfield_w_offset = 113; cfield_h_offset = 58
    
    particle_cropbox = (particle_w_offset, particle_h_offset, \
                        particle_w_offset + data_w, particle_h_offset + data_h)
    particle_temp_img = particle_img.crop(particle_cropbox)
    
    cfield_cropbox = (cfield_w_offset, cfield_h_offset, \
                        cfield_w_offset + data_w, cfield_h_offset + data_h)
    cfield_temp_img =  cfield_img.crop(cfield_cropbox)

    #3) Combine the source images, with the cfield image half transparent
    #       Image.blend(image1, image2, alpha) > image
    #       out = image1 * (1.0 - alpha) + image2 * alpha
    data_img = Image.blend(cfield_temp_img, particle_temp_img, 0.2)

    #4) Paste over the original particle image, which has the desired axis labels
    particle_img.paste(data_img, particle_cropbox)

    print("Combined image saved as %d.png" %fnum)
    
    #5) Finally, add in the colour bar from cfield plot 
    cbar_cropbox = ( data_w + cfield_w_offset + 40, cfield_h_offset, \
                        cfield_img.size[0]-5, cfield_h_offset + data_h )
                        
    colourbar = cfield_img.crop(cbar_cropbox)
    particle_img.paste(colourbar, cbar_cropbox)
    
    particle_img.save("CombinedPNGs/%d.png" %fnum, "PNG")
    cfield_img.close(); particle_img.close(); 
    data_img.close()

if __name__ == "__main__":
    if os.path.exists(datafolder):
        rmtree(datafolder)
        os.mkdir(datafolder)
    else:
        os.mkdir(datafolder)
    
    #Folder 'pngmovie' is assumed to contain only PNG image files
    #range(n) will then indicate PNG file names
    n = len(os.listdir("ParticleData/pngmovie"))
    
    for fnum in range(n):
        combine(fnum)
