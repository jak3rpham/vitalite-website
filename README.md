# VITALITÉ Website — Workspace

Mở Claude Code tại thư mục này.

```bash
cd "E:\Vitalite website"
claude
```

---

## Đọc theo thứ tự

| | |
|---|---|
| `CLAUDE.md` | Cách làm việc, rule không được vi phạm, trạng thái dự án *(Claude Code tự đọc)* |
| **`docs/HANDOFF.md`** | 👈 **File chính.** Việc kế tiếp, cấu trúc theme, quyết định đã chốt, fact brand, thứ đang chặn, bản đồ tài liệu |
| `docs/START-HERE.md` | Bản tóm tắt một trang |

---

## Cấu trúc thư mục

```
CLAUDE.md                       operating system
docs/                           HANDOFF · START-HERE · BUILD-CHECK · ASSUMPTIONS
                                BUILD-PLAN · I18N-SETUP · check-theme.py
reference/                      fact brand đã xác minh từ Shopee / IG / FB
deliverables/
  setup/                        DEPLOY · WORDPRESS-SETUP · PLUGINS
                                HOSTING-LITESPEED · PERFORMANCE
  woo/                          STRUCTURE-SETUP — category, attribute, variation
  content/                      PAGES-CONTENT — copy 6 trang tĩnh
  seo/                          SEO-PLAN
  analytics/                    TRACKING-PLAN
  images/                       MOCKUP-PIPELINE
  video/                        encode.md
  preview/                      static-preview.html  ← bấm đúp để xem giao diện
  motion/                       iridescent.html
repo/vitalite-website/          clone GitHub — THEME THẬT nằm ở đây
Logo/ · mockup-all/ · model/    asset gốc từ brand
```

---

## Xem giao diện ngay, không cần server

Bấm đúp `deliverables/preview/static-preview.html`.
8 màn hình dựng bằng đúng `style.css` của theme và ảnh thật, hero 3 slide chạy thật.

---

## Trạng thái

Theme đã viết lại hoàn toàn (v2.0.0, 25 file PHP, layout full-width, hero 3 slide).
Tự kiểm 7 mục — sạch. **Chưa chạy thử trên hosting lần nào.**

**Việc kế tiếp:** gỡ 96MB video master khỏi thư mục theme → nén → upload cPanel song song.
Xem `deliverables/setup/DEPLOY.md`.
