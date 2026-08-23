/* ============================================================
   Sinh file Word cho brand điền, TỪ CHÍNH file markdown.

     deliverables/CAU-HOI-CHO-BRAND.md   ->   deliverables/CAU-HOI-CHO-BRAND.docx

   🔴 VÌ SAO PHẢI SINH RA CHỨ KHÔNG SOẠN TAY
   Dự án này đã bị lệch bản hai lần rồi: hai file _preview-*.html làm tay nên
   lệch với trang thật, và bảng trong README lệch với số trang thật. Bộ câu hỏi
   này sẽ còn sửa nhiều lần khi brand trả lời dần. Có hai bản Word và markdown
   soạn tay song song là chắc chắn lệch.

   Markdown là bản gốc. Word là bản xuất ra. Sửa câu hỏi thì sửa file .md rồi
   chạy lại:

     cd "E:\Vitalite website"; node docs/make-brand-docx.js

   Cần: gói `docx` của npm (đã có sẵn trong môi trường Claude).
   ============================================================ */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, HeadingLevel,
  PageOrientation, Header, Footer, PageNumber,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'deliverables', 'CAU-HOI-CHO-BRAND.md');
const OUT = path.join(ROOT, 'deliverables', 'CAU-HOI-CHO-BRAND.docx');

// A4 = 11906 dxa. Lề 1080 mỗi bên -> vùng nội dung 9746. Bảng dùng 9700.
const CONTENT_W = 9700;

const INK = '0A0A0A';
const MUTED = '5A5A60';
const BOX_BG = 'F4F4F6';   // ô để brand gõ vào
const CTX_BG = 'FAFAFB';   // khối giải thích
const ACCENT = 'B45309';   // cam, dùng cho cảnh báo

/* ---------- markdown nội dòng -> TextRun[] ----------
   Chỉ xử ba thứ thật sự có trong file: **đậm**, *nghiêng*, `mã`.
   Không viết parser tổng quát, vì file này do mình viết, không phải input lạ. */
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith('**')) {
      out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    } else if (t.startsWith('`')) {
      out.push(new TextRun({ text: t.slice(1, -1), font: 'Consolas', size: 19, ...base }));
    } else {
      out.push(new TextRun({ text: t.slice(1, -1), italics: true, ...base }));
    }
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out.length ? out : [new TextRun({ text: '', ...base })];
}

const P = (text, opts = {}) => new Paragraph({
  children: runs(text, opts.run || {}),
  spacing: { before: opts.before ?? 0, after: opts.after ?? 120 },
  ...(opts.para || {}),
});

/* Khối giải thích: nền nhạt + viền trái. Đây là chỗ nói VÌ SAO cần câu trả lời,
   và nó là lý do brand chịu đọc thay vì bỏ qua. */
function contextBox(lines, warn) {
  const kids = [];
  lines.forEach((ln, i) => {
    if (/^\s*-\s+/.test(ln)) {
      kids.push(new Paragraph({
        children: runs(ln.replace(/^\s*-\s+/, ''), { size: 19, color: MUTED }),
        bullet: { level: 0 },
        spacing: { after: 60 },
      }));
    } else if (/^#+\s/.test(ln)) {
      kids.push(new Paragraph({
        children: runs(ln.replace(/^#+\s*/, ''), { size: 20, bold: true, color: warn ? ACCENT : INK }),
        spacing: { after: 80 },
      }));
    } else {
      kids.push(new Paragraph({
        children: runs(ln, { size: 19, color: MUTED }),
        spacing: { after: i === lines.length - 1 ? 0 : 60 },
      }));
    }
  });
  return new Table({
    columnWidths: [CONTENT_W],
    width: { size: CONTENT_W, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE },
      insideVertical: { style: BorderStyle.NONE },
      left: { style: BorderStyle.SINGLE, size: 18, color: warn ? ACCENT : 'C9C9CE' },
    },
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: warn ? 'FEF6E7' : CTX_BG },
        margins: { top: 140, bottom: 140, left: 200, right: 200 },
        children: kids,
      })],
    })],
  });
}

