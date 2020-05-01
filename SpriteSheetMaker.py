# Author: Alexander Posipanko
# Description:  Gathers all GIFs in the scripts directory and compiles a spritesheet,
#               saving relavent data to split the sprite sheet back into individual GIFs.
               
from PIL import Image, ImageSequence
import PIL
import sys
import ntpath
import os


# Stores data about an animation row. Used to write to the save file.
class Animation:
    name = ""
    frames = 0
    height = 0
    width = 0
    def __init__(self,name,frames,height,width):
        self.name = name
        self.frames = frames
        self.height = height
        self.width = width


# Horizontal concatination to build strips of an animation
def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width, im1.height))
    dst.compress_level = 0
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

# Vertical concatination to build the sheet out of many animations
def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (max(im1.width,im2.width), im1.height + im2.height))
    dst.compress_level = 0
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

# Build a horizontal strip
# Algorithm sourced from mmgp on stackoverflow
# https://stackoverflow.com/questions/14550055/loss-of-data-when-extracting-frames-from-gif-to-png/14550885#14550885
def get_strip(inImg):
    
    img = inImg # Store the GIF that we're working with
    img.compress_level = 0
    inImg.compress_level = 0

    bImg = img  # Stores the background for when we paste tiled frames over eachother
    bImg.compress_level = 0
    pal = img.getpalette()

    prev = img
    prev_dispose = True 

    for i, frame in enumerate(ImageSequence.Iterator(img)):
        dispose = frame.dispose

        # If the GIF has a tile of the area that changed, we crop that
        # To paste on top of the previous frame later
        if frame.tile:
            x0, y0, x1, y1 = frame.tile[0][1]

            if not frame.palette.dirty: # Clean up the palette
                frame.putpalette(pal)

            frame = frame.crop((x0, y0, x1, y1))
            bbox = (x0, y0, x1, y1)
        else:
            bbox = None


        if dispose is None:
            prev = Image.new('RGBA', img.size, color =  (0,0,0,0))
            prev.compress_level = 0
            prev.paste(frame, bbox, frame.convert('RGBA'))
            prev_dispose = False
        else:
            if prev_dispose:
                prev = Image.new('RGBA', img.size, (0, 0, 0, 0))
                prev.compress_level = 0
            out = prev.copy()
            out.compress_level = 0
            out.paste(frame, bbox, frame.convert('RGBA'))
            prev = out
        bImg = get_concat_h(bImg, prev)
    return bImg

# get the length of an animation in frames
def get_length(img):
    count = 0
    for i in enumerate(ImageSequence.Iterator(img)):
        count += 1
    return count

Animations = []
img = Image.new('RGBA', (1,1), color = (0, 0, 0, 0))
img.compress_level = 0
sheet = img
sheet.compress_level = 0
first = True

# Loop through all the files in the working directory
# Assemble all the GIFs onto a spritesheet
files = filter(os.path.isfile, os.listdir( os.curdir) )  
for f in files:
    if f.endswith(".gif"):
        #print f
        img = Image.open(f)
        img.convert('RGBA')
        Animations.append(Animation(f,get_length(img),img.width,img.height))
        newStrip = get_strip(img)
        if first:
            sheet = newStrip
            first = False
        else:
            sheet = get_concat_v(sheet, newStrip)

# Record data about the animations we're adding to the sheet
file = open("spritesheet.dat","w")
for anim in Animations:
    print(anim.name + "," + str(anim.frames) + "," + str(anim.width) + "," + str(anim.height)) 
    file.write(anim.name + "," + str(anim.frames) + "," + str(anim.width) + "," + str(anim.height))
    file.write("\n")
file.close()

# Save the spritesheet
sheet.compress_level = 0
sheet.save('out.png')

