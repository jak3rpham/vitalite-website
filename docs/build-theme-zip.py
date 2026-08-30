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
import sys
import zipfile

BS = chr(92)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'repo', 'vitalite-website', 'vitalite-theme', 'vitalite-theme-2')
OUT = os.path.join(ROOT, 'vitalite-theme.zip')

# Ten thu muc BEN TRONG zip. Day la ten theme se co tren hosting.
# 30/08/2026: user da xoa thu muc `vitalite-theme` cu tren production, nen slot
# nay trong. Extract vao do la ra mot thu muc SACH, khong tron voi ban cu.
# Neu sau nay tren production da co `vitalite-theme` dang chay, DOI ten o day
# thanh mot ten chua ton tai (vd `vitalite-theme-3`) roi dung lai zip --
# lam vay khong phai dong vao theme dang chay, khong co giay nao site hong.
FOLDER = 'vitalite-theme'

SKIP_DIR = {'.git', '__pycache__', 'node_modules', '.vscode', '.idea'}
SKIP_FILE = {'.DS_Store', 'Thumbs.db', 'desktop.ini', 'Desktop.ini'}
SKIP_EXT = {'.log', '.pyc', '.map', '.psd', '.ai', '.zip'}

# Ngưỡng cảnh báo. Không chặn, chỉ bắt phải nhìn thấy.
BIG = 500 * 1024


def main():
    if not os.path.isdir(SRC):
        sys.exit('Khong thay thu muc theme: ' + SRC)

    style = os.path.join(SRC, 'style.css')
    if not os.path.isfile(style):
        sys.exit('Khong thay style.css. Sai thu muc?')

    version = ''
    with open(style, encoding='utf-8') as fh:
        for line in fh:
            if line.strip().lower().startswith('version:'):
                version = line.split(':', 1)[1].strip()
                break

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
    print('THEME     Vitalite Theme %s' % version)
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
