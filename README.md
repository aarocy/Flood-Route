# Flood-Route

## Project Overview
FloodRoute is an offline-capable, client-side data collection pipeline designed for field personnel to log environmental hazards during degraded network conditions. 

The repository consists of two distinct components:
1. **The Field Logger (`index.html`):** A browser-based web application for standardizing and storing incident data locally on a mobile device.
2. **The Data Parser (`parser.py`):** A Python script utilized by command centers to unpack the exported field data into actionable formats (CSV, JPEG, and HTML maps).

## Scope and Limitations
It is critical to understand the operational scope of this tool:
* **No Automated Detection:** FloodRoute does *not* utilize algorithmic image recognition, multi-spectral analysis, or AI to detect floodwater. 
* **Human-in-the-Loop Validation:** The system relies entirely on the human operator to visually assess the hazard and assign a severity tag (`NOMINAL`, `ELEVATED`, `CRITICAL`).
* **Data Standardization:** The primary utility of this software is enforcing a strict, standardized data schema (Timestamp + GPS Coordinates + Image + Severity Tag) rather than relying on disparate camera roll photos.

## System Architecture

### 1. Client-Side Web Application
The web interface is a zero-dependency HTML/JS file. It operates strictly on the client side to ensure offline survivability.
* **Storage Protocol:** Uses browser `localStorage` to persist data between sessions and page reloads.
* **Image Compression:** Raw device photos (often 3-5MB) will rapidly exceed the 5MB `localStorage` limit. The application utilizes a hidden HTML5 `<canvas>` element to compress images to a maximum width of 640px and convert them to base64 JPEG strings (quality ratio 0.6) prior to storage.
* **Geospatial Tracking:** Calls the native `navigator.geolocation` API. HTTPS is required to utilize this feature.

### 2. Command Center Parser
The Python script operates asynchronously from the web app. Once network connectivity is restored, the field user exports the `localStorage` ledger as a JSON payload.
* **Image Extraction:** The script parses the JSON, isolates the base64 URI strings, decodes them, and writes standard `.jpg` files to a local directory.
* **Tabular Formatting:** Strips the heavy image data from the JSON array and converts the remaining telemetry (Time, Lat, Lng, Severity) into a standardized CSV for GIS or database ingestion.
* **Geospatial Mapping:** Utilizes the `folium` library to generate a lightweight, static HTML map with color-coded markers representing the field logs.

## Deployment & Usage

### Hosting the Web App
Because `index.html` lacks backend dependencies, it can be hosted on any static file server (e.g., GitHub Pages, AWS S3, local intranet). HTTPS is mandatory for camera and GPS hardware access.

### Running the Python Parser
1. Ensure Python 3.x is installed.
2. Install dependencies: `pip install pandas folium`
3. Place the downloaded JSON export from the web app into the same directory as `parser.py`.
4. Ensure the `INPUT_JSON` variable in the script matches the downloaded filename.
5. Execute the script: `python parser.py`


## Licence
This Project is under the MIT licence.
---
