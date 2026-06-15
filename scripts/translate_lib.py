def read_file_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # .read().splitlines() is often preferred over .readlines() 
            # because it automatically removes the newline character (\n)
            lines = file.read().splitlines()
        return lines
    except FileNotFoundError:
        return "Error: The file was not found."

def split_into_chapters(lines, delimiter="# "):
    chapters = []
    current_chapter = []

    for line in lines:
        # Check if the line starts with or contains the delimiter
        if delimiter in line.lower():
            # If we already have content in current_chapter, save it before starting a new one
            if current_chapter:
                chapters.append(current_chapter)
            # Start a new sub-list with the delimiter line
            current_chapter = [line]
        else:
            current_chapter.append(line)

    # Append the last chapter if it contains any lines
    if current_chapter:
        chapters.append(current_chapter)

    return chapters

def merge_chapter_files(source_list, chapter_lines,key="<CHAPTER START>"):
  
        # Find the index of the 1st line starting with the key
        split_index = -1
        for i, line in enumerate(source_list):
            if line.strip().startswith(key):
                split_index = i
                break
        
        if split_index == -1:
            return "Error: <CHAPTER START> tag not found in source file."

        # Construct the output list:
        # 1. Source lines up to and including the tag (split_index + 1)
        # 2. All lines from the second file
        # 3. Remaining lines from the first file
        output = source_list[:split_index + 1] + chapter_lines + source_list[split_index + 1:]
        
        return output

def merge_chapter_files2(source_list, chapter_lines,key="<CHAPTER START>",OCC=1):
  
        # Find the index of the line starting with <CHAPTER START>
        occurrence = 0
        split_index = -1
        for i, line in enumerate(source_list):
            if line.strip().startswith(key):
                occurrence = occurrence + 1
                
                if occurrence == OCC:
                    split_index = i
                    break
                pass
        
        if occurrence!=OCC:
            return "Error: <CHAPTER START> tag not found in source file."

        # Construct the output list:
        # 1. Source lines up to and including the tag (split_index + 1)
        # 2. All lines from the second file
        # 3. Remaining lines from the first file
        output = source_list[:split_index + 1] + chapter_lines + source_list[split_index + 1:]
        
        return output
def list_to_text_file(lines, output_filename):
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for line in lines:
                # We add \n to ensure each item in the list 
                # starts on a new line in the text file
                f.write(f"{line}\n")
        print(f"Successfully created {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_text_block(text: str) -> str:
    """Extracts text between ```text and the next ```."""
    start_marker = "```text\n"
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

