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
    asciiart.py FILE [options]
    asciiart.py (-h | --help)
    asciiart.py (-v | --version)

options:
    --help -h           Show this screen.
    --version -v        Show version.
    --pal -p = <p>      ASCII-pharacter palette to be used [default: 2].
    --nhor -n = <n>     Number of chars in horizontal dim [default: 50].
    --chsize -s = <si>  Characters pixels in final image [default: 15].
    --color -c = <col>  Color of the characters [default: 255, 215, 0].
    --whitebg -w        Use white backgr. instead of black with white chars.
    --font -f = <font>  Use special font [default: courier-boldregular.ttf].
                        Font needs to be supplied in folder.
"""

import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from docopt import docopt

# import pdb

PALETTES = (
    "$#H&@*+;:-,.  ",
    "@%#*+=-:.  ",
    "BS#@$%*!:.  ",
    "WB#@$\%wx*i!;:,.  ",
    "█▇▆▅▄▃▂▁  ",
)


class Par(object):
    pass


P = Par()
args = docopt(__doc__, version="asciiart 0.1")


def checkAndSetPar():
    """
    Assert parameter values and write to global paramter object. 
    Wrong types or impossible type convertions will throw exceptions
    that are not caught here.
    """
    tmp = int(args["--pal"])
    assert tmp in range(
        len(PALETTES)
    ), f"arg of --pal must be in range 0...{len(PALETTES)-1}"
    P.SCALE = PALETTES[tmp]

    tmp = int(args["--nhor"])
    assert tmp > 0, "arg of --nhor must be a positive integer!"
    P.NHORIZ = tmp

    tmp = int(args["--chsize"])
    assert tmp > 0, "arg of --chsize must be a positive integer"
    P.CHARSIZE = tmp

    P.FONT = args["--font"]

    tmp = eval(args["--color"])
    assert min(tmp) >= 0 and max(tmp) <= 255, "--r,g,b must be within 0...255"
    P.COLOR = tmp

    P.WHITEBG = args["--whitebg"]
    P.FILE = args["FILE"]


def pixel2char(val, scale):
    """convert a pixel value in range 0...255 to a character."""
    index = round(np.floor(val / 255.0 * (len(scale) - 1)))
    return scale[index]


def coloredTxt(r, g, b, txt):
    """print string 'txt' in colors r,b,g."""
    return f"\033[38;2;{r};{g};{b}m{txt}\033[48;2;0;0;0m"


def printImage(img):
    """print the image to the console in b/w or colored."""
    for row in img:
        print()
        for val in row:
            if np.ndim(val) != 1:  # b&w
                print(
                    f"\033[38;2;255;255;255m{pixel2char(val,P.SCALE)}", end=""
                )
            else:  # colored
                print(
                    coloredTxt(*val, pixel2char(np.mean(val[:3]), P.SCALE)),
                    end="",
                )


def getCharImage(ch, scaleChar=1.2):
    """
    generate and return image of a character.
    ch:         character shown in image.
    scaleChar:	scale up or down the character in the image. 1 = normal scale.
    im:         image containing the character.
    """
    fnt = ImageFont.truetype(P.FONT, int(P.CHARSIZE * scaleChar))
    colors = {True: P.COLOR, False: (0, 0, 0)}
    im = Image.new("RGB", (P.CHARSIZE, P.CHARSIZE), colors[P.WHITEBG])
    draw = ImageDraw.Draw(im)
    draw.text(
        (int(P.CHARSIZE / 2), int(P.CHARSIZE / 2)),
        ch,
        anchor="mm",
        font=fnt,
        fill=colors[not P.WHITEBG],
    )
    return im


def getWholeImage(dat):
    """
    concatenate a complete image out ouf single character Images.
    Each pixel of dat will be converted to a single char image.
    dat:        the image data as numpy string that will be transformed
                to the asciiart.
    complete:   the asciiart image
    """
    complete = Image.new(
        "RGB", (P.CHARSIZE * dat.shape[1], P.CHARSIZE * dat.shape[0]), "black"
    )
    sc = P.SCALE if P.WHITEBG else P.SCALE[::-1]
    for row in range(dat.shape[0]):
        for col in range(dat.shape[1]):
            ch = pixel2char(dat[row, col], sc)
            im = getCharImage(ch)
            complete.paste(im, (col * P.CHARSIZE, row * P.CHARSIZE))
    return complete


def loadAndReshapeImage():
    """
    load and reshape image to given horizontal number of characters.
    Returns 2 version, one b/w and one colored for future colored asciiarts.
    """
    im = Image.open("./" + P.FILE)
    shape = (P.NHORIZ, round(P.NHORIZ / im.size[0] * im.size[1]))
    imBwScaled = np.array(im.resize(shape, Image.ANTIALIAS).convert("L"))
    imColScaled = np.array(im.resize(shape, Image.ANTIALIAS))
    return imBwScaled, imColScaled


def main():
    checkAndSetPar()
    """main function generating and saving the asciiart."""
    imBwScaled, _ = loadAndReshapeImage()
    getWholeImage(imBwScaled).save(P.FILE.split(".")[0] + ".png")


if __name__ == "__main__":
    main()
