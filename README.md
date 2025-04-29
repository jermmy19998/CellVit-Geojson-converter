# 🧰 Few Tools for CellViT

This repository contains a few utility scripts to assist working with [CellViT](https://github.com/TIO-IKIM/CellViT) outputs.

## 🛠 Tools Included

1. **`split_svs.py`**  
   Split large `.svs` whole slide images into 4 quadrants. This helps avoid memory or visualization issues on machines that can't handle very large images.

2. **`geojson_converter.py`**  
   Modify the output `.geojson` files from CellViT so that they can be edited (e.g., fixing incorrect masks) in tools like QuPath.

3. **`convert_tiff2svs.py`**  
   Rename or convert `.tiff` files to `.svs` format via simple suffix replacement for compatibility or visualization.

## 🔗 Related Link

- **CellViT GitHub**: [https://github.com/TIO-IKIM/CellViT](https://github.com/TIO-IKIM/CellViT)

---

If you find this helpful, **please give a star ⭐️** — it really helps!



# 🧰 CellViT 工具集（Few Tools for CellViT）

本工具集包含了一些用于辅助处理 [CellViT](https://github.com/TIO-IKIM/CellViT) 输出结果的小工具。

## 🛠 包含工具

1. **`split_svs.py`**  
   将 `.svs` 格式的整张病理切片图像（Whole Slide Image, WSI）切分为四个象限。适用于图像太大导致部分电脑无法正常打开的情况。

2. **`geojson_converter.py`**  
   修改 CellViT 输出的 `.geojson` 文件，使其在 QuPath 中可编辑，便于手动修正分割错误的区域。

3. **`convert_tiff2svs.py`**  
   将 `.tiff` 文件重命名为 `.svs` 后缀，便于在某些工具中识别和加载图像。

## 🔗 相关链接

- **CellViT GitHub 项目**：[https://github.com/TIO-IKIM/CellViT](https://github.com/TIO-IKIM/CellViT)

---

如果这些工具对你有帮助，**欢迎点个 Star ⭐️ 支持一下！**
