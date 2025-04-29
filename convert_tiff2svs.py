import os
import shutil

# 原始目录和目标目录
src_dir = "/mnt/raid/zanzhuheng/working/ESCC-2025-03-07/quadrants_svs"
dst_dir = "/mnt/raid/zanzhuheng/working/ESCC-2025-03-07/quadrants_tiff2svs"

# 创建目标目录（如果不存在）
os.makedirs(dst_dir, exist_ok=True)

# 遍历原始目录中的所有文件
for filename in os.listdir(src_dir):
    if filename.lower().endswith(".tiff"):
        src_path = os.path.join(src_dir, filename)
        new_filename = os.path.splitext(filename)[0] + ".svs"
        dst_path = os.path.join(dst_dir, new_filename)
        shutil.copy2(src_path, dst_path)

print("转换完成。")
