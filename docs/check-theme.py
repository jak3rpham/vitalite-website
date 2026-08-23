"""Kiểm tra theme Vitalité: cú pháp, hàm, template part, class CSS, i18n, escape."""
import io, re, os, sys, glob

BS = chr(92)
ROOT = sys.argv[1]

def clean(code):
    out = []; i = 0; n = len(code)
    while i < n:
        c = code[i]; nxt = code[i+1] if i+1 < n else ''
        if c == '/' and nxt == '*':
            j = code.find('*/', i+2); i = n if j == -1 else j+2; out.append(' ')
        elif (c == '/' and nxt == '/') or c == '#':
            j = code.find('\n', i); i = n if j == -1 else j; out.append(' ')
        elif c in '"\'':
            q = c; i += 1
            while i < n:
                if code[i] == BS: i += 2; continue
                if code[i] == q: i += 1; break
                i += 1
            out.append('S')
        else:
            out.append(c); i += 1
    return ''.join(out)

def php_code(src):
    parts = []; i = 0
    while True:
        a = src.find('<?php', i)
        if a == -1:
            a2 = src.find('<?=', i)
            if a2 == -1: break
            a, off = a2, 3
        else: off = 5
        b = src.find('?>', a+off)
        parts.append(src[a+off:] if b == -1 else src[a+off:b])
        if b == -1: break
        i = b+2
    return ''.join(parts)

files = sorted(glob.glob(os.path.join(ROOT, '**', '*.php'), recursive=True))
rel = lambda p: os.path.relpath(p, ROOT).replace('\\', '/')
problems = []

print('=' * 74)
print('1. CAN BANG CU PHAP')
print('=' * 74)
for f in files:
    src = io.open(f, encoding='utf-8').read()
    code = clean(php_code(src))
    br = code.count('{') - code.count('}')
    pa = code.count('(') - code.count(')')
    sq = code.count('[') - code.count(']')
    st = 'OK' if br == pa == sq == 0 else '*** LECH ***'
    if st != 'OK':
        problems.append('cu phap lech: ' + rel(f))
    print('  %-42s {}%+d ()%+d []%+d  %s' % (rel(f), br, pa, sq, st))

print()
print('=' * 74)
print('2. HAM vt_* : dinh nghia vs su dung')
print('=' * 74)
defined = {}
used = {}
for f in files:
    src = io.open(f, encoding='utf-8').read()
    for m in re.finditer('function' + r'\s+' + '(vt_' + r'\w+' + r')\s*\(', src):
        defined.setdefault(m.group(1), []).append(rel(f))
    for m in re.finditer(r'(?<!function )\b' + '(vt_' + r'\w+' + r')\s*\(', src):
        used.setdefault(m.group(1), set()).add(rel(f))
missing = sorted(set(used) - set(defined))
unused = sorted(set(defined) - set(used))
dupes = sorted(k for k, v in defined.items() if len(v) > 1)
print('  dinh nghia : %d' % len(defined))
print('  goi ma CHUA co : %s' % (missing or 'khong'))
print('  dinh nghia 2 lan: %s' % (dupes or 'khong'))
print('  dinh nghia ma khong dung: %s' % (unused or 'khong'))
if missing: problems.append('ham chua dinh nghia: %s' % missing)
if dupes: problems.append('ham trung ten: %s' % dupes)

print()
print('=' * 74)
print('3. get_template_part() tro toi file co ton tai khong')
print('=' * 74)
for f in files:
    src = io.open(f, encoding='utf-8').read()
    for m in re.finditer(r"(?<!wc_)get_template_part\(\s*['\"]([^'\"]+)['\"]", src):
        part = m.group(1)
        cand = os.path.join(ROOT, part + '.php')
        ok = os.path.exists(cand)
        print('  %-42s -> %-38s %s' % (rel(f), part, 'OK' if ok else '*** THIEU ***'))
        if not ok: problems.append('template part thieu: %s (goi tu %s)' % (part, rel(f)))

