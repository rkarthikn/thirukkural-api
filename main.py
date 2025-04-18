from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import random

app = FastAPI()

# Load merged Kural data (with section/chapter info)
with open("merged_kural.json", "r", encoding="utf-8") as f:
    kural_data = json.load(f)

# Build quick lookup by Number
kural_dict = {item["Number"]: item for item in kural_data}

@app.get("/")
def read_root():
    return {"message": "Welcome to the full Thirukkural API!"}

# 👇 Move this route ABOVE the dynamic one
@app.get("/kural/random")
def get_random_kural():
    kural = random.choice(kural_data)
    return JSONResponse(content=kural, media_type="application/json; charset=utf-8")

@app.get("/kural/{number}")
def get_kural(number: int):
    kural = kural_dict.get(number)
    if not kural:
        raise HTTPException(status_code=404, detail="Kural not found")
    return JSONResponse(content=kural, media_type="application/json; charset=utf-8")
