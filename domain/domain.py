from pydantic import BaseModel
from typing import List

class FraudRequest(BaseModel):
    amount_usd: float
    transaction_dy: int
    transaction_hr: int
    transaction_min: int
    transaction_sec: int
    device_type: str

class FraudResponse(BaseModel):
    is_fraud: int


class BatchFraudRequest(BaseModel):
    customers: List[FraudRequest]


class BatchFraudResponse(BaseModel):
    predictions: List[FraudResponse]