# API Contracts & Conventions

The SatQuery AI API follows strict RESTful conventions and structured formatting.

## Request Conventions
*   **Content-Type:** Standard requests use `application/json`.
*   **File Uploads:** Use `multipart/form-data`.
*   **Validation:** All incoming data is validated strictly using Pydantic schemas before reaching business logic.

## Standardized Error Responses
The API guarantees that all errors (both expected domain errors and unexpected server crashes) are returned in a predictable, structured format.

```json
{
  "error": {
    "code": "INVALID_FILE",
    "message": "The provided file exceeds the maximum allowed size.",
    "details": {}
  }
}
```

### Common Error Codes
*   `INVALID_FILE` (400)
*   `UNSUPPORTED_FORMAT` (415)
*   `MISSING_METADATA` (400)
*   `INCOMPATIBLE_IMAGE_PAIRS` (400)
*   `MODEL_UNAVAILABLE` (503)
*   `GIS_PROCESSING_FAILURE` (500)
*   `INTERNAL_SERVER_ERROR` (500)

*Note: Internal stack traces are scrubbed from production 500 errors.*
