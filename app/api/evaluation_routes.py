from fastapi import APIRouter, Depends
from app.schemas.evaluation_schema import EvaluationRequest, EvaluationResponse, EvaluationBatchResponse
from app.services.evaluation_service import EvaluationService
from app.dependencies import get_evaluation_service

router = APIRouter()


@router.post("/run", response_model=EvaluationResponse)
async def evaluate_single(
    request: EvaluationRequest,
    service: EvaluationService = Depends(get_evaluation_service),
):
    result = await service.evaluate_single(request)
    return result


@router.post("/batch", response_model=EvaluationBatchResponse)
async def evaluate_batch(
    requests: list[EvaluationRequest],
    service: EvaluationService = Depends(get_evaluation_service),
):
    results = await service.evaluate_batch(requests)
    return EvaluationBatchResponse(results=results, total=len(results))


@router.get("/report")
async def get_evaluation_report(service: EvaluationService = Depends(get_evaluation_service)):
    report = await service.generate_report()
    return report
