from fastapi import FastAPI
from pydantic import BaseModel
from intelligence.query_router import route_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ExamWise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend access
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_examwise(req: QueryRequest):
    answer = route_query(req.query)
    return {"answer": answer}