/* Ô trả lời. Ba dòng trống để brand gõ vào, nền xám nhạt cho biết là gõ được. */
function answerBox() {
  return new Table({
    columnWidths: [CONTENT_W],
    width: { size: CONTENT_W, type: WidthType.DXA },
    borders: ['top', 'bottom', 'left', 'right'].reduce((a, k) => (
      a[k] = { style: BorderStyle.SINGLE, size: 4, color: 'B8B8C0' }, a
    ), {}),
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: CONTENT_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: BOX_BG },
        margins: { top: 120, bottom: 120, left: 180, right: 180 },
        children: [
          new Paragraph({
            children: [new TextRun({ text: 'Trả lời:', size: 17, color: '8A8A92' })],
            spacing: { after: 60 },
          }),
          new Paragraph({ children: [new TextRun('')], spacing: { after: 60 } }),
          new Paragraph({ children: [new TextRun('')], spacing: { after: 0 } }),
        ],
      })],
    })],
  });
}

function mdTable(rows) {
  const cols = rows[0].length;
  const w = Math.floor(CONTENT_W / cols);
  const widths = Array(cols).fill(w);
  widths[cols - 1] = CONTENT_W - w * (cols - 1);
  return new Table({
    columnWidths: widths,
    width: { size: CONTENT_W, type: WidthType.DXA },
    rows: rows.map((cells, ri) => new TableRow({
      children: cells.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: ri === 0 ? 'ECECEF' : 'FFFFFF' },
        margins: { top: 90, bottom: 90, left: 140, right: 140 },
        children: [new Paragraph({
          children: runs(c.replace(/^`|`$/g, '').trim() || ' ',
            { size: 19, bold: ri === 0 }),
          spacing: { after: 0 },
        })],
      })),
    })),
  });
}

// ---------------------------------------------------------------- đọc markdown
const lines = fs.readFileSync(SRC, 'utf8').split(/\r?\n/);
const body = [];
let i = 0;
let inFrontMatter = true;

const flushHr = () => body.push(new Paragraph({
  children: [new TextRun('')],
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'D8D8DC' } },
  spacing: { before: 200, after: 200 },
}));

