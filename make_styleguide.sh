echo "Automated Styleguide Generator"
format_time() {
  ((h=${1}/3600))
  ((m=(${1}%3600)/60))
  ((s=${1}%60))
  printf "%02d:%02d:%02d\n" $h $m $s
 }

python scripts/generate_style_guide.py

echo "Completed in $(format_time $SECONDS)"
