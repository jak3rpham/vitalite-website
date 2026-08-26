# -*- coding: utf-8 -*-
"""Sinh bản xem trước cho hai prototype WooCommerce.

    deliverables/woo-templates/pdp.html                  -> _preview-pdp.html
    deliverables/woo-templates/cart-checkout-account.html -> _preview-shop.html

Khối `:root` trong bản xem trước ĐỌC TỪ deliverables/brand/tokens.css, không
chép tay. Trước đây nó chép tay và đã lệch với theme ở 3 màu, nghĩa là bản mọi
người dùng để duyệt hiển thị SAI MÀU so với production.

    cd "E:\\Vitalite website"; python docs/make-woo-preview.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, 'deliverables', 'brand', 'tokens.css')
OUT = os.path.join(ROOT, 'deliverables', 'woo-templates')


def root_block():
    """Rút gọn :root trong tokens.css thành một khối CSS nhúng được."""
    src = io.open(TOKENS, encoding='utf-8').read()
    body = re.search(r':root\s*\{(.*)\n\}', src, re.S).group(1)
    body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)      # bỏ chú thích
    decls = [' '.join(d.split()) for d in body.split(';') if d.strip()]
    return ':root{' + ';'.join(decls) + ';}'


HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Archivo+Expanded:wght@800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
%(tokens)s
*{box-sizing:border-box}
body{margin:0;background:var(--vt-paper);color:var(--vt-ink);font-family:var(--vt-font-primary);}
</style></head><body>
"""

PAGES = [
    ('pdp.html', 'PDP preview', '_preview-pdp.html'),
    ('cart-checkout-account.html', 'Shop screens preview', '_preview-shop.html'),
]


def build():
    tokens = root_block()
    made = []
    for src, title, out in PAGES:
        path = os.path.join(OUT, src)
        if not os.path.isfile(path):
            continue
        body = io.open(path, encoding='utf-8').read()
        html = (HEAD % dict(title=title, tokens=tokens)) + body + '\n</body></html>\n'
        io.open(os.path.join(OUT, out), 'w', encoding='utf-8', newline='\n').write(html)
        made.append(out)
    return made


if __name__ == '__main__':
    for f in build():
        print('preview  %s' % f)
