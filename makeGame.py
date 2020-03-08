#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math
from random import randint
from random import shuffle
import json
import re

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

	s_indexes = list(find_all(text, " "))
	if s[0] <= w:
		return text

	for i in reversed(s_indexes):
		t_text = text[:i] + "\n" + text[i+1:]
		s = font.getsize_multiline(t_text)
		s_line = font.getsize(text[:i])
		if s[0] < w:
			return t_text
		elif s_line[0] < w:	#TODO finish this
			t_text = text[:i]
			r_text = text[i+1:]
			break

	return t_text + "\n" + wrapText(r_text, font, w)


def choose(items):
	i = randint(0, len(items)-1)
	return items[i]

#################################### DRAWING ####################################

def drawMappings(draw, table):
	table_top = height/8
	table_bottom = height * 7/8

	draw.line((width/2, 0, width/2, height), fill=100)
	draw.line((width * 3/4, table_top, width * 3/4, table_bottom), fill=0)

	o = centerText("They say", normal_fnt, width/4)
	draw.text((width/2 + o,table_top - 10), "They say", font=normal_fnt, fill=(0))
	o = centerText(" ... you say", normal_fnt, width/4)
	draw.text((width * 3/4 + o,table_top - 10), " ... you say", font=normal_fnt, fill=(0))

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

	e = centerText("Excuse: " + table["excuse"], normal_fnt ,width/2)
	draw.text((e + width/2 ,table_bottom + 10), "Excuse: " + table["excuse"], font=normal_fnt, fill=(0))


#################################### MAIN ####################################

def drawCardInner(person, table):

	#prepare the image
	im  = Image.new('RGB', (width,height), (255,255,255))

	# get a drawing context
	draw = ImageDraw.Draw(im)


	v = 10

	### instructions

	for line in instructions:
		wrapped = wrapText(line,normal_fnt,width * 7/16)

		draw.text((width/32,v),wrapped,font=normal_fnt, fill=(0))
		s = normal_fnt.getsize_multiline(wrapped)
		v += s[1] + 20


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
#title_fnt = ImageFont.truetype('fonts/Chocolat.ttf', 100)
normal_fnt = ImageFont.truetype('fonts/victoria.ttf', 35)
normal_size = 35


with open('defs.json') as json_file:
	data = json.load(json_file)

with open('people.json') as json_file:
	people = json.load(json_file)

with open('instructions.txt', "r") as txt_file:
	instructions = []
	for line in txt_file:
		line = re.sub('\n$', '',line)
		instructions.append(line)

for p in people:
	d = data["tables"][p[1] - 1]
	drawCardInner(p[0],d)

exit()
