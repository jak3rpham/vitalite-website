"""
Trích chuỗi dịch được từ theme VITALITÉ ra file .pot.

Không dùng wp-cli vì máy không có PHP CLI. Chỉ quét bằng regex — đủ dùng vì
theme viết nhất quán: mọi lời gọi i18n đều có text-domain 'vitalite' viết thẳng
trong cùng một dòng, không nối chuỗi, không dùng biến làm msgid.

Chạy lại sau MỖI lần sửa theme, nếu không chuỗi mới sẽ không dịch được.
"""
import io
import os
import re
import sys
import collections

# Duong dan thu muc theme: doi so dong lenh, hoac mac dinh la duong dan chuan
# trong repo nay (tinh nguoc tu vi tri file script).
if len(sys.argv) > 1:
    ROOT = sys.argv[1]
else:
    ROOT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'repo', 'vitalite-website', 'vitalite-theme', 'vitalite-theme'
    )
ROOT = os.path.normpath(ROOT)
DOMAIN = 'vitalite'
BS = chr(92)          # dấu backslash, viết kiểu này để heredoc/shell không đụng vào
Q2 = chr(34)          # "

SINGLE = re.compile(
    r"\b(?:esc_html__|esc_html_e|esc_attr__|esc_attr_e|__|_e)\s*\(\s*"
    r"(['\"])((?:\\.|(?!\1).)*)\1\s*,\s*(['\"])" + DOMAIN + r"\3\s*\)"
)
PLURAL = re.compile(
    r"\b_n\s*\(\s*"
    r"(['\"])((?:\\.|(?!\1).)*)\1\s*,\s*"
    r"(['\"])((?:\\.|(?!\3).)*)\3\s*,"
)
TRANSLATORS = re.compile(r'translators:\s*(.+?)(?:\*/)?$')


def unescape(quote, raw):
    out = raw.replace(BS + quote, quote)
    if quote == Q2:
        out = out.replace(BS + 'n', '\n').replace(BS + 't', '\t')
    return out


def po_escape(text):
    out = text.replace(BS, BS + BS)
    out = out.replace(Q2, BS + Q2)
    out = out.replace('\n', BS + 'n')
    out = out.replace('\t', BS + 't')
    return out


def collect():
    entries = collections.OrderedDict()
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ('languages', 'video', 'assets', 'node_modules', '.git')]
        for name in sorted(filenames):
            if name.endswith('.php'):
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, ROOT).replace(BS, '/')
                files.append(rel)

    for path in sorted(files):
        src = io.open(os.path.join(ROOT, path), encoding='utf-8').read()
        lines = src.split('\n')

        def lineno(pos):
            return src.count('\n', 0, pos) + 1

        def note(key, line_index):
            """Bắt comment /* translators: ... */ nằm ngay phía trên lời gọi."""
            for back in range(line_index - 2, max(line_index - 6, -1), -1):
                found = TRANSLATORS.search(lines[back].strip())
                if found:
                    text = found.group(1).strip()
                    if text not in entries[key]['ctx']:
                        entries[key]['ctx'].append(text)
                    return

        for m in SINGLE.finditer(src):
            key = (unescape(m.group(1), m.group(2)), None)
            entries.setdefault(key, {'refs': [], 'ctx': []})
            line = lineno(m.start())
            entries[key]['refs'].append('%s:%d' % (path, line))
            note(key, line)

        for m in PLURAL.finditer(src):
            # _n() có domain ở đối số thứ 4 — kiểm trong vùng ngay sau lời gọi
            if DOMAIN not in src[m.start():m.start() + 400]:
                continue
            key = (unescape(m.group(1), m.group(2)),
                   unescape(m.group(3), m.group(4)))
            entries.setdefault(key, {'refs': [], 'ctx': []})
            line = lineno(m.start())
            entries[key]['refs'].append('%s:%d' % (path, line))
            note(key, line)

    return entries, files


HEADER = '''# VITALITE - mau dich cua theme (.pot)
#
# CACH DUNG
#   1. Ban tieng Anh la msgid, KHONG can file dich - theme viet bang tieng Anh.
#   2. Dich sang tieng Viet: mo file nay bang Poedit -> "Create new translation"
#      -> chon Vietnamese -> dien msgstr -> luu. Poedit sinh ra ca .po lan .mo.
#   3. Dat ten dung chuan: `vitalite-vi.po` va `vitalite-vi.mo`, tha vao chinh
#      thu muc nay. `load_theme_textdomain()` trong inc/setup.php se tu nap.
#
#   CANH BAO 1: chi chuoi GIAO DIEN nam o day (nut, nhan, thong bao).
#   Ten san pham, mo ta, gia, chinh sach KHONG nam o day - chung la noi dung
#   trong WordPress va dich bang Polylang.
#
#   CANH BAO 2: sinh lai sau MOI lan sua theme, neu khong chuoi moi khong dich duoc.
#   Lenh: python docs/make-pot.py   (chay tu thu muc goc du an)
#
msgid ""
msgstr ""
"Project-Id-Version: VITALITE Theme 2.0.0PIPEn"
"Report-Msgid-Bugs-To: vitalitevn@gmail.comPIPEn"
"MIME-Version: 1.0PIPEn"
"Content-Type: text/plain; charset=UTF-8PIPEn"
"Content-Transfer-Encoding: 8bitPIPEn"
"Language-Team: VITALITEPIPEn"
"Plural-Forms: nplurals=2; plural=(n != 1);PIPEn"
"X-Domain: vitalitePIPEn"
'''


def main():
    entries, files = collect()
    out = [HEADER.replace('PIPE', BS)]

    for (msgid, plural), data in entries.items():
        out.append('')
        for comment in data['ctx']:
            out.append('#. translators: ' + comment)
        refs = data['refs']
        for i in range(0, len(refs), 4):
            out.append('#: ' + ' '.join(refs[i:i + 4]))
        out.append('msgid "%s"' % po_escape(msgid))
        if plural is None:
            out.append('msgstr ""')
        else:
            out.append('msgid_plural "%s"' % po_escape(plural))
            out.append('msgstr[0] ""')
            out.append('msgstr[1] ""')

    outdir = os.path.join(ROOT, 'languages')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    target = os.path.join(outdir, 'vitalite.pot')
    io.open(target, 'w', encoding='utf-8', newline='\n').write(
        '\n'.join(out) + '\n'
    )
    print('entries: %d | php files scanned: %d' % (len(entries), len(files)))
    print('-> %s' % target)


if __name__ == '__main__':
    main()
