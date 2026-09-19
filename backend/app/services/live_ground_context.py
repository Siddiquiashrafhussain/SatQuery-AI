"""Live ground-level context service — Mapillary API v4 with mock fallback.

When ``MAPILLARY_ACCESS_TOKEN`` is configured, queries the Mapillary Image
Radius Search endpoint to find the nearest street-level image for a given
change region centroid.  When the token is absent *or* no Mapillary coverage
exists within the search radius, falls back to the existing deterministic
mock panoramas.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.errors import SatQueryError
from app.schemas.ground_context import (
    GroundContextImage,
    GroundContextLocation,
    GroundContextProvenance,
    GroundContextResult,
    GroundContextScene,
    MAPILLARY_GROUND_DISCLOSURE,
)
from app.services.mock_ground_context import (
    MockGroundContextService,
    build_ground_context,
    polygon_centroid_wgs84,
    resolve_direction_hint,
    resolve_scene_category,
    deterministic_heading,
    deterministic_capture_date,
)
from app.services.region_interpretation import _find_region
from app.services.session_store import SessionStore, session_store

logger = logging.getLogger(__name__)

_MAPILLARY_GRAPH_URL = "https://graph.mapillary.com/images"
_SEARCH_RADIUS_M = 50


def _mapillary_radius_search(
    lat: float,
    lng: float,
    token: str,
    *,
    radius: int = _SEARCH_RADIUS_M,
) -> dict[str, Any] | None:
    """Query Mapillary API v4 Image Radius Search.

    Returns the closest image metadata dict or ``None`` when no coverage.
    """
    try:
        response = httpx.get(
            _MAPILLARY_GRAPH_URL,
            params={
                "access_token": token,
                "fields": "id,captured_at,compass_angle,geometry,is_pano",
                "bbox": _bbox_from_point(lng, lat, radius),
                "limit": 1,
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        features = data.get("data", [])
        if not features:
            return None
        return features[0]
    except Exception:
        logger.warning("Mapillary API request failed; falling back to mock.", exc_info=True)
        return None


def _bbox_from_point(lng: float, lat: float, radius_m: int) -> str:
    """Compute a rough bounding box string for the Mapillary bbox filter.

    Uses a simple approximation: 1 degree ≈ 111,320 m at the equator.
    """
    import math

    delta_lat = radius_m / 111_320
    delta_lng = radius_m / (111_320 * math.cos(math.radians(lat)))
    return f"{lng - delta_lng},{lat - delta_lat},{lng + delta_lng},{lat + delta_lat}"


class LiveGroundContextService:
    """Ground context with Mapillary live imagery + mock fallback."""

    def __init__(self, store: SessionStore | None = None) -> None:
        self._store = store or session_store
        self._mock = MockGroundContextService(store=self._store)

    def get_ground_context(self, session_id: str, region_id: str) -> GroundContextResult:
        settings = get_settings()
        token = settings.mapillary_access_token

        # Fast path: no token → delegate entirely to mock
        if not token:
            return self._mock.get_ground_context(session_id, region_id)

        session = self._store.get(session_id)
        if not session or not session.result:
            raise SatQueryError(
                "session_not_found",
                f"No result for session: {session_id}",
                status_code=404,
            )

        result = session.result
        if not result.bi_temporal_change:
            raise SatQueryError(
                "not_bi_temporal_session",
                "Ground context requires a bi-temporal analysis session.",
                status_code=422,
            )

        region = _find_region(result, region_id)
        lon, lat = polygon_centroid_wgs84(region.geometry.model_dump())

        # Try Mapillary
        mapillary_image = _mapillary_radius_search(lat, lon, token)

        if mapillary_image:
            return self._build_mapillary_context(
                session_id=session_id,
                region=region,
                result=result,
                lat=lat,
                lon=lon,
                mapillary=mapillary_image,
            )

        # Fallback to mock when no Mapillary coverage
        logger.info(
            "No Mapillary coverage at (%.5f, %.5f) for region %s; using mock.",
            lat, lon, region_id,
        )
        return build_ground_context(session_id=session_id, region=region, result=result)

    def _build_mapillary_context(
        self,
        *,
        session_id: str,
        region: Any,
        result: Any,
        lat: float,
        lon: float,
        mapillary: dict[str, Any],
    ) -> GroundContextResult:
        image_id = str(mapillary["id"])
        compass_angle = float(mapillary.get("compass_angle", 0))
        heading = compass_angle % 360

        # Mapillary captured_at is a Unix timestamp in ms
        captured_at_ms = mapillary.get("captured_at")
        if captured_at_ms:
            from datetime import UTC, datetime
            capture_date = datetime.fromtimestamp(captured_at_ms / 1000, tz=UTC).date().isoformat()
        else:
            capture_date = deterministic_capture_date(
                session_id, region.id, later_acquisition=None,
            )

        is_pano = mapillary.get("is_pano", False)
        direction_hint = resolve_direction_hint(region, result)
        category = resolve_scene_category(direction_hint)

        embed_url = f"https://www.mapillary.com/embed?image_key={image_id}&style=photo"

        return GroundContextResult(
            session_id=session_id,
            region_id=region.id,
            location=GroundContextLocation(latitude=lat, longitude=lon),
            heading=heading,
            capture_date=capture_date,
            scene=GroundContextScene(
                category=category,
                title="Street-level context" if not is_pano else "360° street-level panorama",
                description=(
                    f"Live street-level imagery from Mapillary near the change region centroid. "
                    f"Image ID: {image_id}."
                ),
                features=[
                    "street-level perspective",
                    "real-world imagery",
                    f"heading {heading:.0f}°",
                    "panoramic" if is_pano else "directional",
                ],
            ),
            image=GroundContextImage(
                asset_id=f"mapillary-{image_id}",
                url=embed_url,
                alt=f"Mapillary street-level image {image_id} near ({lat:.5f}, {lon:.5f})",
            ),
            provenance=GroundContextProvenance(
                provider="mapillary",
                source_type="street_level",
                status="live_street_level",
                real_world_imagery=True,
                disclosure=MAPILLARY_GROUND_DISCLOSURE,
            ),
        )


live_ground_context_service = LiveGroundContextService()

