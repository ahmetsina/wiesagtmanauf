#!/usr/bin/env python3


import openai
import re
import datetime
from PIL import Image, ImageDraw, ImageFont
import random
import yaml

## Open AI 
openai.api_key = "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"

# create a completion
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                          messages=[{"role": "user",
                                                     "content": "Choose a random german word. And write a jekyll post about its definitions, oppositites or synonyms and examples. And make it markdown with yaml post structrute on the head. On the head must inclueded: layout as post, categories and tags must in brackets, title must be only word"}])

# print the completion
content = completion.choices[0].message.content

today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')

match = re.search(r'^title:\s+("?)(.+?)\1$',content, re.MULTILINE)

def first_word(words_tuple):
    return re.match(r'\W*(\w[^,. !?"]*)', words_tuple).groups()[0]


def create_image(text):
    # Define image dimensions and mesh gradient parameters
    width, height = 730, 383
    num_steps = 50

    # Define a list of colorful and light colors
    colors = [(92, 65, 93), (46, 196, 182), (9, 82, 86), (157, 193, 211), (94, 124, 226), (21, 113, 69), (96, 105, 92), (17, 75, 95), (11, 110, 79)]

    # Select a random color from the list to use as the background
    background_color = random.choice(colors)

    # Create a new image with a solid color background
    img = Image.new('RGB', (width, height), background_color)

    # Add custom text on top of the solid color background
    font = ImageFont.truetype("assets/Roboto-Bold.ttf", 48, encoding="unic")
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    text_x, text_y = (width - text_width) // 2, (height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    # Save the image
    word = first_word(text)
    path = "assets/images/posts/" + word + ".png"
    img.save(path)
    return path


def manipulate(content, image_path):
    return insertAfter(content, "layout: post", "\nimage: " + image_path)

def insertAfter(haystack, needle, newText):
  i = haystack.find(needle)
  return haystack[:i + len(needle)] + newText + haystack[i + len(needle):]


if match:
    matched_title = match.group(2)
    title = re.sub(r'[\s?-?].+',"", matched_title)    
    dash_replaced_title = title.replace(" ", "-").replace(",","").replace("---","-").replace("--","-").replace("---","-")
    title_md = (dash_replaced_title + ".md").lower()
    file_title = formatted_date + "-" + title_md
    print(file_title)
    aussprache = f"\ <a id=\"yg-widget-0\" class=\"youglish-widget\" data-query=\"{title}\" data-lang=\"german\" data-components=\"8412\" data-auto-start=\"0\" data-bkg-color=\"theme_light\" data-title=\"How%20to%20pronounce%20{title}%20in%20German\"  rel=\"nofollow\" href=\"https://youglish.com\">Visit YouGlish.com</a><script async src=\"https://youglish.com/public/emb/widget.js\" charset=\"utf-8\"></script>"
    image_path = create_image(dash_replaced_title)
    modified_yaml = manipulate(content + aussprache, image_path)
    f = open("_posts/" + file_title, "a")
    f.write(modified_yaml)
    f.close()
else:
    print('Title not found')


