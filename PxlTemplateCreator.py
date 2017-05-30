# -*- encoding: utf-8 -*-

import sys
import os
import argparse
from PIL import Image
import PIL

ap = argparse.ArgumentParser()
ap.add_argument('image', type=str, help="Image you want to convert into a template.")
ap.add_argument('-num_transparent_pixels', type=int, dest='ntp', help="Number of transparent pixels between each pixel",
                default=1)
ap.add_argument('-v', action='store_true', default=False, dest='verbose', help="Show what the program is doing")
ap.add_argument('-out', '-o', dest='outfile', type=str, default=None, help='''Path for your template to be stored on.\n
                                                                           Default: imagename_template.png''')
args = ap.parse_args()
if args.outfile is None:
    args.outfile = str(os.path.split(args.image)[1]).split('.')[0] + '_template'


def load_image(image) -> Image:
    if not os.path.isfile(image):
        raise FileNotFoundError(image)
    img = Image.open(image)
    return img


def convert_image(image, out_file, num_transparent_pixels=1):
    # 1st: Convert it to indexed colors and add alpha channel
    image = image.convert('RGBA')

    # Create the new image
    newImage = Image.new('RGBA', (image.size[0]+(num_transparent_pixels*image.size[0]),
                                  image.size[1]+(num_transparent_pixels*image.size[1])))
    for ox in range(0, image.size[0]-1):
        for oy in range(0, image.size[1]-1):
            newImage.putpixel((ox+num_transparent_pixels*ox, oy+num_transparent_pixels*oy), image.getpixel((ox, oy)))
            if args.verbose:
                print("setting pixel", ox+num_transparent_pixels*ox, oy+num_transparent_pixels*oy,
                      "to", image.getpixel((ox, oy)))
    newImage.save(out_file + '_' + str(image.size[0]) + '.png')
    return

print("PxlTemplateCreator - create your templates the easy way")
print("Copyright (C) 2017 Haruna")
print("")
print("Join the official discord at https://discord.gg/pxls")
convert_image(load_image(args.image), args.outfile, args.ntp)