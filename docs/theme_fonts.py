# -*- coding: utf-8 -*-
"""Một nguồn sự thật duy nhất cho URL Google Fonts của mọi thứ sinh ra từ repo.

    from theme_fonts import font_url
    ...  '<link rel="stylesheet" href="%s">' % font_url()

🔴 VÌ SAO FILE NÀY TỒN TẠI

Ngày 30/08/2026, bản vá `6b04acf` gỡ `Archivo+Expanded` khỏi theme. Family đó
KHÔNG TỒN TẠI trên Google Fonts: gọi riêng thì trả 404, gọi kèm family khác thì
Google **im lặng bỏ qua**. Không 404, không cảnh báo — chỉ là mọi tiêu đề mất bề
ngang và chữ header 11px rơi về bold giả, nhoè. Không nhìn ra bằng mắt trừ khi
đã biết mà đi tìm.

Bản vá đó sửa theme và sửa các file HTML đã sinh ra. Nhưng nó **không sửa những
script sinh ra các file đó**. URL cũ nằm im trong bốn script, và mỗi lần chạy
lại là lặng lẽ dựng lại đúng cái lỗi vừa vá:

    docs/make-site-preview.py      bản xem trước toàn site
    docs/make-woo-preview.py       _preview-pdp.html · _preview-shop.html
    docs/make-guideline.py         deliverables/brand/guideline.html
    docs/make-guideline-pdf.py     bản PDF guideline

Phát hiện 25/09/2026, gần một tháng sau, khi chạy `make-woo-preview.py` và thấy
`Archivo+Expanded` mọc lại trong file vừa sinh. Hai file guideline thì đã sai
suốt từ 30/08 — nghĩa là chính tài liệu định nghĩa typography của brand đang tự
render bằng font sai.

Nên URL không được viết sẵn ở đâu nữa. Nó đọc thẳng từ `inc/enqueue.php`, chỗ
theme thật khai báo. Theme đổi font thì mọi thứ sinh ra đổi theo, hết drift.
"""
import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ENQUEUE = os.path.join(_ROOT, 'repo', 'vitalite-website', 'vitalite-theme',
                        'vitalite-theme-2', 'inc', 'enqueue.php')


def font_url():
    """Rút URL Google Fonts ra khỏi lời gọi wp_enqueue_style('vitalite-fonts', ...).

    URL trong PHP được nối từ nhiều chuỗi, xen giữa là chú thích. Nên lấy mọi
    chuỗi nháy đơn trong lời gọi đó rồi giữ lại các mảnh thuộc về URL.

    @raise SystemExit nếu không đọc được, hoặc nếu theme lại có Archivo+Expanded.
           Vỡ to còn hơn lặng lẽ sinh ra file sai font.
    """
    src = io.open(_ENQUEUE, encoding='utf-8').read()
    m = re.search(r"'vitalite-fonts'\s*,(.*?)\);", src, re.S)
    if not m:
        raise SystemExit(
            'theme_fonts: khong tim thay wp_enqueue_style(\'vitalite-fonts\') trong\n'
            '  %s\nTheme doi cau truc? Sua regex o day truoc khi chay tiep.' % _ENQUEUE)

    parts = [s for s in re.findall(r"'([^']*)'", m.group(1))
             if s.startswith(('https://fonts.', '?', '&'))]
    url = ''.join(parts)

    if not url.startswith('https://fonts.googleapis.com/css2?'):
        raise SystemExit('theme_fonts: URL rut ra trong khong giong URL font: %r' % url)
    if 'Archivo+Expanded' in url:
        raise SystemExit(
            "theme_fonts: inc/enqueue.php van con 'Archivo+Expanded'.\n"
            'Family do KHONG TON TAI tren Google Fonts — xem dau file nay.')
    return url


if __name__ == '__main__':
    print(font_url())
