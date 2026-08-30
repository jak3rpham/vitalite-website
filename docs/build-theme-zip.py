"""Đóng gói theme thành zip để upload lên cPanel.

CHẠY
    cd "E:\\Vitalite website"; python docs/build-theme-zip.py
    -> ghi ra E:\\Vitalite website\\vitalite-theme.zip

VÌ SAO LÀ SCRIPT CHỨ KHÔNG PHẢI CHUỘT PHẢI → NÉN
    Nén bằng Explorer gói cả rác: Thumbs.db, desktop.ini, file .map còn sót,
    và bất kỳ file nặng nào lỡ rơi vào thư mục theme. Trên shared hosting
    không SSH, phát hiện ra rác sau khi đã extract là phải xoá tay từng file.

    Script này bỏ rác theo danh sách rõ ràng, và QUAN TRỌNG HƠN: nó in ra
    mọi file trên 500 KB. Site fashion chết vì trọng lượng, nên mỗi file nặng
    lọt vào theme phải là một quyết định có người nhìn thấy, không phải tai nạn.

TÊN THƯ MỤC TRONG ZIP
    `vitalite-theme` — xem hằng FOLDER bên dưới. Luật là: tên trong zip phải
    KHÁC mọi thư mục theme đang có trên production. Extract vào một cái tên
    trống thì không có bước ghi đè, không có bước đổi tên, và không có giây
    phút nào site hỏng. Xem `deliverables/setup/DEPLOY.md` bước 2.
"""
import os
import re
import sys
import unicodedata
import zipfile

BS = chr(92)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'repo', 'vitalite-website', 'vitalite-theme', 'vitalite-theme-2')
# Ten thu muc trong zip va ten file zip KHONG viet tay nua: ca hai suy ra tu
# `Theme Name` trong style.css (xem slug_from_name()). Doi ten theme la thu muc
# tu doi theo, khong con kha nang hai thu lech nhau.
#
# LUAT: ten thu muc phai KHAC moi thu muc theme dang co tren hosting. Extract
# vao mot ten trong thi khong co buoc ghi de, khong co buoc doi ten, va khong
# co giay phut nao site hong. Extract de len thu muc da ton tai la TRON chu
# khong phai thay -- file cu khong con trong ban moi van nam nguyen do.
FOLDER = None   # dat trong main(), sau khi doc style.css
OUT = None

SKIP_DIR = {'.git', '__pycache__', 'node_modules', '.vscode', '.idea'}
SKIP_FILE = {'.DS_Store', 'Thumbs.db', 'desktop.ini', 'Desktop.ini'}
SKIP_EXT = {'.log', '.pyc', '.map', '.psd', '.ai', '.zip'}

# Ngưỡng cảnh báo. Không chặn, chỉ bắt phải nhìn thấy.
BIG = 500 * 1024


def slug_from_name(name):
    """Bien `Theme Name` thanh slug thu muc.

        'Vitalite 2.0'  ->  'vitalite-2-0'

    Bo dau tieng Viet truoc, vi ten theme co the mang dau (Vitalite co dau sac)
    va ten thu muc tren hosting thi khong nen co. Dau cham trong so phien ban
    thanh dau gach ngang -- dau cham trong ten thu muc de bi nham la duoi file.
    """
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('đ', 'd').replace('Đ', 'D')   # d gach ngang khong tach dau duoc
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'theme'


def main():
    if not os.path.isdir(SRC):
        sys.exit('Khong thay thu muc theme: ' + SRC)

    style = os.path.join(SRC, 'style.css')
    if not os.path.isfile(style):
        sys.exit('Khong thay style.css. Sai thu muc?')

    version = ''
    # KHONG dat ten bien la `name`: vong lap dong goi ben duoi dung `name` cho
    # ten tung file, va no se ghi de len ten theme truoc khi kip in ra.
    theme_name = ''
    with open(style, encoding='utf-8') as fh:
        for line in fh:
            low = line.strip().lower()
            if low.startswith('version:'):
                version = line.split(':', 1)[1].strip()
            elif low.startswith('theme name:'):
                theme_name = line.split(':', 1)[1].strip()
            if version and theme_name:
                break

    if not theme_name:
        sys.exit('style.css khong khai Theme Name')

    global FOLDER, OUT
    FOLDER = slug_from_name(theme_name)
    OUT = os.path.join(ROOT, FOLDER + '.zip')

    skipped = []
    big = []
    count = 0
    raw = 0

    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, dirs, files in os.walk(SRC):
            dirs[:] = [d for d in dirs if d not in SKIP_DIR]
            for name in sorted(files):
                if name in SKIP_FILE or os.path.splitext(name)[1].lower() in SKIP_EXT:
                    skipped.append(name)
                    continue
                full = os.path.join(root, name)
                rel = os.path.relpath(full, SRC).replace(BS, '/')
                size = os.path.getsize(full)
                raw += size
                if size > BIG:
                    big.append((rel, size))
                z.write(full, FOLDER + '/' + rel)
                count += 1

    zipped = os.path.getsize(OUT)

    print('')
    print('THEME     %s  v%s' % (theme_name, version))
    print('THU MUC   %s/   (trong zip)' % FOLDER)
    print('NGUON     %s' % SRC)
    print('ZIP       %s' % OUT)
    print('')
    print('%d file  %.1f MB  ->  %.1f MB' % (count, raw / 1048576.0, zipped / 1048576.0))

    if skipped:
        print('')
        print('Bo qua %d file rac: %s' % (len(skipped), ', '.join(sorted(set(skipped)))))

    print('')
    if big:
        print('File tren 500 KB — moi cai phai la mot quyet dinh, khong phai tai nan:')
        for rel, size in sorted(big, key=lambda x: -x[1]):
            print('   %7.2f MB  %s' % (size / 1048576.0, rel))
    else:
        print('Khong file nao tren 500 KB.')

    # Kiem lai chinh minh: zip doc duoc, va style.css nam dung cho
    with zipfile.ZipFile(OUT) as z:
        bad = z.testzip()
        if bad:
            sys.exit('ZIP HONG o file: ' + bad)
        if FOLDER + '/style.css' not in z.namelist():
            sys.exit('style.css khong nam o goc thu muc theme trong zip')
        tops = {n.split('/')[0] for n in z.namelist()}
        if tops != {FOLDER}:
            sys.exit('Zip co nhieu thu muc goc: %s' % sorted(tops))

    print('')
    print('Zip OK. Buoc tiep theo: deliverables/setup/DEPLOY.md buoc 1b.')


if __name__ == '__main__':
    main()
