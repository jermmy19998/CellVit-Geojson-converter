Few Tools for CellVit

split_svs.py
(Splits SVS files into 4 parts. Since WSIs are extremely large, the output JSON files can sometimes be too big to open on some PCs.)

geojson_converter.py
(The output GeoJSON files from CellVit are not directly editable. I made several modifications to make the GeoJSON files editable, so you can fix incorrect masks in QuPath.)

convert_tiff2svs.py
(A simple script that replaces file suffixes to convert TIFF files into SVS format.)
