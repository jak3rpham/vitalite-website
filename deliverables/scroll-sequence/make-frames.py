"""
Cắt video thành chuỗi frame WebP cho hiệu ứng scroll-sequence.

CHẠY
    cd "E:\\Vitalite website"
    python deliverables/scroll-sequence/make-frames.py <video> <tên-chuỗi> [số-frame] [chiều-rộng]

VÍ DỤ
    python deliverables/scroll-sequence/make-frames.py raw/model-walk.mp4 walk 32 900

RA CÁI GÌ
    deliverables/scroll-sequence/frames/<tên-chuỗi>/001.webp … NNN.webp
    deliverables/scroll-sequence/frames/<tên-chuỗi>/manifest.json

VÌ SAO KHÔNG PHẢI 24FPS
    24fps × 4 giây = 96 frame. Ở 900px WebP đó là ~3MB cho một section.
    Mắt đọc chuyển động xoay chậm là mượt từ khoảng 30 frame. Script này
    LẤY MẪU ĐỀU trên toàn bộ video thay vì cắt theo fps — nghĩa là video dài
    bao nhiêu cũng ra đúng số frame mình muốn.

YÊU CẦU
    ffmpeg trong PATH. Kiểm: ffmpeg -version
"""
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES_ROOT = os.path.join(HERE, 'frames')

# Ngưỡng cấu hình cho Web & High-Quality sequence
MAX_FRAMES = 180
MAX_TOTAL_KB = 25000
MAX_FRAME_KB = 400


def probe_duration(path):
    out = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', path
    ])
    return float(out.decode().strip())


def build(video, name, count, width, quality=72):
    if count > MAX_FRAMES:
        print('!! %d frame vượt ngưỡng %d. Nhiều hơn không mượt hơn, chỉ nặng hơn.'
              % (count, MAX_FRAMES))
        return 1

    outdir = os.path.join(FRAMES_ROOT, name)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    dur = probe_duration(video)
    # Lấy mẫu ĐỀU trên toàn bộ video, không cắt theo fps.
    fps = count / dur

    cmd = [
        'ffmpeg', '-y', '-v', 'error', '-i', video,
        '-vf', 'fps=%.6f,scale=%d:-2' % (fps, width),
        '-frames:v', str(count),
        '-c:v', 'libwebp', '-quality', str(quality), '-compression_level', '6',
        os.path.join(outdir, '%03d.webp'),
    ]
    subprocess.check_call(cmd)

    files = sorted(f for f in os.listdir(outdir) if f.endswith('.webp'))
    sizes = [os.path.getsize(os.path.join(outdir, f)) for f in files]
    total_kb = sum(sizes) / 1024.0
    biggest_kb = (max(sizes) / 1024.0) if sizes else 0

    manifest = {
        'name': name,
        'count': len(files),
        'width': width,
        'quality': quality,
        'source_duration_s': round(dur, 3),
        'total_kb': round(total_kb, 1),
        'largest_frame_kb': round(biggest_kb, 1),
        'pattern': '%03d.webp',
    }
    with open(os.path.join(outdir, 'manifest.json'), 'w') as fh:
        json.dump(manifest, fh, indent=2)

    print('%-18s %d frame · %dpx · tổng %.0f KB · frame nặng nhất %.0f KB'
          % (name, len(files), width, total_kb, biggest_kb))

    bad = False
    if total_kb > MAX_TOTAL_KB:
        print('   !! tổng %.0f KB > ngưỡng %d KB — giảm số frame hoặc hạ quality'
              % (total_kb, MAX_TOTAL_KB))
        bad = True
    if biggest_kb > MAX_FRAME_KB:
        print('   !! frame nặng nhất %.0f KB > ngưỡng %d KB — hạ width hoặc quality'
              % (biggest_kb, MAX_FRAME_KB))
        bad = True
    if not bad:
        print('   OK, trong ngân sách.')
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    video = sys.argv[1]
    name = sys.argv[2]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    width = int(sys.argv[4]) if len(sys.argv) > 4 else 900
    quality = int(sys.argv[5]) if len(sys.argv) > 5 else 72
    if not os.path.isfile(video):
        print('Không thấy file video: %s' % video)
        return 1
    return build(video, name, count, width, quality)


if __name__ == '__main__':
    sys.exit(main())
