#! /usr/bin/python3
"""
    ___   _____ ______________   ___         __ 
   /   | / ___// ____/  _/  _/  /   |  _____/ /_
  / /| | \__ \/ /    / / / /   / /| | / ___/ __/
 / ___ |___/ / /____/ /_/ /   / ___ |/ /  / /_  
/_/  |_/____/\____/___/___/  /_/  |_/_/   \__/

Andreas de Moll, April 2022

description:
    Generates ascii-art from images. A given FILE (*.jpg) is
    converted to an ascii-art *.png and stored. Have fun!

usage:
    convert.py FILE [options]
    convert.py (-h | --help)
    convert.py (-v | --version)

options:
    --help -h           Show this screen.
    --version -v        Show version.
    --pal -p = <p>      ASCII-pharacter palette to be used [default: 2].
    --nhor -n = <n>     Number of chars in horizontal dim [default: 50].
    --chsize -s = <si>  Characters pixels in final image [default: 15].
    --color -c = <col>  Color of the characters [default: (255, 215, 0)].
    --whitebg -w        Use white background instead of black.
    --font -f = <font>  Use special font [default: courier-boldregular.ttf].
                        Font needs to be supplied in folder.
"""

import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from docopt import docopt
#import pdb

palettes = (
    "$#H&@*+;:-,.  ",
    "@%#*+=-:.  ",
    "BS#@$%*!:.  ",
    "WB#@$\%wx*i!;:,.  ",
    "█▇▆▅▄▃▂▁  ",
)

SCALE = palettes[2]
NHORIZ = 50
CHARSIZE = 15
FONT = "courier-boldregular.ttf"
COLOR = (255, 215, 0)
WHITEBG = False
FILE = "AuN"

def pixel2char(val, scale):
    """convert a pixel value in range 0...255 to a character."""
    index = round(np.floor(val / 255.0 * (len(scale) - 1)))
    return scale[index]


def coloredTxt(r, g, b, txt):
    """print string 'txt' in colors r,b,g."""
    return f"\033[38;2;{r};{g};{b}m{txt}\033[48;2;0;0;0m"


def printImage(dat):
    """print the image to the console in b/w or colored."""
    for row in dat:
        print()
        for val in row:
            if np.ndim(val) != 1:  # b&w
                print(f"\033[38;2;255;255;255m{pixel2char(val,SCALE)}", end="")
            else:  # colored
                print(
                    coloredTxt(*val, pixel2char(np.mean(val[:3]), SCALE)),
                    end="",
                )


def getCharImage(ch, scaleChar=1.2):
    """
    generate and return image of a character.
    ch:         character shown in image.
    scaleChar:	scale up or down the character in the image. 1 = normal scale.
    """
    fnt = ImageFont.truetype(FONT, int(CHARSIZE * scaleChar))
    colors = {True: COLOR, False: (0, 0, 0)}
    im = Image.new("RGB", (CHARSIZE, CHARSIZE), colors[WHITEBG])
    draw = ImageDraw.Draw(im)
    draw.text(
        (int(CHARSIZE / 2), int(CHARSIZE / 2)),
        ch,
        anchor="mm",
        font=fnt,
        fill=colors[not WHITEBG],
    )
    return im


def getWholeImage(dat):
    complete = Image.new(
        "RGB", (CHARSIZE * dat.shape[1], CHARSIZE * dat.shape[0]), "black"
    )
    sc = SCALE if WHITEBG else SCALE[::-1]
    for row in range(dat.shape[0]):
        for col in range(dat.shape[1]):
            ch = pixel2char(dat[row, col], sc)
            im = getCharImage(ch)
            complete.paste(im, (col * CHARSIZE, row * CHARSIZE))
    return complete


def loadAndReshapeImage():
    im = Image.open("./input/" + FILE + ".jpg")
    shape = (NHORIZ, round(NHORIZ / im.size[0] * im.size[1]))
    imBwScaled = np.array(im.resize(shape, Image.ANTIALIAS).convert("L"))
    imColScaled = np.array(im.resize(shape, Image.ANTIALIAS))
    return imBwScaled, imColScaled


def main():
    imBwScaled, _ = loadAndReshapeImage()
    getWholeImage(imBwScaled).save("./output/" + FILE + ".png")


if __name__ == "__main__":
    args = docopt(__doc__, version='asciiart 0.0')
    print(args)
    print(eval(args['--color']))

    main()