from fastapi import APIRouter
from app.schemas.predict_schema import PredictRequest
from model.predict import predict_spam

router = APIRouter()

@router.post("/predict")
def predict(request: PredictRequest):
    result = predict_spam(request.text)
    return result