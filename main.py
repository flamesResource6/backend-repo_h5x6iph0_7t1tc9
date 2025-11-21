import os
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Pond, Measurement

app = FastAPI(title="Aquaculture Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Aquaculture API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# ------------------------- Aquaculture Endpoints -------------------------

class PondOut(Pond):
    id: str

class MeasurementOut(Measurement):
    id: str

@app.post("/api/ponds", response_model=dict)
def create_pond(pond: Pond):
    pond_id = create_document("pond", pond)
    return {"id": pond_id}

@app.get("/api/ponds", response_model=List[PondOut])
def list_ponds():
    docs = get_documents("pond")
    out = []
    for d in docs:
        d["id"] = str(d.pop("_id"))
        out.append(PondOut(**d))
    return out

@app.post("/api/measurements", response_model=dict)
def create_measurement(m: Measurement):
    # ensure timestamp
    data = m.model_dump()
    if not data.get("timestamp"):
        data["timestamp"] = datetime.now(timezone.utc)
    meas_id = create_document("measurement", data)
    return {"id": meas_id}

@app.get("/api/measurements/{pond_id}", response_model=List[MeasurementOut])
def get_measurements(pond_id: str, limit: Optional[int] = 50):
    docs = get_documents("measurement", {"pond_id": pond_id}, limit=limit or 50)
    out = []
    for d in docs:
        d["id"] = str(d.pop("_id"))
        # pydantic will parse timestamp if present
        out.append(MeasurementOut(**d))
    return out

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
