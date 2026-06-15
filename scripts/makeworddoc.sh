pandoc --wrap=preserve $1 -f markdown+hard_line_breaks -o $2
echo "$2 created."
