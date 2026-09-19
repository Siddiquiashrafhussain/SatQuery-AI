"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { GroundViewPoint } from "@/lib/aoiGroundView";
import {
  GROUND_VIEW_DISCLOSURE,
  GROUND_VIEW_PANORAMA_HINT,
  formatGroundViewCoordinates,
  formatGroundViewHeading,
  headingFromPan,
  initialPanPercent,
  panoramaTranslatePercent,
} from "@/lib/aoiGroundView";
import {
  findNearbyImage,
  isMapillaryAvailable,
  type MapillaryImage,
} from "@/lib/mapillaryService";

type Props = {
  point: GroundViewPoint;
  onClose: () => void;
};

type MapillaryState = {
  loading: boolean;
  image: MapillaryImage | null;
  failed: boolean;
};

const MAPILLARY_DISCLOSURE =
  "Street-level imagery provided by Mapillary (© Mapillary, a Meta company). Coverage and recency vary by location.";

export function GroundViewOverlay({ point, onClose }: Props) {
  const [pan, setPan] = useState(() => initialPanPercent(point.heading));
  const dragRef = useRef<{ startX: number; startPan: number; pointerId: number } | null>(null);
  const stageRef = useRef<HTMLDivElement>(null);

  const [mapillary, setMapillary] = useState<MapillaryState>({
    loading: false,
    image: null,
    failed: false,
  });

  // Attempt Mapillary lookup when the overlay opens
  useEffect(() => {
    if (!isMapillaryAvailable()) {
      setMapillary({ loading: false, image: null, failed: false });
      return;
    }

    let cancelled = false;
    setMapillary({ loading: true, image: null, failed: false });

    void findNearbyImage(point.latitude, point.longitude).then((result) => {
      if (cancelled) return;
      if (result) {
        setMapillary({ loading: false, image: result, failed: false });
      } else {
        setMapillary({ loading: false, image: null, failed: true });
      }
    });

    return () => {
      cancelled = true;
    };
  }, [point.id, point.latitude, point.longitude]);

  useEffect(() => {
    setPan(initialPanPercent(point.heading));
  }, [point.id, point.heading]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
      }
    };

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [onClose]);

  const updatePanFromDelta = useCallback((deltaX: number) => {
    const stage = stageRef.current;
    if (!stage || !dragRef.current) return;
    const deltaPan = deltaX / stage.clientWidth;
    const next = Math.min(1, Math.max(0, dragRef.current.startPan - deltaPan));
    setPan(next);
  }, []);

  const onPointerDown = (event: React.PointerEvent<HTMLDivElement>) => {
    // Disable drag-to-pan when showing Mapillary iframe (it has its own controls)
    if (mapillary.image) return;
    if (!point.panorama360) return;
    dragRef.current = {
      startX: event.clientX,
      startPan: pan,
      pointerId: event.pointerId,
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const onPointerMove = (event: React.PointerEvent<HTMLDivElement>) => {
    if (!dragRef.current || dragRef.current.pointerId !== event.pointerId) return;
    updatePanFromDelta(event.clientX - dragRef.current.startX);
  };

  const onPointerUp = (event: React.PointerEvent<HTMLDivElement>) => {
    if (!dragRef.current || dragRef.current.pointerId !== event.pointerId) return;
    dragRef.current = null;
    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId);
    }
  };

  const usingMapillary = mapillary.image != null;
  const displayHeading = usingMapillary
    ? mapillary.image!.heading
    : headingFromPan(point.heading, pan);
  const translatePercent =
    !usingMapillary && point.panorama360
      ? panoramaTranslatePercent(pan, point.panoramaSpan)
      : 0;

  const effectiveTitle = usingMapillary
    ? mapillary.image!.isPano
      ? "360° street-level panorama"
      : "Street-level context"
    : point.title;

  const effectiveDescription = usingMapillary
    ? `Live street-level imagery from Mapillary. Image ID: ${mapillary.image!.id}.`
    : point.description;

  const effectiveCaptureDate = usingMapillary
    ? mapillary.image!.captureDate
    : point.captureDate;

  const effectiveDisclosure = usingMapillary ? MAPILLARY_DISCLOSURE : GROUND_VIEW_DISCLOSURE;

  return (
    <div
      className="ground-view-overlay"
      data-testid="ground-view-overlay"
      role="dialog"
      aria-modal="true"
      aria-label={`Ground View: ${effectiveTitle}`}
    >
      <button
        type="button"
        className="ground-view-overlay__close"
        data-testid="ground-view-close"
        onClick={onClose}
        aria-label="Close Ground View"
      >
        ×
      </button>

      <div
        ref={stageRef}
        className={`ground-view-overlay__stage${!usingMapillary && point.panorama360 ? " ground-view-overlay__stage--panorama" : ""}`}
        data-testid="ground-view-stage"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
      >
        {mapillary.loading ? (
          <div className="ground-view-overlay__loading" data-testid="ground-view-loading">
            <p>Loading street-level imagery…</p>
          </div>
        ) : usingMapillary ? (
          <iframe
            src={mapillary.image!.embedUrl}
            className="ground-view-overlay__iframe"
            data-testid="ground-view-mapillary-iframe"
            title={`Mapillary street view near (${point.latitude.toFixed(5)}, ${point.longitude.toFixed(5)})`}
            allow="fullscreen"
            loading="lazy"
          />
        ) : (
          <>
            <div
              className="ground-view-overlay__frame"
              style={
                point.panorama360
                  ? {
                      width: `${point.panoramaSpan * 100}%`,
                      transform: `translateX(${translatePercent}%)`,
                    }
                  : undefined
              }
            >
              <img
                src={point.imageUrl}
                alt={point.imageAlt}
                className="ground-view-overlay__image"
                data-testid="ground-view-image"
                draggable={false}
              />
            </div>
            <div className="ground-view-overlay__vignette" aria-hidden="true" />
            {point.panorama360 ? (
              <p className="ground-view-overlay__pan-hint" data-testid="ground-view-panorama-hint">
                {GROUND_VIEW_PANORAMA_HINT}
              </p>
            ) : null}
          </>
        )}
      </div>

      <div className="ground-view-overlay__meta">
        <p className="ground-view-overlay__eyebrow">Ground View</p>
        {usingMapillary ? (
          <span
            className="ground-view-overlay__badge ground-view-overlay__badge--live"
            data-testid="ground-view-mapillary-badge"
          >
            MAPILLARY
          </span>
        ) : (
          <span className="ground-view-overlay__badge" data-testid="ground-view-demo-badge">
            DEMO DATA
          </span>
        )}
        {!usingMapillary && point.panorama360 ? (
          <span className="ground-view-overlay__badge ground-view-overlay__badge--muted">
            Mock 360°
          </span>
        ) : null}
        <h2 className="ground-view-overlay__title" data-testid="ground-view-title">
          {effectiveTitle}
        </h2>
        <p className="ground-view-overlay__description" data-testid="ground-view-description">
          {effectiveDescription}
        </p>
        <dl className="ground-view-overlay__details">
          <div>
            <dt>Coordinates</dt>
            <dd data-testid="ground-view-coordinates">
              {formatGroundViewCoordinates(point.latitude, point.longitude)}
            </dd>
          </div>
          <div>
            <dt>Heading</dt>
            <dd data-testid="ground-view-heading">{formatGroundViewHeading(displayHeading)}</dd>
          </div>
          <div>
            <dt>Capture date</dt>
            <dd data-testid="ground-view-capture-date">{effectiveCaptureDate}</dd>
          </div>
        </dl>
        <p className="ground-view-overlay__disclosure" data-testid="ground-view-disclosure">
          {effectiveDisclosure}
        </p>
      </div>
    </div>
  );
}

