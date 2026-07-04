#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 06:49:09 2026

@author: alan
"""
from translate_lib import *
import json

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)
#### parameters

msfile = config["msfile"]
template_file = config["03_template_file"]
style_file = config["style_file"]
prompt_prefix = config["03_prompt_prefix"]
FRfile =config["02DESTINATION"]

file_content = read_file_to_list(msfile)
chapter = split_into_chapters(file_content)
nchs= len(chapter) # no of source chapters found
fr_content = read_file_to_list(FRfile)
chapter = split_into_chapters(fr_content)
nch = len(chapter) # no of target chapters found

print(f"{nch} translated chapters  {nchs} source chapters")


if nchs == nch:

    chapter = split_into_chapters(file_content)
    FRchapter = split_into_chapters(fr_content)
    style_list= read_file_to_list(style_file)
    template = read_file_to_list(template_file)

    for i in range(nch):
        prompt = merge_chapter_files(template, style_list,key="PROJECT STYLE SHEET")
        prompt = merge_chapter_files2(prompt, chapter[i],key="<CHAPTER START>",OCC=1)
        prompt = merge_chapter_files2(prompt, FRchapter[i],key="<CHAPTER START>",OCC=2)
        list_to_text_file(prompt, prompt_prefix+str(i+1)+'.txt')

else:
    print(f" No of source and target chapters do not match in Acc Check stage")
    
