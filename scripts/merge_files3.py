import os
import re

# ================= CONFIGURATION =================
# Change these two variables to fit your needs:
FILE_PREFIX = "acc_check_response_file_ch"  # The part before the number (e.g., "chapter_")
DESTINATION = "AccChecked.md" # The name of the resulting file
# =================================================

def natural_sort_key(s):
    """Sorts strings containing numbers in logical order (1, 2, 10)."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def main():
    # Dynamic regex based on your FILE_PREFIX
    # Matches: PREFIX + digits + .md
    pattern = re.compile(rf'^{re.escape(FILE_PREFIX)}(\d+)\.md$')
    
    # Identify matching files in the current directory
    matched_files = [f for f in os.listdir('.') if pattern.match(f)]
    
    if not matched_files:
        print(f"No files found matching pattern: {FILE_PREFIX}n.md")
        return

    # Sort files numerically
    matched_files.sort(key=natural_sort_key)

    print(f"Found {len(matched_files)} files. Merging into '{DESTINATION}'...")

    try:
        with open(DESTINATION, 'w', encoding='utf-8') as outfile:
            for filename in matched_files:
                with open(filename, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    # Ensures a clean break between concatenated files
                    outfile.write("\n\n")
                print(f"  > Integrated {filename}")
        
        print(f"\nDone! File created at: {os.path.abspath(DESTINATION)}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

