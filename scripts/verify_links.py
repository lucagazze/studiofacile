import re
import os

with open('libri.html', 'r', encoding='utf-8') as f:
    html = f.read()

sources = re.findall(r'src=["\']([^"\']+)["\']', html)
for s in sources:
    if not s.startswith('http') and not s.startswith('//'):
        exists = os.path.exists(s)
        print(f"SRC: {s} -> Exists: {exists}")

preview_imgs = re.findall(r"'([a-zA-Z0-9_]+\.webp)'", html)
for p in set(preview_imgs):
    path = os.path.join('amostras/ebooks', p)
    print(f"PREVIEW: {path} -> Exists: {os.path.exists(path)}")

print("All validations completed.")
