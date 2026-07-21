echo "Automated Translation Task"
format_time() {
  ((h=${1}/3600))
  ((m=(${1}%3600)/60))
  ((s=${1}%60))
  printf "%02d:%02d:%02d\n" $h $m $s
 }
echo "Pass 2 Initial Translation with prompt caching"
python scripts/Check_manuscript.py
python scripts/translate_cache_prompt.py
python scripts/multiprompt_async_cache.py "translate_prompt_file_ch" "AI_response" "02Translate" 1 1
python scripts/multiprompt_async_cache.py "translate_prompt_file_ch" "AI_response" "02Translate" 2 1

echo "Tanslation using concurrent API completed."
python scripts/Parse_translation.py
python scripts/merge_translation.py
echo "Pass 3 Translation Accuracy Check with prompt caching"
python scripts/acc_check_cache_prompt.py
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 1 1
python scripts/multiprompt_async_cache.py "acc_check_prompt_file_ch" "AI_response" "03Check" 2 1

echo "Accuracy Check using concurrent API completed."
python scripts/Parse_check.py
python scripts/merge_check.py
echo "Pass 4 Line editing with prompt caching"
python scripts/line_edit_cache_prompt.py
python scripts/multiprompt_async_cache.py "line_edit_prompt_file_ch" "AI_response" "04Edit" 1 1
python scripts/multiprompt_async_cache.py "line_edit_prompt_file_ch" "AI_response" "04Edit" 2 1
echo "Line Edit using concurrent API completed."
python scripts/Parse_edit.py
python scripts/merge_edit.py
echo "Generation of final documents"
./scripts/makeworddoc.sh 04Edit/LineEdited.md 04Edit/LineEdited.docx
cp 04Edit/LineEdited.docx LineEdited.docx
cp 02Translate/log.txt 02Log.txt
cp 03Check/log.txt 03Log.txt
cp 04Edit/log.txt 04Log.txt
echo "Translation completed in $(format_time $SECONDS)"
