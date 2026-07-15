from fastapi import FastAPI

from domain.domain import (
    FraudRequest,
    FraudResponse,
    BatchFraudRequest,
    BatchFraudResponse
)

from service.fraud_service import FraudService

fraud_app=FastAPI()



service = FraudService()


# ------------------------------------
# Predict one customer
# ------------------------------------
@fraud_app.post(
    "/predict_fraud",
    response_model=FraudResponse
)
async def predict_fraud(request: FraudRequest):

    return service.predict_fraud(request)


# ------------------------------------
# Predict multiple customers
# ------------------------------------
@fraud_app.post(
    "/predict_fraud_batch",
    response_model=BatchFraudResponse
)
async def predict_fraud_batch(
    request: BatchFraudRequest
):

    predictions = service.predict_fraud_batch(
        request.customers
    )

    return BatchFraudResponse(
        predictions=predictions
    )