# -*- coding: utf-8 -*-
#
#  Script to submit a chapter for translation and record associated notes.
#



import os
from time import time
from translate_lib import *
import json

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)
#### parameters

msfile = config["msfile"]
template_file = config["04_template_file"]
style_file = config["style_file"]
prompt_prefix = config["04_prompt_prefix"]

FRfile =config["03_chapter"]
############### main Prog ####################################
logfile = config["03logfile"]
ch = config["chcount"]
infile = []
outfile = []
outname = []
for i in range(ch):
   infile.append(f"{config['03_response']}{i+1}.txt")
   outfile.append(f"{config['03_chapter']}{i+1}.md")                            
   outname.append(f"\nChapter {i+1}\n")


   
for fileio in range(ch):
    
   with open(infile[fileio],'r') as f:
        output = f.read()

    # store fenced code block in the output file
   with open(outfile[fileio],'w') as f:
         f.write(str(extract_text_block(output)))
    # Add notes to the log file    
   with open(logfile,'a') as f:
        f.write(str(outname[fileio] + get_text_after_second_marker(output)))    
    
print("All files parsed and log created")  
    
