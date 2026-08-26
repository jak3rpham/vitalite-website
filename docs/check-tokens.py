# -*- coding: utf-8 -*-
"""Kiểm token có lệch nhau ở ba nơi không. Chạy trước khi commit.

Ba nơi phải khớp:
  1. deliverables/brand/tokens.css                    nguồn sự thật cho người
  2. repo/.../vitalite-theme-2/style.css  :root       production đọc cái này
  3. giá trị dự phòng var(--vt-x, ...) trong fragment  bản xem trước đọc cái này

Lệch một trong ba là duyệt một màu, deploy ra màu khác. Đã xảy ra thật ở 10 token.

    cd "E:\\Vitalite website"; python docs/check-tokens.py
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, 'deliverables', 'brand', 'tokens.css')
THEME = os.path.join(ROOT, 'repo', 'vitalite-website', 'vitalite-theme',
                     'vitalite-theme-2', 'style.css')


def norm(v):
    return re.sub(r'\s+', '', v).lower()


def root_map(path):
    src = io.open(path, encoding='utf-8').read()
    body = re.search(r':root\s*\{(.*?)\n\}', src, re.S).group(1)
    body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
    return {m.group(1): norm(m.group(2))
            for m in re.finditer(r'(--vt-[a-z0-9-]+)\s*:\s*([^;]+);', body)}


def fragments():
    out = []
    for pat in ('deliverables/pages-html/*.html', 'deliverables/woo-templates/*.html'):
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            if not os.path.basename(f).startswith('_'):
                out.append(f)
    out.append(os.path.join(ROOT, 'docs', 'make-pages.py'))
    return out


def main():
    src = root_map(TOKENS)
    theme = root_map(THEME)
    problems = 0

    # 1. tokens.css vs theme
    for k in sorted(set(src) | set(theme)):
        a, b = src.get(k), theme.get(k)
        if a is None:
            print('  THIEU trong tokens.css : %-20s theme=%s' % (k, b)); problems += 1
        elif b is None:
            print('  THIEU trong theme      : %-20s tokens=%s' % (k, a)); problems += 1
        elif a != b:
            print('  LECH tokens vs theme   : %-20s %s != %s' % (k, a, b)); problems += 1

    # 2. fallback trong fragment vs tokens.css
    for f in fragments():
        s = io.open(f, encoding='utf-8').read()
        rel = os.path.relpath(f, ROOT)
        for m in re.finditer(r'var\(\s*(--vt-[a-z0-9-]+)\s*,\s*'
                             r'([^()]*?(?:\([^()]*\)[^()]*?)*)\)', s):
            k, v = m.group(1), norm(m.group(2))
            if k in src and v != src[k]:
                print('  LECH fallback          : %-20s %s' % (k, rel))
                print('%28s %s != %s' % ('', v, src[k]))
                problems += 1

    print()
    if problems:
        print('%d cho lech. Sua roi chay lai make-pages.py + make-woo-preview.py + make-guideline.py'
              % problems)
        return 1
    print('OK. %d token khop o ca ba noi.' % len(src))
    return 0


if __name__ == '__main__':
    sys.exit(main())
