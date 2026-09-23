# SatQuery AI - Phase 6 Demo Script

This script provides a curated set of tested queries designed to showcase the full end-to-end capabilities of the SatQuery AI platform in a reliable, predictable manner for the final presentation. 

## Prerequisites
- The environment is seeded with `backend/scripts/seed_demo_data.py`.
- You are logged in as `demo@satquery.ai`.

---

### Query 1: Single Image VQA (Optical)
**Action**: Open `demo_optical_1.tif` in the Workstation.
**Query**: "Are there any roads visible in this region?"
**Expected Plan Output**: 
1. `vqa`
2. `gis_verify`
**Expected Verification**: `not_applicable` (No numeric spatial claim).
**Expected Result**: The model successfully describes the presence of roads, with a confidence score above 80%.

### Query 2: Single Image VQA with Hallucination Catch (Optical)
**Action**: Still on `demo_optical_1.tif`.
**Query**: "How many hectares of water are in this scene?"
**Expected Plan Output**: 
1. `vqa`
2. `gis_verify`
**Expected Verification**: `false` (Model hallucination caught by deterministic GIS verifier).
**Expected Result**: The Execution Trace correctly flags the hallucination, noting the mathematical mismatch between the claimed area and the projected bounding box area.

### Query 3: Graceful Failure on Unimplemented Tool
**Action**: Still on `demo_optical_1.tif`.
**Query**: "Segment all the buildings in this scene."
**Expected Plan Output**: 
1. `segmentation`
2. `vqa`
3. `gis_verify`
**Expected Verification**: `not_applicable` (Execution halts before verify).
**Expected Result**: The trace shows the `segmentation` tool failing loudly with a "Not Implemented: Segmentation tool is a future enhancement" message, proving the agent aborts gracefully instead of swallowing errors.

### Query 4: Optical-SAR Fusion
**Action**: Go to Dashboard -> Upload Pair -> Select `demo_optical_1.tif` and `demo_sar_1.tif` (already seeded and co-registered). Open in workstation.
**Query**: "Identify flooded regions by comparing the SAR and optical data."
**Expected Plan Output**: 
1. `fusion`
2. `gis_verify`
**Expected Verification**: `true` or `not_applicable`.
**Expected Result**: The `fusion` tool successfully routes to the Late Fusion microservice, providing a combined analysis of both sensory inputs.
