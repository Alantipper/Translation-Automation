# -*- coding: utf-8 -*-
#
#################################################################
#
#           python multiprompt_async.py     source target concur cycles
#
#           manage multiple concurrent AI prompts
#            'concur'  tasks are launched per cycle
#            repeated for 'cycles' cycles with a 60 sec pause between cycles.
#            prompts are fetched from <source>n.txt and responses sent to <target>n.txt
#            where n is an integer up to 100
#
#             The next 'concur' tasks are run from source files without matching target files.
#              ANTHROPIC_API_KEY must be assigned in a .env file in the current working directory
##################################################################

import sys
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from litellm import acompletion
import asyncio
import time
import json

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)

# Check if an argument was actually passed
if len(sys.argv) == 6:
    source = sys.argv[1]
    target =  sys.argv[2]
    folder = sys.argv[3]
    concur = int(sys.argv[4])
    cycles = int(sys.argv[5])
else:
    print("Running with default arguments")
    source = "acc_check_prompt_file_ch"
    target  = "AI_response_trial"
    concur = 5
    cycles = 1

load_dotenv() # load the environment variables containing AI API keys




# utility functions

def extract_text_block(text: str) -> str:
    """Extracts text between ```text and the next ```."""
    start_marker = "```text"
    end_marker = "```"
    
    # Find where the starting marker begins
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return ""  # Marker not found
        
    # Move the index to the end of the "```text" marker
    content_start = start_idx + len(start_marker)
    
    # Find the next "```" closing marker after the starting point
    end_idx = text.find(end_marker, content_start)
    if end_idx == -1:
        return text[content_start:]  # If no closing marker, return everything until the end
        
    return text[content_start:end_idx]


def get_text_after_second_marker(text: str) -> str:
    """Returns all text after the second occurrences of '```' up to the end."""
    # Split the string a maximum of 2 times using the delimiter
    parts = text.split("```", 2)
    
    # If there are fewer than 3 parts, the second marker does not exist
    if len(parts) < 3:
        return ""
        
    # The third element (index 2) contains everything after the second marker
    return parts[2]

def get_next_unexecuted_files(m: int, directory: str = ".") -> list:
    """
    Returns the next 'm' input file names that have not been executed yet.
    
    :param m: Number of unexecuted files to return.
    :param directory: The directory where the input and output files are located.
    :return: A list of file names (e.g., ['input_ch3.txt', 'input_ch4.txt'])
    """
    # 1. Find all existing output files and extract their character/integer IDs
    executed_ids = set()
    try:
        for filename in os.listdir(directory):
            if filename.startswith(target) and filename.endswith(".txt"):
                # Extract 'x' from 'AI_responsex.txt'
                parts = filename.replace(target, "").replace(".txt", "")
                if parts.isdigit():
                    executed_ids.add(int(parts))
    except FileNotFoundError:
        print(move_to_end=f"Directory '{directory}' not found.")
        return []

    # 2. Iterate through possible IDs (1 to 100) to find unexecuted ones
    next_inputs = []
    next_outputs =[]
    for x in range(1, 101):
        if x not in executed_ids:
            input_filename = f"{source}{x}.txt"
            
            # Optional: Check if the input file actually exists before suggesting it
            if os.path.exists(os.path.join(directory, input_filename)):
                next_inputs.append(input_filename)
                next_outputs.append(f"{target}{x}.txt")
        
        # Stop once we have found 'm' files
        if len(next_inputs) == m:
            break
            
    return next_inputs,next_outputs

############### co-function to run one instance of AI prompt ####################################
async def submit_prompt(sysfile,userfile,outfile,model):
    # Assemble style guide and task definition
    with open(sysfile,'r') as f:
        SYSTEM_INSTRUCTIONS = f.read()  # any common instructions

    with open(userfile,'r') as f:
        USER_INSTRUCTIONS = f.read()    # specific task
        
    
    print(f"🤖 Running model: {model}...") # define model

    try:
        response =  await acompletion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": USER_INSTRUCTIONS}
            ],
            # Optional parameters like temperature can go here
            temperature=0.2 
        )
        
        # LiteLLM standardizes the response format so this works for ALL models
        output = response.choices[0].message.content
        
        # store fenced code block in the output file
##        with open(outfile,'w') as f:
##            f.write(str(extract_text_block(output)))
##        # Add notes to the log file    
##        with open(logfile,'a') as f:
##            f.write(str(outname + get_text_after_second_marker(output)))    
        with open(outfile,'w') as f:
             f.write(str(output))
             
        #print(f"✨ Result from {model}:\n{output}\n")
        print(f"💰 Tokens used: {response.usage.total_tokens}\n{'-'*50}\n")
        
    except Exception as e:
        print(f"❌ Failed to run {model}. Error: {e}\n{'-'*50}\n")
################### Main ###################################
async def main():
    start_time = time.time()
    results= []
    async with asyncio.TaskGroup() as tg:
      for i in range(len(userfile)):
        print(f"Starting task input = {userfile[i]}  output = {outfile[i]}")
        results = tg.create_task(submit_prompt(sysfile,folder+'/'+userfile[i],folder+'/'+outfile[i],model))
      
    mins = (time.time()-start_time)/60
    print(f"Total execution time {time.time()-start_time:.2f} seconds")

#####################################################    
sysfile = "sys.txt"


for it in range(cycles):
    userfile,outfile = get_next_unexecuted_files(concur,folder)
    print(f"Iteration {it}")
    MODELS_TO_USE = [
        "gemini/gemini-2.5-flash",
        "openai/gpt-4o",
        "anthropic/claude-sonnet-4-6"
        ]
    model = MODELS_TO_USE[modelnumber]
    if len(userfile) != 0:
        asyncio.run(main())
        time.sleep(40)  
    
print(f"Completed AI tasks")

