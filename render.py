from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps
from image4layer import Image4Layer
from glitch_this import ImageGlitcher
import random
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
)

S = 2000  # size of the image
W, H = S, int(2 ** 0.5 * S)

NAME1 = "SRINIVAS"
NAME2 = "RAMANUJAN"
QUOTE = "The man who knew Infinity"

FONT1 = ImageFont.truetype("fonts/Uni Sans Heavy.otf", 300)
FONT2 = ImageFont.truetype("fonts/Uni Sans Heavy.otf", 90)
FONT3 = ImageFont.truetype("fonts/Uni Sans Heavy.otf", 900)

rmjn = Image.open("assets/ramanujan.png").convert("RGBA")
rmjn = rmjn.resize((int(rmjn.width * 4.5), int(rmjn.height * 4.5)))


def newimg():
    return Image.new("RGBA", (W, H))


img = newimg()
offset = 150
fill = (255, 255, 255, 255)

textimg1 = newimg()
draw1 = ImageDraw.Draw(textimg1)

w, h = draw1.textsize(NAME1, font=FONT1)
draw1.text(
    ((W - w) / 2, 1650 + offset),
    NAME1,
    font=FONT1,
    stroke_width=4,
    stroke_fill=(68, 68, 68),
    fill=fill,
)

w, h = draw1.textsize(NAME2, font=FONT1)
draw1.text(
    ((W - w) / 2, 1900 + offset),
    NAME2,
    font=FONT1,
    stroke_width=4,
    stroke_fill=(68, 68, 68),
    fill=fill,
)


textimg2 = newimg()
draw2 = ImageDraw.Draw(textimg2)

w, h = draw2.textsize(QUOTE, font=FONT2)
draw2.text(
    ((W - w) / 2, 2200 + offset),
    QUOTE,
    font=FONT2,
    stroke_width=3,
    stroke_fill=(68, 68, 68),
    fill=fill,
)


p, t1, t2 = img.load(), textimg1.load(), textimg2.load()


bgfunc = lambda x, y: ((x | y) % 191 + 64,) * 3 + (255,)

logging.info("Rendering the background..")
for x in range(W):
    for y in range(H):
        p[x, y] = bgfunc(x, y)

rand1 = random.Random()
rand1.seed(6969)
textimg3 = newimg()
draw3 = ImageDraw.Draw(textimg3)
w, h = draw3.textsize("1\n7\n2\n9", font=FONT3)

draw3.text((-150, (H - h) // 2), "1\n7\n2\n9", font=FONT3, fill=fill)
# draw3.text((rand1.randint(0, 3000), rand1.randint(0, 3000)), "", font=FONT3, fill=fill)
# draw3.text((rand1.randint(0, 3000), rand1.randint(0, 3000)), "1729", font=FONT3, fill=fill)

textimg3b = newimg()
t3bp = textimg3b.load()
for x in range(W):
    for y in range(H):
        t3bp[x, y] = (20, (x | y) % 200 + 55, 20, 180)

textimg3 = Image4Layer.multiply(textimg3, textimg3b)

img = Image4Layer.hard_light(img, textimg3)

logging.info("Pasting the image..")
rmjn2 = newimg()
rmjn2.paste(
    rmjn, (int((W - rmjn.width) / 2), 480), rmjn.filter(ImageFilter.GaussianBlur(20))
)
r = rmjn2.load()
img = Image4Layer.darken(img, rmjn2)
p = img.load()
# for x in range(W):
#    for y in range(H):
#        p[x, y] = tuple((c1 + c2) // 255 for c1, c2 in zip(p[x, y], r[x, y]))

t1func = lambda x, y: (90, (x ** 2 | y) % 200 + 55, 80, 255)
t2func = lambda x, y: (38, (x | y ** 2) % 75, 150, 255)

logging.info("Rendering the text..")
img.paste(i := textimg1.filter(ImageFilter.GaussianBlur(5)), (0, 0), i)
img.paste(i := textimg2.filter(ImageFilter.GaussianBlur(5)), (0, 0), i)
for x in range(W):
    for y in range(H):
        if t1[x, y][-1] == 0:
            pass
        elif t1[x, y] == (255, 255, 255, 255):
            p[x, y] = t1func(x, y)
        else:
            p[x, y] = t1[x, y]

        if t2[x, y][-1] == 0:
            pass
        elif t2[x, y] == (255, 255, 255, 255):
            p[x, y] = t1func(x, y)
        else:
            p[x, y] = t2[x, y]

img = ImageGlitcher().glitch_image(img, 2, color_offset=True, seed=5363)
# img.paste(rmjn, (W / 2, 300), rmjn)

logging.info("Saving the image..")
img.save("rendered.png", "PNG")
logging.info("Done!")
