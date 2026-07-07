import os
from dotenv import load_dotenv
import litellm
import json

# load the configuration settings
with open("config.json", mode="r", encoding="utf-8") as read_file: config = json.load(read_file)
globals().update(config)
MODELS_TO_USE = [
        "gemini/gemini-2.5-flash",
        "openai/gpt-4o",
        "anthropic/claude-sonnet-4-6"
        ]
model = MODELS_TO_USE[modelnumber]
# 1. Load environment variables from the .env file
load_dotenv()

# Verify API key is present
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("Missing ANTHROPIC_API_KEY in environment or .env file.")

# Define input and output file paths
TEMPLATE_PATH = config["_05_template_file"]       # Your style guide template structure
MANUSCRIPT_PATH = config["_04DESTINATION"]   # Your markdown file
OUTPUT_PATH = config["_05DESTINATION"] # The final generated report
STYLE_PATH = config["style_file"] # The style guide to use

def read_file(file_path):
    """Safely reads text content from a local file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        exit(1)

def write_file(file_path, content):
    """Writes the generated string output into a text file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Success! Report generated and saved to: {file_path}")

def main():
    print("Reading input files...")
    template_content=read_file(TEMPLATE_PATH)
    style_content = read_file(STYLE_PATH)
    manuscript_content = read_file(MANUSCRIPT_PATH)
    
    # 2. Build a structured user prompt injecting both files
    print("Constructing prompt ...")
    user_prompt = f"""
You are an expert translation editor. 
Your task is to follow the instructions in the template 
<template>
{template_content}
</template>
Here is the Style Guide Template structure you MUST follow:
<styleguide>
{style_content}
</styleguide>

Here is the Manuscript text to analyze:
<manuscript>
{manuscript_content}
</manuscript>

Please return ONLY the text report. Do not include introductory text or markdown conversational filler outside of the template structure.
"""

    # 3. Call Claude via LiteLLM 
    # Using 'anthropic/claude-3-5-sonnet-20241022' for deep linguistic analysis.
    # Adjust max_tokens if your target template requires a massive output layout.
    print("Sending request to Claude via LiteLLM...")
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            max_tokens=4000, 
            temperature=0.2 # Lower temperature forces analytical consistency
        )
        
        # 4. Extract and save the results
        generated_guide = response.choices[0].message.content
        write_file(OUTPUT_PATH, generated_guide)
        
    except Exception as e:
        print(f"An error occurred during API execution: {e}")

if __name__ == "__main__":
    main()