print()
print('=' * 74)
print('4. CLASS CSS dung trong PHP ma khong co rule')
print('=' * 74)
css = io.open(os.path.join(ROOT, 'style.css'), encoding='utf-8').read()
css_no_comment = re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)
used_classes = set()
for f in files:
    src = io.open(f, encoding='utf-8').read()
    for m in re.finditer(r'class="([^"]*)"', src):
        for c in m.group(1).split():
            if c.startswith('vt-') and '<' not in c and '?' not in c:
                used_classes.add(c)
    for m in re.finditer(r"'(vt-[a-z0-9-]+)'", src):
        used_classes.add(m.group(1))
# Class chi dung lam hook (JS/PHP bam vao) hoac da duoc style qua selector cha
HOOK_ONLY = {
    'vt-brand-mark',    # .vt-brand img da style
    'vt-footer-logo',   # .vt-footer-brand img da style
    'vt-card-front',    # .vt-card-media img da style
    'vt-card-2x',       # ten image size, khong phai class
    'vt-has-hero',      # body class, hook cho JS/CSS tuong lai
    'vt-nav-wrap',      # container ngu nghia, khong can style
    'vt-search-',       # tien to ID trong searchform.php, khong phai class
}
def is_real_class(c):
    return re.fullmatch(r'vt-[a-z0-9-]+', c) is not None
missing_css = [c for c in sorted(used_classes)
               if is_real_class(c) and c not in HOOK_ONLY
               and not re.search(r'\.' + re.escape(c) + r'(?![\w-])', css_no_comment)]
print('  class vt-* dung: %d' % len(used_classes))
print('  KHONG co rule  : %s' % (missing_css or 'khong'))
if missing_css: problems.append('class thieu CSS: %s' % missing_css)

print()
print('=' * 74)
print('5. CHUOI BIA - phai bang 0 (tru trong comment)')
print('=' * 74)
banned = ['480GSM', 'SS26', 'Cropped Zip', 'Boxy Tee "Vital', 'Washed Tee',
          'Longsleeve Ribbed', 'Baggy Tee', 'Knit Polo', 'Utility Shirt',
          '1.290.000', '1.450.000', 'Song Het Cong Suat', 'Duong Pho']
hits = []
for f in files:
    src = io.open(f, encoding='utf-8').read()
    code = clean(php_code(src))          # bo comment va string PHP
    html = re.sub(r'<\?php.*?(\?>|$)', ' ', src, flags=re.S)   # phan HTML thuan
    for b in banned:
        if b in html:
            hits.append('%s : %s (trong HTML)' % (rel(f), b))
print('  ' + ('\n  '.join(hits) if hits else 'sach'))
if hits: problems.append('con chuoi bia trong HTML')

print()
print('=' * 74)
print('6. ESCAPE: echo bien khong qua esc_*')
print('=' * 74)
risky = []
for f in files:
    for i, line in enumerate(io.open(f, encoding='utf-8'), 1):
        s = line.strip()
        if s.startswith('*') or s.startswith('//'): continue
        m = re.search(r'echo\s+\$[A-Za-z_]', s)
        if m and not re.search(r'esc_|wp_kses|wp_json|absint|intval|number_format', s):
            risky.append('%s:%d  %s' % (rel(f), i, s[:78]))
print('  ' + ('\n  '.join(risky) if risky else 'khong co dong nao dang ngo'))
if risky: problems.append('echo bien chua escape')

print()
print('=' * 74)
print('7. i18N: text-domain dung nhat quan')
print('=' * 74)
domains = {}
for f in files:
    src = io.open(f, encoding='utf-8').read()
    for m in re.finditer(r"(?:__|_e|esc_html__|esc_html_e|esc_attr__|esc_attr_e)\(\s*'[^']*'\s*,\s*'([^']+)'", src):
        domains[m.group(1)] = domains.get(m.group(1), 0) + 1
print('  ' + str(domains))
if len(domains) > 1: problems.append('text-domain khong nhat quan: %s' % list(domains))

print()
print('=' * 74)
print('KET LUAN')
print('=' * 74)
if problems:
    for p in problems: print('  [!] ' + p)
    print('\n  TONG: %d van de' % len(problems))
else:
    print('  Khong phat hien van de.')
