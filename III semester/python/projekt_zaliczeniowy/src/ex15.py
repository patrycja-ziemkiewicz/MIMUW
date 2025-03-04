from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json
import os
from pathlib import Path

app = FastAPI()

DATA_FILE = os.path.join(Path(__file__).resolve().parent.parent, "output", "ex6.json")

class DrugRequest(BaseModel):
    drug_id: str

def load_drug_counts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["drug_id"]: item["pathway_count"] for item in data}

drug_counts = load_drug_counts()

@app.post("/drug")
def get_drug_pathway_count(request: DrugRequest):
    drug_id = request.drug_id
    if drug_id in drug_counts:
        return {"drug_id": drug_id, "pathway_count": drug_counts[drug_id]}
    else:
        raise HTTPException(status_code=404, detail="Drug not found")

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

#http://127.0.0.1:8000/docs
if __name__ == "__main__":
    main()
