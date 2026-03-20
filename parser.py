import json
import pandas as pd
import folium
import os
import base64

# Configuration Variables
INPUT_JSON = 'floodroute_export.json'
OUTPUT_CSV = 'parsed_triage_log.csv'
OUTPUT_MAP = 'incident_map.html'
IMAGE_DIR = 'incident_photos'

def process_ledger(json_filepath):
    print(f"Loading field ledger: {json_filepath}...")
    
    with open(json_filepath, 'r') as file:
        logs = json.load(file)

    if not logs:
        print("Error: Ledger is empty.")
        return

    # Initialize storage
    os.makedirs(IMAGE_DIR, exist_ok=True)
    table_data = []

    for log in logs:
        # 1. Image Extraction and Decoding
        image_filename = f"incident_{log['id']}.jpg"
        image_path = os.path.join(IMAGE_DIR, image_filename)
        
        if 'image' in log and log['image'].startswith('data:image'):
            try:
                # Split the data URI scheme from the actual base64 payload
                header, encoded = log['image'].split(',', 1)
                with open(image_path, "wb") as fh:
                    fh.write(base64.b64decode(encoded))
            except Exception as e:
                print(f"Failed to decode image for log {log['id']}: {e}")
                image_filename = "ERROR_DECODING"
        else:
            image_filename = "NO_IMAGE_DATA"

        # 2. Compile Tabular Data
        table_data.append({
            'ID': log['id'],
            'Timestamp': log['timestamp'],
            'Latitude': float(log['lat']),
            'Longitude': float(log['lng']),
            'Severity': log['severity'],
            'Local_Image': image_filename
        })

    # 3. Generate CSV
    df = pd.DataFrame(table_data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved tabular data to: {OUTPUT_CSV}")
    print(f"Extracted {len(df)} images to: {IMAGE_DIR}/")

    # 4. Generate Interactive Map
    if not df.empty:
        avg_lat = df['Latitude'].mean()
        avg_lng = df['Longitude'].mean()
        incident_map = folium.Map(location=[avg_lat, avg_lng], zoom_start=14, tiles='cartodbdark_matter')

        color_map = {
            'CRITICAL': 'red',
            'ELEVATED': 'orange',
            'NOMINAL': 'green'
        }

        for index, row in df.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"Severity: {row['Severity']}<br>Time: {row['Timestamp']}<br>File: {row['Local_Image']}",
                tooltip=row['Severity'],
                icon=folium.Icon(color=color_map.get(row['Severity'], 'blue'), icon='info-sign')
            ).add_to(incident_map)

        incident_map.save(OUTPUT_MAP)
        print(f"Saved interactive map to: {OUTPUT_MAP}")

if __name__ == "__main__":
    if os.path.exists(INPUT_JSON):
        process_ledger(INPUT_JSON)
    else:
        print(f"File '{INPUT_JSON}' not found. Verify the filename matches your downloaded export.")
