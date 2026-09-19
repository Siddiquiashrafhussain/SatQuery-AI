from app.schemas.geonli import GeoNLIRequest, GeoNLIResult

class GeoNLIChatService:
    async def analyze(self, request: GeoNLIRequest) -> GeoNLIResult:
        # Development mock implementation for GeoNLI
        # In a real implementation, this would route to GeoChat-7B or another VLM
        return GeoNLIResult(
            entailment_class="neutral",
            reasoning="This is a mocked GeoNLI response based on the development mock pattern.",
            premise=request.premise,
            hypothesis=request.hypothesis,
            image_id=request.image_id,
            provider="development",
            model_name="mock-geonli"
        )

geonli_chat_service = GeoNLIChatService()
