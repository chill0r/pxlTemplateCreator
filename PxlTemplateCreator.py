# -*- encoding: utf-8 -*-

import sys
import os
import argparse
from PIL import Image
import PIL
import urllib.request as request
import urllib.parse as urlparse
import base64
import webbrowser
import json

ap = argparse.ArgumentParser()
ap.add_argument('image', type=str, help="Image you want to convert into a template.")
ap.add_argument('-num_transparent_pixels', type=int, dest='ntp', help="Number of transparent pixels between each pixel",
                default=2)
ap.add_argument('-num_solid_pixels', type=int, dest='nsp', help="Number of solid pixels between each pixel",
                default=2)
ap.add_argument('-v', action='store_true', default=False, dest='verbose', help="Show what the program is doing")
ap.add_argument('-out', '-o', dest='outfile', type=str, default=None, help='''Path for your template to be stored on.\n
                                                                           Default: imagename_template.png''')
ap.add_argument('-generate_link', '-gl', dest='genLink', action='store_true', default=False, help='''Automatically upload the image to imgur.com and generate the templatelink''')

args = ap.parse_args()


if args.outfile is None:
    args.outfile = str(os.path.split(args.image)[1]).split('.')[0] + '_template'


def load_image(image) -> Image:
    if not os.path.isfile(image):
        raise FileNotFoundError(image)
    img = Image.open(image)
    return img


def upload_to_imgur(imagepath) -> str:
    with open(imagepath, 'rb') as fh:
        bdata = base64.b64encode(fh.read())
    data = urlparse.urlencode({'image': bdata,'type': 'base64'}).encode('utf-8')
    req = request.Request('https://api.imgur.com/3/image', data)
    req.add_header('authorization', 'Client-ID 6af3bde991a78db')
    oreq = request.urlopen(req)
    if oreq.getcode() != 200:
        print("Something went wrong on uploading to imgur.")
        if args.verbose:
            print("Responsecode: %s" % oreq.getcode())
        return None
    reqdata = oreq.read().decode('utf-8')
    reqjson = json.loads(reqdata)
    if not reqjson['success']:
        print("Something went wrong on uploading to imgur.")
        if args.verbose:
            print("Error from api")
    url = reqjson['data']['link']
    oreq.close()
    return url


def convert_image(image, out_file, num_transparent_pixels=2, num_solid_pixels=2):
    # 1st: Convert it to indexed colors and add alpha channel
    image = image.convert('RGBA')

    # Create the new image
    newImage = Image.new('RGBA', ((num_solid_pixels+num_transparent_pixels)*image.size[0],
                                  (num_solid_pixels+num_transparent_pixels)*image.size[1]))
    for ox in range(0, image.size[0]-1):
        for oy in range(0, image.size[1]-1):
            for x in range(0, num_solid_pixels):
                for y in range(0, num_solid_pixels):
                    posx = ox*(num_transparent_pixels+num_solid_pixels)+x+int(num_transparent_pixels/2)
                    posy = oy*(num_transparent_pixels+num_solid_pixels)+y+int(num_transparent_pixels/2)
                    newImage.putpixel((posx, posy), image.getpixel((ox, oy)))
                    if args.verbose:
                        print("setting pixel", ox+num_transparent_pixels*ox, oy+num_transparent_pixels*oy,
                              "to", image.getpixel((ox, oy)))
    newImage.save(out_file + '_' + str(image.size[0]) + '.png')
    return out_file + '_' + str(image.size[0]) + '.png', str(image.size[0])

print("PxlTemplateCreator - create your templates the easy way")
print("Copyright (C) 2017 Haruna")
print("")
print("Join the official discord at https://discord.gg/pxls")
imgpath, orgsize = convert_image(load_image(args.image), args.outfile, args.ntp, args.nsp)
if args.genLink:
    url = upload_to_imgur(imgpath)
    if not url is None:
        templateurl = 'https://pxls.space/#x=140&y=103&scale=3&oo=1&template=' + url + '&tw=' + orgsize
        webbrowser.open(templateurl)

