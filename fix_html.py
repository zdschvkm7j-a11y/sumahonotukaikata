from pathlib import Path
import re

root = Path(r'c:\Users\katsuyoshi\Desktop\新しいフォルダー (3)')
replacements = [
    ("text ; '説明を待っています'", "text || '説明を待っています'"),
    ("text ; '説明を待っています';", "text || '説明を待っています';"),
    ("new SpeechSynthesisUtterance(text ; '説明を待っています')", "new SpeechSynthesisUtterance(text || '説明を待っています')"),
    ("caption.textContent = text ; '説明を待っています';", "caption.textContent = text || '説明を待っています';"),
    ("const safeText = text ; '説明を待っています';", "const safeText = text || '説明を待っています';"),
    ("updateCaption(text ; '説明を待っています');", "updateCaption(text || '説明を待っています');"),
]

note = "<p>※ 1つずつ順番に進めると、やり方がわかりやすくなります。</p>"

for path in root.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    new_text = text

    for old, new in replacements:
        new_text = new_text.replace(old, new)

    new_text = re.sub(
        r'\n\s*<div class="button-row">\s*<button type="button" class="action-btn"[^>]*>.*?説明を聞く.*?</button>\s*</div>',
        '',
        new_text,
        flags=re.S,
    )

    if '※ 1つずつ順番に進めると' not in new_text:
        if '\n\n  <script>' in new_text:
            new_text = new_text.replace('\n\n  <script>', f'\n{note}\n\n  <script>', 1)
        elif '</body>' in new_text:
            new_text = new_text.replace('</body>', f'{note}\n</body>', 1)

    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f'fixed {path.name}')

print('done')