while (i < lines.length) {
  const ln = lines[i];

  // gom khối trích dẫn
  if (/^>\s?/.test(ln)) {
    const buf = [];
    while (i < lines.length && /^>\s?/.test(lines[i])) {
      buf.push(lines[i].replace(/^>\s?/, ''));
      i++;
    }
    const clean = buf.filter((x, k) => !(x.trim() === '' && (k === 0 || k === buf.length - 1)));
    const warn = clean.some(x => x.includes('⚠️') || x.includes('🔴'));
    body.push(contextBox(clean.length ? clean : [' '], warn));
    body.push(new Paragraph({ children: [new TextRun('')], spacing: { after: 120 } }));
    continue;
  }

  // gom bảng
  if (/^\|/.test(ln)) {
    const rows = [];
    while (i < lines.length && /^\|/.test(lines[i])) {
      const cells = lines[i].split('|').slice(1, -1).map(c => c.trim());
      if (!cells.every(c => /^:?-+:?$/.test(c))) rows.push(cells);
      i++;
    }
    if (rows.length) body.push(mdTable(rows));
    body.push(new Paragraph({ children: [new TextRun('')], spacing: { after: 160 } }));
    continue;
  }

  // ô trả lời
  if (/^`\.{5,}`\s*$/.test(ln) || /^`(Ai duyệt|Trả lời):\s*\.{3,}`\s*$/.test(ln)) {
    body.push(answerBox());
    body.push(new Paragraph({ children: [new TextRun('')], spacing: { after: 160 } }));
    i++;
    continue;
  }

  // câu hỏi đánh số: gom cả những dòng nối tiếp
  const q = ln.match(/^\*\*(\d+)\.\*\*\s*(.*)$/);
  if (q) {
    let text = q[2];
    i++;
    while (i < lines.length && lines[i].trim() !== ''
           && !/^[>|`#-]/.test(lines[i]) && !/^\*\*\d+\.\*\*/.test(lines[i])
           && !/^\s*\d+\.\s/.test(lines[i])) {
      text += ' ' + lines[i].trim();
      i++;
    }
    body.push(new Paragraph({
      children: [
        new TextRun({ text: q[1] + '.  ', bold: true, size: 24, color: ACCENT }),
        ...runs(text, { bold: true, size: 22 }),
      ],
      spacing: { before: 280, after: 140 },
      keepNext: true,
    }));
    continue;
  }

  if (/^# /.test(ln)) {
    inFrontMatter = false;
    body.push(new Paragraph({
      children: runs(ln.slice(2), { bold: true, size: 34, color: INK }),
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 420, after: 200 },
      pageBreakBefore: body.length > 0,
    }));
    i++; continue;
  }
  if (/^## /.test(ln)) {
    body.push(new Paragraph({
      children: runs(ln.slice(3), { bold: true, size: 26, color: INK }),
      heading: HeadingLevel.HEADING_2,
      spacing: { before: 340, after: 160 },
      keepNext: true,
    }));
    i++; continue;
  }

  if (/^---+\s*$/.test(ln)) {
    if (!inFrontMatter && lines[i + 1] && /^---+\s*$/.test(lines[i + 1])) { i += 2; continue; }
    i++; continue;
  }

  // Mục đánh số trong phần "Cách trả lời".
  // 🔴 Phải gom dòng nối tiếp VÀ phải dừng ở mục kế tiếp. Bản trước không dừng,
  // nên cả ba mục dính thành một đoạn.
  if (/^\d+\.\s/.test(ln)) {
    let text = ln.replace(/^\d+\.\s*/, '');
    i++;
    while (i < lines.length && lines[i].trim() !== ''
           && !/^\s*\d+\.\s/.test(lines[i]) && !/^[>|#`-]/.test(lines[i])) {
      text += ' ' + lines[i].trim();
      i++;
    }
    body.push(new Paragraph({
      children: runs(text, { size: 21 }),
      bullet: { level: 0 },
      spacing: { after: 120 },
    }));
    continue;
  }

  if (/^\*[^*]/.test(ln) && /\*\s*$/.test(ln)) {
    body.push(P(ln, { run: { size: 18, italics: true, color: MUTED }, before: 200 }));
    i++; continue;
  }

  if (ln.trim() === '') { i++; continue; }

  // đoạn văn thường, gom dòng nối tiếp
  let text = ln;
  i++;
  while (i < lines.length && lines[i].trim() !== ''
         && !/^[>|#`-]/.test(lines[i]) && !/^\*\*\d+\.\*\*/.test(lines[i])
         && !/^\s*\d+\.\s/.test(lines[i])) {
    text += ' ' + lines[i].trim();
    i++;
  }
  body.push(P(text, { run: { size: 21 } }));
}

// ---------------------------------------------------------------- xuất file
const doc = new Document({
  creator: 'VITALITE',
  title: 'Cau hoi cho VITALITE',
  description: 'Bo cau hoi de brand dien va tra lai',
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 21, color: INK }, paragraph: { spacing: { line: 288 } } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { orientation: PageOrientation.PORTRAIT },
        margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: 'VITALITÉ  ·  Câu hỏi cho brand  ·  24/08/2026', size: 16, color: '9A9AA2' })],
          spacing: { after: 0 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'E0E0E4' } },
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ children: ['Trang ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], size: 16, color: '9A9AA2' })],
        })],
      }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  const kb = (buf.length / 1024).toFixed(1);
  console.log('OK  ' + path.relative(ROOT, OUT) + '  (' + kb + ' KB)');
  console.log('    nguon: ' + path.relative(ROOT, SRC));
});
