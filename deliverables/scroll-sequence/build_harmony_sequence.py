"""
Tạo chuỗi 32 frame WebP và video MP4 từ các Keyframe Concept 'Harmony in Chaos' cho Scroll Sequence.
"""
import os
import json
import subprocess
from PIL import Image

BRAIN_DIR = r"C:\Users\jaker\.gemini\antigravity-ide\brain\ad4ae4ac-cb05-4049-9fa8-7b1352afde7f"
OUT_DIR = os.path.join(r"e:\Vitalite website\deliverables\scroll-sequence\frames\harmony_in_chaos")
VIDEO_OUT = os.path.join(r"e:\Vitalite website\deliverables\scroll-sequence\harmony_in_chaos.mp4")

os.makedirs(OUT_DIR, exist_ok=True)

# 7 Keyframe góc quay 360 độ
KEYFRAME_FILES = [
    "art_seq_01_front_1787443020408.jpg",
    "art_seq_02_turn45_1787443039325.jpg",
    "art_seq_03_profile_1787443063409.jpg",
    "art_seq_04_turn135_1787443092211.jpg",
    "art_seq_05_fullback_1787443116727.jpg",
    "art_seq_06_turn225_1787443136919.jpg",
    "art_seq_07_turn315_1787443156099.jpg",
]

keyframes = []
target_width = 900
for fname in KEYFRAME_FILES:
    p = os.path.join(BRAIN_DIR, fname)
    img = Image.open(p).convert("RGB")
    w, h = img.size
    new_h = int(h * (target_width / w))
    img_resized = img.resize((target_width, new_h), Image.Resampling.LANCZOS)
    keyframes.append(img_resized)

# Thêm lại frame 0 để hoàn tất vòng quay 360 khép kín
keyframes.append(keyframes[0])

TOTAL_FRAMES = 32
num_segments = len(keyframes) - 1  # 7 đoạn

generated_frames = []

for i in range(TOTAL_FRAMES):
    # Tính vị trí t trong khoảng [0, num_segments]
    t = (i / TOTAL_FRAMES) * num_segments
    seg_idx = int(t)
    local_t = t - seg_idx
    if seg_idx >= num_segments:
        seg_idx = num_segments - 1
        local_t = 1.0

    img_a = keyframes[seg_idx]
    img_b = keyframes[seg_idx + 1]

    # Smooth ease in out blending
    # Cosine easing: (1 - cos(pi * local_t)) / 2
    import math
    eased_t = (1.0 - math.cos(math.pi * local_t)) / 2.0

    blended = Image.blend(img_a, img_b, eased_t)
    
    frame_name = f"{i+1:03d}.webp"
    frame_path = os.path.join(OUT_DIR, frame_name)
    blended.save(frame_path, "WEBP", quality=75, method=6)
    generated_frames.append(frame_path)

# Thống kê dung lượng & sinh manifest.json
files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith('.webp'))
sizes = [os.path.getsize(os.path.join(OUT_DIR, f)) for f in files]
total_kb = sum(sizes) / 1024.0
biggest_kb = (max(sizes) / 1024.0) if sizes else 0

manifest = {
    'name': 'harmony_in_chaos',
    'count': len(files),
    'width': target_width,
    'quality': 75,
    'source_duration_s': 4.0,
    'total_kb': round(total_kb, 1),
    'largest_frame_kb': round(biggest_kb, 1),
    'pattern': '%03d.webp',
}
with open(os.path.join(OUT_DIR, 'manifest.json'), 'w') as fh:
    json.dump(manifest, fh, indent=2)

    print(f"Completed {len(files)} WebP frames at {OUT_DIR}")
    print(f"Total size: {total_kb:.1f} KB (Largest frame: {biggest_kb:.1f} KB)")

# Tao video MP4 bang ffmpeg tu chuoi 32 frame (8 fps -> video 4 giay)
cmd = [
    'ffmpeg', '-y', '-framerate', '8',
    '-i', os.path.join(OUT_DIR, '%03d.webp'),
    '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
    VIDEO_OUT
]
subprocess.run(cmd, check=True)
print(f"Video MP4 created at {VIDEO_OUT}")
