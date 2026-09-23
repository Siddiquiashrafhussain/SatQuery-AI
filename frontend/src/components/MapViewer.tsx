"use client";
import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface MapViewerProps {
  activeScene?: any | null;
  activePair?: any | null;
  activeQueryResult?: any | null;
}

export default function MapViewer({ activeScene, activePair, activeQueryResult }: MapViewerProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (map.current || !mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
      center: [0, 0],
      zoom: 1
    });

    map.current.on('load', () => {
      setMapLoaded(true);
    });

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapLoaded || !map.current || !activeScene || !activeScene.bbox) return;

    const [minLon, minLat, maxLon, maxLat] = activeScene.bbox;
    
    // Auto zoom
    map.current.fitBounds([
      [minLon, minLat],
      [maxLon, maxLat]
    ], { padding: 50, duration: 1000 });

    const sourceId = 'scene-bounds-source';
    const layerId = 'scene-bounds-layer';

    const geojsonData: GeoJSON.FeatureCollection = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [minLon, minLat],
            [maxLon, minLat],
            [maxLon, maxLat],
            [minLon, maxLat],
            [minLon, minLat]
          ]]
        }
      }]
    };

    if (map.current.getSource(sourceId)) {
      (map.current.getSource(sourceId) as maplibregl.GeoJSONSource).setData(geojsonData);
    } else {
      map.current.addSource(sourceId, {
        type: 'geojson',
        data: geojsonData
      });

      map.current.addLayer({
        id: layerId,
        type: 'line',
        source: sourceId,
        layout: {},
        paint: {
          'line-color': '#2563eb', // blue-600
          'line-width': 3,
          'line-dasharray': [2, 2]
        }
      });
      
      map.current.addLayer({
        id: layerId + '-fill',
        type: 'fill',
        source: sourceId,
        layout: {},
        paint: {
          'fill-color': '#2563eb',
          'fill-opacity': 0.1
        }
      });
    }
  }, [activeScene, mapLoaded]);

    // Handle Grounding Overlay from Query Results
  useEffect(() => {
    if (!mapLoaded || !map.current || !activeScene || !activeScene.bbox) return;

    const sourceId = 'grounding-boxes-source';
    const layerId = 'grounding-boxes-layer';
    
    // Clear previous if no result or no boxes
    if (!activeQueryResult || !activeQueryResult.bounding_boxes || activeQueryResult.bounding_boxes.length === 0) {
        if (map.current.getSource(sourceId)) {
            (map.current.getSource(sourceId) as maplibregl.GeoJSONSource).setData({
                type: 'FeatureCollection',
                features: []
            });
        }
        return;
    }

    const [minLon, minLat, maxLon, maxLat] = activeScene.bbox;
    const width = maxLon - minLon;
    const height = maxLat - minLat;

    const features: GeoJSON.Feature[] = activeQueryResult.bounding_boxes.map((box: number[]) => {
      const [x1, y1, x2, y2] = box;
      // Florence-2 y=0 is top, which corresponds to maxLat.
      const boxMinLon = minLon + (x1 * width);
      const boxMaxLat = maxLat - (y1 * height);
      const boxMaxLon = minLon + (x2 * width);
      const boxMinLat = maxLat - (y2 * height);

      return {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [boxMinLon, boxMinLat],
            [boxMaxLon, boxMinLat],
            [boxMaxLon, boxMaxLat],
            [boxMinLon, boxMaxLat],
            [boxMinLon, boxMinLat]
          ]]
        }
      };
    });

    const geojsonData: GeoJSON.FeatureCollection = {
      type: 'FeatureCollection',
      features
    };

    if (map.current.getSource(sourceId)) {
      (map.current.getSource(sourceId) as maplibregl.GeoJSONSource).setData(geojsonData);
    } else {
      map.current.addSource(sourceId, {
        type: 'geojson',
        data: geojsonData
      });

      map.current.addLayer({
        id: layerId,
        type: 'line',
        source: sourceId,
        layout: {},
        paint: {
          'line-color': '#f59e0b', // amber-500
          'line-width': 3
        }
      });
      
      map.current.addLayer({
        id: layerId + '-fill',
        type: 'fill',
        source: sourceId,
        layout: {},
        paint: {
          'fill-color': '#f59e0b',
          'fill-opacity': 0.3
        }
      });
    }
    
    // Auto zoom to grounded boxes if they exist
    if (features.length > 0) {
        const bounds = new maplibregl.LngLatBounds();
        features.forEach(f => {
            if (f.geometry.type === 'Polygon') {
                f.geometry.coordinates[0].forEach(coord => {
                    bounds.extend(coord as [number, number]);
                });
            }
        });
        map.current.fitBounds(bounds, { padding: 100, duration: 800, maxZoom: 16 });
    }
  }, [activeQueryResult, activeScene, mapLoaded]);

  const [viewMode, setViewMode] = useState<"before" | "after" | "diff">("before");

  useEffect(() => {
    if (!mapLoaded || !map.current || !activePair || !activePair.beforeScene || !activePair.beforeScene.bbox) return;
    
    const [minLon, minLat, maxLon, maxLat] = activePair.beforeScene.bbox;
    map.current.fitBounds([
      [minLon, minLat],
      [maxLon, maxLat]
    ], { padding: 50, duration: 1000 });
    
    const sourceId = 'pair-bounds-source';
    const layerId = 'pair-bounds-layer';
    
    const geojsonData: GeoJSON.FeatureCollection = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [minLon, minLat],
            [maxLon, minLat],
            [maxLon, maxLat],
            [minLon, maxLat],
            [minLon, minLat]
          ]]
        }
      }]
    };

    if (map.current.getSource(sourceId)) {
      (map.current.getSource(sourceId) as maplibregl.GeoJSONSource).setData(geojsonData);
    } else {
      map.current.addSource(sourceId, {
        type: 'geojson',
        data: geojsonData
      });

      map.current.addLayer({
        id: layerId,
        type: 'line',
        source: sourceId,
        layout: {},
        paint: {
          'line-color': viewMode === 'diff' ? '#ef4444' : '#10b981', // red or emerald
          'line-width': 3,
          'line-dasharray': [2, 2]
        }
      });
      
      map.current.addLayer({
        id: layerId + '-fill',
        type: 'fill',
        source: sourceId,
        layout: {},
        paint: {
          'fill-color': viewMode === 'diff' ? '#ef4444' : '#10b981',
          'fill-opacity': viewMode === 'diff' && activeQueryResult ? 0.4 : 0.1
        }
      });
    }
    
    // Update paint properties based on mode dynamically
    if (map.current.getLayer(layerId)) {
        map.current.setPaintProperty(layerId, 'line-color', viewMode === 'diff' ? '#ef4444' : '#10b981');
        map.current.setPaintProperty(layerId + '-fill', 'fill-color', viewMode === 'diff' ? '#ef4444' : '#10b981');
        map.current.setPaintProperty(layerId + '-fill', 'fill-opacity', viewMode === 'diff' && activeQueryResult ? 0.4 : 0.1);
    }
    
  }, [activePair, mapLoaded, viewMode, activeQueryResult]);

  return (
    <div className="absolute inset-0 w-full h-full">
      <div ref={mapContainer} className="w-full h-full" />
      
      {activePair && (
        <div className="absolute top-4 right-4 bg-white rounded-md shadow-md flex overflow-hidden border border-gray-200 z-10">
          <button 
            onClick={() => setViewMode("before")} 
            className={`px-4 py-2 text-xs font-semibold uppercase ${viewMode === "before" ? "bg-blue-600 text-white" : "text-gray-700 hover:bg-gray-50"}`}
          >
            Before
          </button>
          <button 
            onClick={() => setViewMode("after")} 
            className={`px-4 py-2 text-xs font-semibold uppercase border-l border-r border-gray-200 ${viewMode === "after" ? "bg-blue-600 text-white" : "text-gray-700 hover:bg-gray-50"}`}
          >
            After
          </button>
          <button 
            onClick={() => setViewMode("diff")} 
            className={`px-4 py-2 text-xs font-semibold uppercase ${viewMode === "diff" ? "bg-red-600 text-white" : "text-gray-700 hover:bg-gray-50"}`}
          >
            Diff
          </button>
        </div>
      )}
    </div>
  );
}
