#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math
from random import randint
from random import shuffle
import json

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

#################################### HELPER FUNCTIONS ####################################


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
    return wrapText(best_text, font, w)

def choose(items):
    i = randint(0, len(items)-1)
    return items[i]

#################################### DRAWING ####################################

def drawMappings(draw, table):
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

    #mappings
    keys = list(table["mappings"].keys())
    keys = list(keys)
    shuffle(keys)

    for i in keys:
        t = wrapText(data["phrases"][i], normal_fnt, width/4 - offset_x * 2)
        s = normal_fnt.getsize_multiline(t)
        v = s[1]
        draw.text((width/2 + offset_x,running_y), t, font=normal_fnt, fill=(0))
        if i == "x":
            answer = "Well I've heard that you're sitting on table " + str(table["mappings"]["x"])
        else:
            answer = table["mappings"][i]
            if isinstance(answer, list):
                answer = choose(answer)
            answer = data["phrases"][answer]
        t = wrapText(answer, normal_fnt, width/4 - offset_x * 2)
        s = normal_fnt.getsize_multiline(t)
        v = max(s[1], v)
        draw.text((width *3/4 + offset_x,running_y), t, font=normal_fnt, fill=(0))
        running_y += v + normal_size
        draw.line((width/2, running_y, width, running_y), fill=100)

    draw.text((width/2 + offset_x,running_y), " ? ? ? ", font=normal_fnt, fill=(0))
    t = wrapText(table["excuse"], normal_fnt, width/4 - offset_x * 2)
    draw.text((width *3/4 + offset_x,running_y), t, font=normal_fnt, fill=(0))

#################################### MAIN ####################################

def drawCard(person, table):

    #prepare the image
    im  = Image.new('RGB', (width,height), (255,255,255))

    # get a drawing context
    draw = ImageDraw.Draw(im)


    ### title page and instructions
    v = 10
    t1 = "Simon and Marguerite's"
    o = centerText(t1, normal_fnt,width/2)
    draw.text((o,v), t1,font=normal_fnt, fill=(0))
    s = normal_fnt.getsize(t1)
    v += s[1]

    t2 = "Conversation Piece"
    o = centerText(t2, title_fnt,width/2)
    draw.text((o,v), t2, font=title_fnt, fill=(0))
    s = title_fnt.getsize(t2)
    v += s[1]
    o = centerText(person, normal_fnt ,width/2)
    draw.text((o,v), person, font=normal_fnt, fill=(0))
    s = normal_fnt.getsize(t2)
    v += s[1] + 20

    ### instructions

    draw.text((10,v),instructions,font=small_fnt, fill=(0))


    ### second page
    opener = data["phrases"][table["opener"]]
    o = centerText("Opener: " + opener, normal_fnt ,width/2)
    draw.text((o + width/2 ,20), "Opener: " + opener, font=normal_fnt, fill=(0))

    drawMappings(draw, table)


    im.save("./output/" + person, "PNG")

################################################################################

print('Wedding game maker !')

res = 1000
width = math.floor(1.4142857 * res)
height = res

# get a font
title_fnt = ImageFont.truetype('./Chocolat.ttf', 100)
normal_fnt = ImageFont.truetype('./Alice-regular.ttf', 35)
small_fnt = ImageFont.truetype('./Alice-regular.ttf', 25)
normal_size = 35

with open('defs.json') as json_file:
    data = json.load(json_file)

with open('people.json') as json_file:
    people = json.load(json_file)

with open('instructions.txt', "r") as txt_file:
     instructions = txt_file.read()

for p in people:
    d = data["tables"][p[1] - 1]
    drawCard(p[0],d)
