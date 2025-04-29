import json
import os
import threading
from queue import Queue
from tqdm import tqdm
import copy

def process_feature(feature, pbar, lock, new_features):
    try:
        feature_copy = copy.deepcopy(feature)
        properties = feature_copy.get("properties", {})
        
        if "classification" not in properties:
            properties["classification"] = {
                "name": "Epithelial",
                "color": [255, 159, 68]
            }
        if "objectType" not in properties:
            properties["objectType"] = "annotation"

        processed_features = []
        
        if feature_copy["geometry"]["type"] == "MultiPolygon":
            for idx, polygon_coords in enumerate(feature_copy["geometry"]["coordinates"], start=1):
                new_feature = {
                    "type": "Feature",
                    "id": f"{feature_copy['id']}-polygon-{idx}",
                    "geometry": {"type": "Polygon", "coordinates": polygon_coords},
                    "properties": copy.deepcopy(properties)
                }
                processed_features.append(new_feature)
        else:
            processed_features.append(feature_copy)
        
        with lock:
            new_features.extend(processed_features)
            pbar.update(1)
    except Exception as e:
        print(f"Error processing feature {feature.get('id')}: {e}")

def worker(feature_queue, pbar, lock, new_features):
    while True:
        feature = feature_queue.get()
        if feature is None:
            feature_queue.task_done()
            break
        process_feature(feature, pbar, lock, new_features)
        feature_queue.task_done()

def process_single_file(input_path, output_path):
    with open(input_path, "r") as f:
        raw_data = json.load(f)
    
    geojson = raw_data if isinstance(raw_data, dict) else {
        "type": "FeatureCollection",
        "features": raw_data
    }
    
    feature_queue = Queue()
    for feature in geojson["features"]:
        feature_queue.put(feature)
    
    new_features = []
    lock = threading.Lock()
    total = len(geojson["features"])
    
    pbar = tqdm(total=total, desc=f"Processing {os.path.basename(output_path)}", unit="feature")
    
    num_threads = 16
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(
            target=worker,
            args=(feature_queue, pbar, lock, new_features)
        )
        t.start()
        threads.append(t)
    
    feature_queue.join()
    
    for _ in range(num_threads):
        feature_queue.put(None)
    for t in threads:
        t.join()
    pbar.close()
    
    new_geojson = {
        "type": "FeatureCollection",
        "features": new_features
    }
    
    with open(output_path, "w") as f:
        json.dump(new_geojson, f, indent=2)

def main():
    base_dir = "path/to/input" # data structure just like CellViT output structure
    output_dir = "path/to/output" 
    
    os.makedirs(output_dir, exist_ok=True)
    
    sample_folders = [d for d in os.listdir(base_dir) 
                     if os.path.isdir(os.path.join(base_dir, d))]
    
    main_pbar = tqdm(sample_folders, desc="Overall Progress", unit="sample")
    
    for sample_id in main_pbar:
        input_path = os.path.join(
            base_dir, sample_id, "cell_detection", "cells.geojson"
        )
        output_path = os.path.join(output_dir, f"{sample_id}.geojson")
        
        if not os.path.exists(input_path):
            print(f"Warning: {input_path} does not exist, skipping")
            continue
        
        main_pbar.set_postfix({"Current Sample": sample_id})
        process_single_file(input_path, output_path)
    
    main_pbar.close()
    print(f"All processing completed! Results saved to {output_dir}")

if __name__ == "__main__":
    main()
