from fastapi.testclient import TestClient
import io
from PIL import Image

def test_health(client: TestClient) -> None:
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metadata(client: TestClient) -> None:
    response = client.get("/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "model_mode" in data

def test_predict_validation_error(client: TestClient) -> None:
    response = client.post("/v1/predict")
    assert response.status_code == 422 # Missing file

def test_predict_synthetic(client: TestClient) -> None:
    # Create dummy image
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    response = client.post(
        "/v1/predict",
        files={"file": ("test.png", buf, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "prediction" in data
    assert "uncertainty" in data
    assert "explanation" in data
    assert data["prediction"]["class_id"] >= 0
    assert data["uncertainty"]["predictive_entropy"] > 0
    assert data["explanation"]["heatmap_base64"] is not None
