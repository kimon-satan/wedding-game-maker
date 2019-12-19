#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math

phrases = [
"Splendid occasion",
"Marvellous occasion",
"Outstanding occasion",
"Outstanding champagne",
"Just a little more champagne ?",
"I always appreciate a good champagne",
"I always appreciate a good wedding",
"The flowers ! What wonderful flowers",
"Doesn't the bride look magnificent",
"The groom is simply charming",
"What a glamorous outfit",
"My my don't you look dapper",
"What ?",
"Can you speak a little louder ?",
"Isn't it very noisy in here"
]

phrase_x = "but I do wonder when we'll be eating..."

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def centerText(text, font, w):
    s = font.getsize(text)
    return (w - s[0])/2

def wrapText(text, font, w):
    s = font.getsize_multiline(text)
    best_text = text
    best_size = s[0]
    s_indexes = list(find_all(text, " "))
    if s[0] <= w:
        return text

    for i in reversed(s_indexes):
        t_text = text[:i] + "\n" + text[i+1:]
        s = font.getsize_multiline(t_text)
        if s[0] < w:
            return t_text
        elif s[0] < best_size:
            best_text = t_text
            best_size = s[0]
    print(best_text)
    return wrapText(best_text, font, w)



print('Wedding game maker !')

res = 1000
width = math.floor(1.4142857 * res)
height = res
im  = Image.new('RGB', (width,height), (255,255,255));

# get a drawing context
draw = ImageDraw.Draw(im)




# get a font
title_fnt = ImageFont.truetype('./Chocolat.ttf', 100)
normal_fnt = ImageFont.truetype('./Alice-regular.ttf', 35)
normal_size = 35

# draw text, half opacity

opener = phrases[0]

draw.text((10,10), "Simon and Marguerite's\nConversation Piece", font=title_fnt, fill=(0))

o = centerText("Opener: " + opener, normal_fnt ,width/2)
draw.text((o + width/2 ,20), "Opener: " + opener, font=normal_fnt, fill=(0))

table_top = height/8
table_bottom = height * 15/16

draw.line((width/2, 0, width/2, height), fill=100)
draw.line((width * 3/4, table_top, width * 3/4, table_bottom), fill=0)

o = centerText("They say", normal_fnt, width/4)
draw.text((width/2 + o,table_top), "They say", font=normal_fnt, fill=(0))
o = centerText(" ... you say", normal_fnt, width/4)
draw.text((width * 3/4 + o,table_top), " ... you say", font=normal_fnt, fill=(0))

draw.line((width/2, table_top + normal_size, width, table_top + normal_size), fill=100)

#draw the they say phrases
running_y = table_top + normal_size
offset_x = 10

for i in range(0,6):
    t = wrapText(phrases[i], normal_fnt, width/4 - offset_x * 2)
    s = normal_fnt.getsize_multiline(t)
    v = s[1]
    draw.text((width/2 + offset_x,running_y), t, font=normal_fnt, fill=(0))
    t = wrapText(phrases[i+1], normal_fnt, width/4 - offset_x * 2)
    s = normal_fnt.getsize_multiline(t)
    v = max(s[1], v)
    draw.text((width *3/4 + offset_x,running_y), t, font=normal_fnt, fill=(0))
    running_y += v + normal_size
    draw.line((width/2, running_y, width, running_y), fill=100)


t = wrapText(phrase_x, normal_fnt, width/4 - offset_x * 2)
draw.text((width/2 + offset_x,running_y), t, font=normal_fnt, fill=(0))
t = wrapText("Well I've heard that you're sitting on table " + str(4), normal_fnt, width/4 - offset_x * 2)
draw.text((width * 3/4 + offset_x,running_y), t, font=normal_fnt, fill=(0))


im.show();



# write to stdout
# im.save(sys.stdout, "PNG")
