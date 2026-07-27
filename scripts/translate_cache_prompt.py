#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 06:49:09 2026

@author: alan
"""

from translate_lib import *
import json
import sys

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)
#### parameters

msfile = config["msfile"]
template_file = config["_02_template_file"]
style_file = config["style_file"]
prompt_prefix = config["_02_prompt_prefix"]

try:
    file_content = read_file_to_list(msfile)
    chapter = split_into_chapters(file_content)
    nch = len(chapter) # no of chapters found
    if nch != config["chcount"]:
        print(f" Input chapter count does not match config entry")
        sys.exit(1)
    print(f"{nch} Chapters found")
    template = read_file_to_list(template_file)
    style_list= read_file_to_list(style_file)
except:
    print(f"Unable to load and split manuscript")
    sys.exit(2)

try:    
    prompt = merge_chapter_files(template, style_list,key="PROJECT STYLE SHEET")
    list_to_text_file(prompt, 'sys.txt') # save the template and style guide for caching
except:
    print(f"Unable to create template & style guide for caching")
    sys.exit(3)
    
header = ["use the system instructions on the attached CHAPTER\n","<CHAPTER START>"]
try:
    for i in range(nch): # iterate over all of the chapters
        
        prompt = merge_chapter_files(header, chapter[i],key="<CHAPTER START>")
        list_to_text_file(prompt, prompt_prefix +str(i+1)+'.txt')
        print(f"{prompt_prefix +str(i+1)+'.txt'} generated")
except:
        print(f"Unable to create the prompt files")
        sys.exit(4)
sys.exit(0)    
    

