from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .rag_pipeline import get_rationale  # Use relative import if inside a package


app = FastAPI()

# CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/rationale_from_dict")
async def generate_from_uploaded(request: Request):
    customer_data = await request.json()
    explanation = get_rationale(customer_data)
    return {"rationale": explanation}
