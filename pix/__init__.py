# -*- coding: utf-8 -*-
# @Author: detailyang
# @Date:   2016-09-20 21:13:28
# @Last Modified by:   detailyang
# @Last Modified time: 2016-09-23 20:26:57


import argparse
import sys
from os import path
from PIL import Image
from jinja2 import Template


dtpl = '''
<style>
body {
    margin: 0px;
}
.art {
    position: relative;
    width: {{ width }}px;
    height: {{ width }}px;
    animation: {{duration}}s art steps(1) infinite;
}

@keyframes art {
   {% for k in keyframes %}
        {{k.progress}} {
            box-shadow: {{k.frame}};
        }
   {% endfor %}
}
</style>

<div class="art"></div>
'''

stpl = '''
<style>
body {
    margin: 0px;
}
.art {
    position: relative;
    width: {{ width }}px;
    height: {{ width }}px;
}

div {
    box-shadow: {{ art }};
}
</style>

<div class="art"></div>
'''

dir = path.dirname(path.abspath(__file__))


def toGif(args, im):
    tpl = Template(dtpl)
    palette = im.getpalette()

    try:
        scale = args.scale
        arts = []
        i = 0
        pw = 1
        duration = 0

        while True:
            im.putpalette(palette)
            duration = duration + im.info['duration']

            # scale image
            nim = Image.new("RGBA", im.size)
            w = nim.size[0]
            h = nim.size[1]
            nim.paste(im)
            nim = nim.resize((int(w * scale), int(h * scale)), Image.ANTIALIAS)
            w = nim.size[0]
            h = nim.size[1]

            arts.append([])
            for x in range(0, w):
                for y in range(0, h):
                    px = nim.getpixel((x, y))
                    arts[i].append("%dpx %dpx 0 #%.2x%.2x%.2x" % (int(x * pw), int(y * pw), px[0], px[1], px[2]))

            im.seek(im.tell() + 1)
            i = i + 1
    except EOFError:
        pass

    keyframes = []

    for i, art in enumerate(arts):
        keyframes.append({
            'progress': '%.1f%%' % (100 / len(arts) * i),
            'frame': ','.join(art)
        })

    return tpl.render({
        'keyframes': keyframes,
        'width': 1,
        'duration': duration / 1000.0
    })


def toOther(args, im):
    tpl = Template(stpl)
    scale = args.scale
    width = args.width

    w = im.size[0]
    h = im.size[1]
    im = im.resize((int(w * scale), int(h * scale)), Image.ANTIALIAS)
    w = im.size[0]
    h = im.size[1]

    art = []
    for x in range(0, w):
        for y in range(0, h):
            # print(w, h)
            px = im.getpixel((x, y))
            art.append("%dpx %dpx 0 #%.2x%.2x%.2x" % (int(x * width), int(y * width), px[0], px[1], px[2]))

    return tpl.render({
        'width': str(width),
        'art': ','.join(art)
    })


def main():
    parser = argparse.ArgumentParser(description='transform picture to CSS pixel art')
    parser.add_argument('filename', help='picture filename')
    parser.add_argument('-w', '--width', help='per pixel width (px)', type=int, default=5)
    parser.add_argument('-s', '--scale', help='scale the picture', type=float, default=1)

    args = parser.parse_args()

    try:
        im = Image.open(args.filename)
    except IOError:
        print("cannot open the file %s" % args.filename)

        sys.exit(1)

    if im.format == 'GIF':
        print(toGif(args, im))
    else:
        print(toOther(args, im))

if __name__ == '__main__':
    main()
