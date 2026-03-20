# Aegis FloodBase

**Version:** 3.1.0

**Type:** Hydrological Intelligence & Rapid Assessment System

Aegis FloodBase is a lightweight, edge-computed web application designed for rapid flood risk assessment in field environments. By utilizing browser-native capabilities, it transforms standard smartphone optical sensors into multi-spectral diagnostic tools, eliminating the need for complex backend processing during network-degraded crisis scenarios.

## Core Architecture

The system operates strictly on the client side, ensuring maximum privacy and zero latency after the initial load. It relies on a three-tier analysis pipeline applied to the HTML5 Canvas image buffer.

### Multi-Factor Diagnostic Engine

Standard image recognition struggles with unpredictable lighting and terrain. Aegis circumvents this by using a deterministic heuristic algorithm to measure three key environmental indicators:

1. **Silt Density ($S_{silt}$):** Scans the pixel array for specific RGB ratios (where $R > G > B$) that indicate sediment-heavy water, distinguishing it from vegetation, asphalt, or clean standing water.
2. **Surface Uniformity ($S_{uniform}$):** Calculates per-pixel variance across color channels. Fluid surfaces typically exhibit lower texture variance compared to dry ground or debris fields.
3. **Reflectivity Index ($S_{reflect}$):** Measures specular highlights and local luminance peaks to detect the mirror-like properties of pooled water.

### Mathematical Model

The aggregated risk factor ($R_{total}$) is calculated using a weighted formula optimized for turbid floodwater detection:

$$R_{total} = (0.55 \times S_{silt}) + (0.35 \times S_{uniform}) + (0.10 \times S_{reflect})$$

* **$R_{total} > 0.30$:** CRITICAL (High probability of severe flooding).
* **$0.12 < R_{total} \le 0.30$:** ELEVATED (Advisory level; moderate risk).
* **$R_{total} \le 0.12$:** NOMINAL (Stable conditions).

## Implementation & Usage

### Prerequisites
* A modern web browser (Chrome 90+, Safari 14+, Firefox 88+).
* HTTPS context (required to access the Geolocation and MediaDevices APIs).

### Deployment
Because Aegis FloodBase contains no backend dependencies or build steps, it can be deployed directly to any static file host:
* GitHub Pages
* Netlify
* AWS S3 (Static Website Hosting)

### Features
* **Zero-Dependency UI:** Styled via CDN-delivered TailwindCSS.
* **Event Logging:** Integrated system console for real-time diagnostic output.
* **Geospatial Sync:** Automatic GPS coordinate fetching mapped via Leaflet.js and CartoDB base layers.
* **Hardware Fallbacks:** Graceful error handling if camera permissions are denied, allowing manual photo upload.

## Security & Privacy

All image processing and location mapping occur locally on the device. No visual telemetry or geospatial coordinates are transmitted to external servers.
