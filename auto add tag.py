from bs4 import BeautifulSoup
import os

def should_wrap(text):
    if not text.strip():
        return False
    if '{%' in text or '{{' in text:
        return False
    if '{% trans' in text or '{% blocktrans' in text:
        return False
    return True

def wrap_trans_in_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    changed = False

    for element in soup.find_all(text=True):
        if element.parent.name in ['script', 'style']:
            continue
        if should_wrap(element):
            text = element.strip()
            element.replace_with('{% trans "' + text + '" %}')
            changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

# Quét thư mục template
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            wrap_trans_in_html(os.path.join(root, file))
