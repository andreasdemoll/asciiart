#  /|,_ |   _    _   | _   |\/|  ||
# /-|||(||`(/_(|_\  (|(/_  |  |()||     Feb 2022

import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

scale0 = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~
		 <>i!lI;:,"^`'.      """
scale1 = "$#H&@*+;:-,. "
scale2 = "@%#*+=-:.  "
scale3 = "BS#@$%*!:.  "
scale4 = "WB#@$\%wx*i!;:,.  "
scaleU = "█▇▆▅▄▃▂▁  "

FAC = 5
SCALE = scale3
FILE = "AuN"

im = Image.open("./input/" + FILE + ".jpg")
shape = [round(i / FAC) for i in im.size]
dat = np.array(im.resize(shape, Image.ANTIALIAS).convert("L"))
datCol = np.array(im.resize(shape, Image.ANTIALIAS))


def pixel2char(val, scale):
    """convert a pixel value in range 0...255 to a character."""
    index = round(np.floor(val / 255.0 * (len(scale) - 1)))
    return scale[index]


def coloredTxt(r, g, b, txt):
    """print string 'txt' in colors r,b,g."""
    return f"\033[38;2;{r};{g};{b}m{txt}\033[48;2;0;0;0m"


def printImage(dat, scale):
    """print the image to the console in b/w or colored."""
    for row in dat:
        print()
        for val in row:
            if np.ndim(val) != 1:  # b&w
                print(f"\033[38;2;255;255;255m{pixel2char(val,scale)}", end="")
            else:  # colored
                print(coloredTxt(*val, pixel2char(np.mean(val[:3]), scale)), end="")


def genImage(ch, size, isWhiteBg=False, font="courier-boldregular.ttf", scaleUp=1.2):
    """
    generate and return image of a character.
    size: 		size of the returned squarish character image in pixels.
    isWhiteBg: 	use white or black background.
    scaleUp:	scale up or down the letter in the returned image. 1 = normal scale.
    """
    fnt = ImageFont.truetype(font, int(size * scaleUp))
    colors = {True: (255, 215, 0), False: (0, 0, 0)}
    im = Image.new("RGB", (size, size), colors[isWhiteBg])
    draw = ImageDraw.Draw(im)
    draw.text(
        (int(size / 2), int(size / 2)),
        ch,
        anchor="mm",
        font=fnt,
        fill=colors[not isWhiteBg],
    )
    return im


def genWholeImage(dat, size, scale=scale3):
    complete = Image.new("RGB", (size * dat.shape[1], size * dat.shape[0]), "black")
    sc = scale if isWhiteBg else scale[::-1]
    for row in range(dat.shape[0]):
        for col in range(dat.shape[1]):
            ch = pixel2char(dat[row, col], sc)
            im = genImage(ch, size)
            complete.paste(im, (col * size, row * size))
    return complete


# genImage('@',20,True).show()
genWholeImage(dat, 15, False, SCALE).save("./output/" + FILE + ".png")
# printColoredImage(datCol)
