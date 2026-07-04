#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 06:49:09 2026
@author: alan
Do some basic checks on the source manuscript
"""
import os
from pathlib import Path
from translate_lib import *
import json

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)


# Make sure the  manuscript sub directory exists and contains a single markdown file

target_dir = Path.cwd() / "manuscript"
if not target_dir.exists():
    print("Error: The 'manuscript' subdirectory does not exist.")
elif not target_dir.is_dir():
    print("Error: 'manuscript' exists but it is a file, not a directory.")
else:
    # Find all .md files in that directory
    # (glob matches files; we use lower case, but it's case-insensitive on Windows)
    md_files = list(target_dir.glob("*.md"))
    
    # Verify that there is exactly one markdown file add add its name to the json index
    if len(md_files) == 1:
        markdown_filename= md_files[0]
        print(f"Success! Found exactly one Markdown file: '{markdown_filename.name}'")
        if markdown_filename.name != msfile:
            config["msfile"] = "manuscript/"+markdown_filename.name
            config["chcount"] = len(split_into_chapters(read_file_to_list(config["msfile"])))
            with open("config.json", "w") as file:
               json.dump(config, file, indent=4)
            print(f" Config updated with manuscript at {config["msfile"] } with {config["chcount"] } chapters ")
