@echo off
echo "Automated Translation Task with Prompt Caching"

echo "Pass 2 Initial Translation"
python scripts/Check_manuscript.py
python scripts/translate_cache_prompt.py
python scripts/multiprompt_async_cache.py "translate_prompt_file_ch" "AI_response" "02Translate" 1 1
python scripts/multiprompt_async_cache.py "translate_prompt_file_ch" "AI_response" "02Translate" 2 1
echo "Tanslation using concurrent API completed."
python scripts/acc_check_cache_prompt.py
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 1 1
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 2 1
echo "Pass 3 Translation Accuracy Check"
python scripts/acc_check_cache_prompt.py
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 1 1
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 2 1
echo "Accuracy Check using concurrent API completed."
python scripts/Parse_check.py
python scripts/merge_check.py
echo "Pass 4 Line editing"
python scripts/line_edit_prompt.py
python scripts/multiprompt_async.py "line_edit_prompt_file_ch" "AI_response" "04Edit" 2 2
echo "Line Edit using concurrent API completed."
python scripts/Parse_edit.py
python scripts/merge_edit.py
echo "Generation of final documents"
./scripts/makeworddoc.sh 04Edit/LineEdited.md 04Edit/LineEdited.docx
cp 04Edit/LineEdited.docx LineEdited.docx
cp 02Translate/log.txt 02Log.txt
cp 03Check/log.txt 03Log.txt
cp 04Edit/log.txt 04Log.txt
echo "Done"
