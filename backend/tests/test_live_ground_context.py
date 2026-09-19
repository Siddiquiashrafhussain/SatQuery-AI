"""Tests for the LiveGroundContextService — Mapillary integration with mock fallback."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from app.schemas.domain import AnalysisResult, AnalysisStatus, DataMode, EvidenceRegion
from app.schemas.domain import BiTemporalChangeResult
from app.schemas.ground_context import GroundContextResult
from app.services.live_ground_context import LiveGroundContextService, _mapillary_radius_search


def _make_evidence_region() -> EvidenceRegion:
    return EvidenceRegion(
        id="region-1",
        geometry={
            "type": "Polygon",
            "coordinates": [
                [
                    [77.56, 12.94],
                    [77.57, 12.94],
                    [77.57, 12.95],
                    [77.56, 12.95],
                    [77.56, 12.94],
                ]
            ],
        },
        type="spectral_change",
        confidence=0.72,
        metrics=[],
        source="deterministic_change_detector",
        metadata={"change_direction_hint": "built_up_increase"},
    )


def _make_result(session_id: str = "test-sess") -> AnalysisResult:
    region = _make_evidence_region()
    from datetime import datetime, UTC
    return AnalysisResult(
        status=AnalysisStatus.COMPLETED,
        session_id=session_id,
        answer="Test answer",
        confidence=0.72,
        metrics=[],
        evidence=[region],
        trace=[],
        mode=DataMode.DEVELOPMENT,
        bi_temporal_change=BiTemporalChangeResult(
            change_summary="Test change summary",
            question="What changed?",
            earlier_date="2024-01-01",
            later_date="2024-06-01",
            detector="deterministic",
            changed_region_count=1,
            provider="development",
            provenance="deterministic_change_detector v1.0.0",
            earlier_image_id="img-earlier",
            later_image_id="img-later",
            earlier_acquisition=datetime(2024, 1, 1, tzinfo=UTC),
            later_acquisition=datetime(2024, 6, 1, tzinfo=UTC),
        ),
    )


class TestMapillaryRadiusSearch:
    def test_returns_none_when_no_images(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("app.services.live_ground_context.httpx.get", return_value=mock_response):
            result = _mapillary_radius_search(12.945, 77.565, "test-token")
            assert result is None

    def test_returns_image_when_found(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "12345678",
                    "captured_at": 1704067200000,  # 2024-01-01T00:00:00Z
                    "compass_angle": 135.5,
                    "is_pano": True,
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("app.services.live_ground_context.httpx.get", return_value=mock_response):
            result = _mapillary_radius_search(12.945, 77.565, "test-token")
            assert result is not None
            assert result["id"] == "12345678"

    def test_returns_none_on_http_error(self):
        with patch(
            "app.services.live_ground_context.httpx.get",
            side_effect=Exception("Connection refused"),
        ):
            result = _mapillary_radius_search(12.945, 77.565, "test-token")
            assert result is None


class TestLiveGroundContextService:
    def test_falls_back_to_mock_when_no_token(self):
        """When MAPILLARY_ACCESS_TOKEN is not set, the service delegates to mock."""
        mock_store = MagicMock()
        result = _make_result()
        mock_session = MagicMock()
        mock_session.result = result
        mock_store.get.return_value = mock_session

        with patch(
            "app.services.live_ground_context.get_settings",
        ) as mock_settings:
            settings = MagicMock()
            settings.mapillary_access_token = None
            mock_settings.return_value = settings

            service = LiveGroundContextService(store=mock_store)
            ctx = service.get_ground_context("test-sess", "region-1")

            assert isinstance(ctx, GroundContextResult)
            assert ctx.provenance.provider == "mock_ground_context"
            assert ctx.provenance.real_world_imagery is False

    def test_uses_mapillary_when_token_set_and_coverage_found(self):
        """When token is set and Mapillary has coverage, returns live data."""
        mock_store = MagicMock()
        result = _make_result()
        mock_session = MagicMock()
        mock_session.result = result
        mock_store.get.return_value = mock_session

        mapillary_image = {
            "id": "99887766",
            "captured_at": 1719792000000,  # 2024-06-30
            "compass_angle": 45.0,
            "is_pano": False,
        }

        with (
            patch("app.services.live_ground_context.get_settings") as mock_settings,
            patch(
                "app.services.live_ground_context._mapillary_radius_search",
                return_value=mapillary_image,
            ),
        ):
            settings = MagicMock()
            settings.mapillary_access_token = "fake-token"
            mock_settings.return_value = settings

            service = LiveGroundContextService(store=mock_store)
            ctx = service.get_ground_context("test-sess", "region-1")

            assert isinstance(ctx, GroundContextResult)
            assert ctx.provenance.provider == "mapillary"
            assert ctx.provenance.source_type == "street_level"
            assert ctx.provenance.real_world_imagery is True
            assert "99887766" in ctx.image.url
            assert ctx.heading == 45.0

    def test_falls_back_to_mock_when_no_coverage(self):
        """When token is set but no Mapillary coverage, returns mock."""
        mock_store = MagicMock()
        result = _make_result()
        mock_session = MagicMock()
        mock_session.result = result
        mock_store.get.return_value = mock_session

        with (
            patch("app.services.live_ground_context.get_settings") as mock_settings,
            patch(
                "app.services.live_ground_context._mapillary_radius_search",
                return_value=None,
            ),
        ):
            settings = MagicMock()
            settings.mapillary_access_token = "fake-token"
            mock_settings.return_value = settings

            service = LiveGroundContextService(store=mock_store)
            ctx = service.get_ground_context("test-sess", "region-1")

            assert isinstance(ctx, GroundContextResult)
            assert ctx.provenance.provider == "mock_ground_context"
