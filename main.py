from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pickle
import io
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications import ResNet50
import uvicorn

app = FastAPI()

model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
embedding_file = "images/object_embeddings.pkl"

with open(embedding_file, "rb") as f:
    data = pickle.load(f)
    known_embeddings = np.array(data["embeddings"])
    known_names = data["names"]

@app.post("/predict/")
async def predict_image_endpoint(uploaded_file: UploadFile = File(...)):
    # Step 1: Load and preprocess the image
    img = Image.open(uploaded_file.file)
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    embedding = model.predict(img_array).flatten()
    distances = np.linalg.norm(known_embeddings - embedding, axis=1)
    closest_index = np.argmin(distances)
    predicted_name = known_names[closest_index]
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = f"Predicted: {predicted_name}"
    draw.text((10, 10), text, font=font, fill="white")
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)
    return StreamingResponse(img_byte_array, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)