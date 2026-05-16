from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Comment, CommentCreate
from pydantic import ValidationError

app = FastAPI(title="Comments Service")

id_counter = 1
comments_db = []

@app.on_event("startup")
async def startup_event():
    print("Comments Service is running")

@app.on_event("shutdown")
async def shutdown_event():
    print("Comments Service is stopped")

@app.get("/")
async def get_root():
    return {"message": "Comments Service", "service": "comments-svc-s01", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/comments", response_model=List[Comment])
async def get_comments():
    return comments_db

@app.get("/api/comments/{comment_id}", response_model=Comment)
async def get_comment(comment_id: int):
    comment = next((c for c in comments_db if c.id == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.post("/api/comments", response_model=Comment, status_code=201)
async def create_comment(comment: CommentCreate):
    global id_counter
    try:
        new_comment = Comment(id=id_counter, **comment.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validation error")
    
    comments_db.append(new_comment)
    id_counter += 1
    return new_comment