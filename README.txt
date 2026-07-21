This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Install python from www.python.org and its libraries litellm and dotenv
(use "pip install litellm" and "pip install dotenv" at the command prompt)
Install pandoc from www.pandoc.org

Add the manuscript to be translated to the "manuscript" directory.
Make sure it is in markdown format and the filename ends ".md".
Also make sure all chapters start "# <chapter name>" and there are no
lines before the first chapter.

Add "styleguide.txt" to the 01Style directory.

Add the files "Translation_template.txt", "Acccheck_template.txt" and "LineEdit_template.txt"files for the particular language combination to the "scripts" directory as per the SPS course to the scripts directory.

Add the API key to the .env file using the syntax ANTHROPIC_API_KEY=<your key>
where <your key> can be downloaded from the claude.platform dashboard once you have
a developer account set up.

In the command files tune the concurrency and cycles to match your particular claude rate limits.
For example python scripts/multiprompt_async.py "translate_prompt_file_ch" "AI_response" "02Translate" 3 1

The fist number (3) is the number of concurrent chapters to submit and the second (1) is the number of times to cycle the submission requests, The product of these two numbers should be greater than the number of chapters. We have sucessfully used concurrency of 6 or 13 with moderate rate limits.
There are three instances of these lines to be tuned.

Run the command file "startup.sh" (Linux) or "startup.cmd" (Windows)
That will run through all of the passes of the translation and copy the final word document to the top level directory.

If you want to rerun the translation just delete the contents of 02Translate,03Check and 04Edit and rerun the command file.

Caching

  To implement prompt caching as an experiment I have included startup_cache.sh,translate_cache_prompt.py,acc_check_cache_prompt.py,line_edit_cache_prompt.py and multiprompt_async_cache.py - the original files are unchanged and can still be used.
  The method combines template and style guide into system instructions and then tags them for caching as they dont change between chapters. The source text chapters are still loaded as user instructions as before.
   
