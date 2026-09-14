'use client';
import { useMemo } from 'react';
import Map, { Source, Layer, NavigationControl } from 'react-map-gl/maplibre';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

// The formal interface for the Map Architecture
export interface MapLayerConfig {
  id: string;
  type: 'raster' | 'geojson' | 'bbox';
  url?: string; // For raster tiles
  data?: any; // For GeoJSON
  opacity?: number;
  visible?: boolean;
}

interface MapViewerProps {
  layers?: MapLayerConfig[];
  center?: [number, number]; // [longitude, latitude]
  zoom?: number;
}

export default function MapViewer({ 
    layers = [], 
    center = [77.2090, 28.6139], // Default: New Delhi (ISRO Context)
    zoom = 12 
}: MapViewerProps) {
  
  // Base map style (OpenStreetMap)
  const mapStyle = useMemo(() => ({
    version: 8,
    sources: {
      osm: {
        type: 'raster',
        tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
        tileSize: 256,
        attribution: '&copy; OpenStreetMap Contributors'
      }
    },
    layers: [
      {
        id: 'osm-layer',
        type: 'raster',
        source: 'osm',
        minzoom: 0,
        maxzoom: 19
      }
    ]
  }), []);

  return (
    <div className="w-full h-full relative rounded-xl overflow-hidden border border-white/10 shadow-lg bg-black">
      <Map
        initialViewState={{
          longitude: center[0],
          latitude: center[1],
          zoom: zoom
        }}
        mapStyle={mapStyle as any}
        mapLib={maplibregl}
        style={{ width: '100%', height: '100%' }}
      >
        <NavigationControl position="bottom-right" />
        
        {/* Dynamic Layer Rendering Architecture */}
        {layers.map((layer) => {
           if (layer.visible === false) return null;
           
           if (layer.type === 'geojson' && layer.data) {
               return (
                 <Source key={layer.id} id={layer.id} type="geojson" data={layer.data}>
                   <Layer 
                     id={`${layer.id}-fill`} 
                     type="fill" 
                     paint={{
                       'fill-color': '#3b82f6', // sat-accent
                       'fill-opacity': layer.opacity ?? 0.3
                     }} 
                   />
                   <Layer 
                     id={`${layer.id}-line`} 
                     type="line" 
                     paint={{
                       'line-color': '#2563eb', // sat-accent-hover
                       'line-width': 2
                     }} 
                   />
                 </Source>
               );
           }
           
           if (layer.type === 'raster' && layer.url) {
               return (
                   <Source key={layer.id} id={layer.id} type="raster" tiles={[layer.url]} tileSize={256}>
                       <Layer 
                          id={`${layer.id}-layer`} 
                          type="raster" 
                          paint={{ 'raster-opacity': layer.opacity ?? 1.0 }} 
                       />
                   </Source>
               );
           }
           
           return null;
        })}
      </Map>

      {/* Coordinate Display Overlay Stub */}
      <div className="absolute bottom-4 right-14 z-10 glass-panel px-3 py-1 text-xs font-mono text-gray-400">
        Lng: {center[0].toFixed(4)}, Lat: {center[1].toFixed(4)}
      </div>
    </div>
  );
}
