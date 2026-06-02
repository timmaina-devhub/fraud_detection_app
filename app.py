from fastapi import FastAPI

from domain.domain import FraudRequest, FraudResponse
from service.fraud_service import FraudService

fraud_app=FastAPI()

@fraud_app.post("/predict_fraud")
async def predict_fraud(request: FraudRequest)->FraudResponse:
    service = FraudService()
    response = service.predict_fraud(request)
    return response