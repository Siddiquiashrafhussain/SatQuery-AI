"use client";

import { useState } from "react";
import { Minus, Plus, Stack } from "@phosphor-icons/react";
import { SiteMenu } from "@/components/SiteMenu";

type LayerState = {
  detections: boolean;
  aoi: boolean;
};

type Props = {
  onZoomIn: () => void;
  onZoomOut: () => void;
  layers: LayerState;
  onLayersChange: (next: LayerState) => void;
  inspectorOpen?: boolean;
};

function LayerToggle({
  open,
  layers,
  onToggle,
  onLayersChange,
}: {
  open: boolean;
  layers: LayerState;
  onToggle: () => void;
  onLayersChange: (next: LayerState) => void;
}) {
  return (
    <div className="relative">
      <button
        type="button"
        data-testid="layer-toggle"
        className="map-tool-btn"
        aria-label="Layers"
        aria-expanded={open}
        onClick={onToggle}
      >
        <Stack size={20} weight="regular" />
      </button>
      {open ? (
        <div
          className="layer-popover glass absolute right-0 top-[calc(100%+4px)] w-[250px] p-3"
          role="group"
          aria-label="Map layers"
        >
          <div className="flex items-center gap-2 mb-3">
            <Stack size={16} className="text-blue-400" />
            <p className="composer-label text-[13px] font-semibold text-white m-0">Analysis Layers</p>
          </div>
          <div className="bg-sat-surface/50 rounded-md p-2 border border-sat-border/50">
            <label className="layer-check font-medium text-white mb-2 pb-2 border-b border-sat-border/50">
              <input
                type="checkbox"
                checked={layers.detections}
                onChange={(e) => onLayersChange({ ...layers, detections: e.target.checked })}
              />
              Physical Change Highlight
            </label>
            <div className="pl-6 space-y-2 text-[11px] text-[var(--text-muted)] flex flex-col">
              <div className="flex items-center gap-2 relative -left-[19px]">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-sm border border-red-600/20"></span> Vegetation Decrease / Deforestation
              </div>
              <div className="flex items-center gap-2 relative -left-[19px]">
                <span className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-sm border border-green-600/20"></span> Vegetation Increase / Growth
              </div>
              <div className="flex items-center gap-2 relative -left-[19px]">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-sm border border-blue-600/20"></span> Water Expansion / Gain
              </div>
              <div className="flex items-center gap-2 relative -left-[19px]">
                <span className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-sm border border-orange-600/20"></span> Built-up Growth / Urban Sprawl
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export function MapToolCluster({
  onZoomIn,
  onZoomOut,
  layers,
  onLayersChange,
  inspectorOpen = false,
}: Props) {
  const [open, setOpen] = useState(false);

  if (inspectorOpen) {
    return (
      <div className="map-tools map-tools--dock-inspector" data-testid="map-tools">
        <div
          className="map-tool-cluster map-tool-cluster--horizontal map-tool-cluster--pill glass"
          data-tour="map-tools"
        >
          <button type="button" className="map-tool-btn" aria-label="Zoom out" onClick={onZoomOut}>
            <Minus size={20} weight="regular" />
          </button>
          <button type="button" className="map-tool-btn" aria-label="Zoom in" onClick={onZoomIn}>
            <Plus size={20} weight="regular" />
          </button>
          <LayerToggle
            open={open}
            layers={layers}
            onToggle={() => setOpen((v) => !v)}
            onLayersChange={onLayersChange}
          />
          <span className="map-tool-cluster__divider" aria-hidden="true" />
          <SiteMenu variant="toolbar" />
        </div>
      </div>
    );
  }

  return (
    <div className="map-tools" data-testid="map-tools">
      <div className="map-tool-cluster glass" data-tour="map-tools">
        <LayerToggle
          open={open}
          layers={layers}
          onToggle={() => setOpen((v) => !v)}
          onLayersChange={onLayersChange}
        />
        <button type="button" className="map-tool-btn" aria-label="Zoom in" onClick={onZoomIn}>
          <Plus size={20} weight="regular" />
        </button>
        <button type="button" className="map-tool-btn" aria-label="Zoom out" onClick={onZoomOut}>
          <Minus size={20} weight="regular" />
        </button>
      </div>
    </div>
  );
}
