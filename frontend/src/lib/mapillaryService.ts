/**
 * Mapillary API v4 client for finding street-level images near a coordinate.
 *
 * Uses the Image Radius Search via the bbox filter on the /images endpoint.
 * Returns null (triggering mock fallback) when:
 *  - NEXT_PUBLIC_MAPILLARY_TOKEN is not set
 *  - No images are found within the search radius
 *  - The API request fails
 */

const MAPILLARY_TOKEN = process.env.NEXT_PUBLIC_MAPILLARY_TOKEN ?? "";
const MAPILLARY_GRAPH_URL = "https://graph.mapillary.com/images";
const SEARCH_RADIUS_M = 50;

export interface MapillaryImage {
  id: string;
  captureDate: string;
  heading: number;
  isPano: boolean;
  embedUrl: string;
}

function bboxFromPoint(lng: number, lat: number, radiusM: number): string {
  const deltaLat = radiusM / 111_320;
  const deltaLng = radiusM / (111_320 * Math.cos((lat * Math.PI) / 180));
  return `${lng - deltaLng},${lat - deltaLat},${lng + deltaLng},${lat + deltaLat}`;
}

export function isMapillaryAvailable(): boolean {
  return MAPILLARY_TOKEN.length > 0;
}

export async function findNearbyImage(
  lat: number,
  lng: number,
  radiusM: number = SEARCH_RADIUS_M,
): Promise<MapillaryImage | null> {
  if (!MAPILLARY_TOKEN) return null;

  try {
    const bbox = bboxFromPoint(lng, lat, radiusM);
    const params = new URLSearchParams({
      access_token: MAPILLARY_TOKEN,
      fields: "id,captured_at,compass_angle,is_pano",
      bbox,
      limit: "1",
    });

    const res = await fetch(`${MAPILLARY_GRAPH_URL}?${params.toString()}`);
    if (!res.ok) {
      console.warn("[Mapillary] API returned", res.status);
      return null;
    }

    const data = await res.json();
    const features = data?.data;
    if (!Array.isArray(features) || features.length === 0) return null;

    const img = features[0];
    const imageId = String(img.id);
    const compassAngle = Number(img.compass_angle ?? 0) % 360;
    const isPano = Boolean(img.is_pano);

    // captured_at is a Unix timestamp in milliseconds
    let captureDate = "Unknown";
    if (img.captured_at) {
      captureDate = new Date(img.captured_at).toISOString().slice(0, 10);
    }

    return {
      id: imageId,
      captureDate,
      heading: compassAngle,
      isPano,
      embedUrl: `https://www.mapillary.com/embed?image_key=${imageId}&style=photo`,
    };
  } catch (err) {
    console.warn("[Mapillary] Radius search failed; falling back to mock.", err);
    return null;
  }
}
