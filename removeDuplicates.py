import os
import glob
import re

folder_path = '_posts/'
files = glob.glob(os.path.join(folder_path, '*.md'))
unique_words = set()
pattern = re.compile(r'^\d{4}-\d{2}-\d{2}-(.*)\.md$')

for file in files:
    match = pattern.match(os.path.basename(file))
    if match:
        word = match.group(1)
        if word not in unique_words:
            unique_words.add(word)
        else:
            os.remove(file)
