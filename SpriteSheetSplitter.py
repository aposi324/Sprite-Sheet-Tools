# Author: Alexander Posipanko
# Description:  Splits a spritesheet made by Sprite Sheet Maker back into GIFs using spritesheet.dat

import csv
from PIL import Image, ImageSequence
import PIL

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


# Author: zrksyd
# Adapted by Alexander Posipanko 4/28/2020
# Description: Take a sprite strip and convert it to a GIF
def strip_to_gif(img, numberOfSlices, name):
    imageWidth, imageHeight = img.size
    sliceWidth = imageWidth // numberOfSlices
    imageArray = []

    if name == "yoshi_idle.gif":
        img.show()
    i=0
    for i in range(0,numberOfSlices):
        left = (i) * sliceWidth
        right = (i+1) * sliceWidth
        upper = 0
        lower = imageHeight
        workingSlice = img.crop((left, upper, right, lower))
        imageArray.append(workingSlice)

    try:
        imageArray[0].save(name,format= 'gif', save_all = True, duration = 3*numberOfSlices, append_images = imageArray[:], loop = 0, optimize=False)
    except:
        print("Error saving " + name)

    return


# Read the data file to gather the necessary information to parse the animations from the spritesheet
animations = []
with open('spritesheet.dat', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        animations.append(Animation(row[0],int(row[1]),int(row[2]),int(row[3])))
        print("...".join(row))

for anim in animations:
    print(anim.name + "," + str(anim.frames) + "," + str(anim.width) + "," + str(anim.height))

current_h = 0   # Current height of the spritesheet we are operating on

try:
    spritesheet = Image.open("out.png")
except: 
    print("Error opening sprite sheet. Please make sure out.png is in the same directory as the executable.")


for anim in animations:
    #if c == 2:
   
    print("Processing " + anim.name + "...")
    strip = spritesheet.crop((0,current_h,anim.width*(anim.frames+1),current_h+anim.height))
    strip.compress_level = 0

    strip_to_gif(strip.convert('P'), anim.frames+1, anim.name)
    current_h += anim.height

print("All done!")
