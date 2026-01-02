from pydantic import BaseModel

class PredictionRequest(BaseModel):
    # Mostly unused if using Multipart Form Data, but kept for structure
    pass
