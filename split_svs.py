import os
from openslide import OpenSlide
import pyvips
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

input_dir = '/mnt/raid/zanzhuheng/working/ESCC-2025-03-07'
output_dir = os.path.join(input_dir, 'quadrants_svs')
os.makedirs(output_dir, exist_ok=True)

svs_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.svs')]

def slide_to_vips_image(slide, x, y, w, h):
    region = slide.read_region((x, y), 0, (w, h)).convert("RGB")
    return pyvips.Image.new_from_memory(region.tobytes(), w, h, 3, "uchar")

def save_quadrants(filename):
    try:
        filepath = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]

        # 检查是否所有的四个象限文件都存在，如果存在就跳过
        expected_files = [
            os.path.join(output_dir, f"{base_name}_q1.tiff"),
            os.path.join(output_dir, f"{base_name}_q2.tiff"),
            os.path.join(output_dir, f"{base_name}_q3.tiff"),
            os.path.join(output_dir, f"{base_name}_q4.tiff"),
        ]
        if all(os.path.exists(f) for f in expected_files):
            return  # ✅ 全部存在，跳过

        slide = OpenSlide(filepath)

        width, height = slide.dimensions
        half_w, half_h = width // 2, height // 2
        coords = {
            "q1": (0, 0, half_w, half_h),
            "q2": (half_w, 0, width - half_w, half_h),
            "q3": (0, half_h, half_w, height - half_h),
            "q4": (half_w, half_h, width - half_w, height - half_h),
        }

        for quadrant, (x, y, w, h) in coords.items():
            out_path = os.path.join(output_dir, f"{base_name}_{quadrant}.tiff")
            if os.path.exists(out_path):  # ✅ 单独跳过已存在象限（可选）
                continue
            vips_img = slide_to_vips_image(slide, x, y, w, h)
            vips_img.tiffsave(
                out_path, compression="jpeg",
                tile=True, tile_width=256, tile_height=256,
                pyramid=True, bigtiff=True
            )

        slide.close()
    except Exception as e:
        print(f"Error processing {filename}: {e}")


max_workers = 8
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(save_quadrants, f) for f in svs_files]
    for _ in tqdm(as_completed(futures), total=len(futures), desc="Splitting & Saving SVS"):
        pass
