from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from reviewer import review_content

# ✅ Create app FIRST
app = FastAPI()

# ✅ Then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    content: str
    review_type: str = "general"

@app.post("/review")
def review(req: ReviewRequest):
    result = review_content(req.content, req.review_type)
    return {"review": result}