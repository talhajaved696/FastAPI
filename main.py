from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

posts = [{"id": 1, "title": "Post 1", "content": "Post 1 description"}, {
    "id": 2, "title": "Post 2", "content": "Post 2 description"}]
def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post 
def find_post_id(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i

@app.get("/")
def read_root():
    return {"API_Status": "Running"}

@app.get("/posts")
def get_posts():
    return {"all_posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostModel):
    post = post.dict()
    post["id"] = randrange(0, 100000)
    posts.append(post)
    return {"post": post}

@app.get("/posts/latest")
def get_latest_post():
    post = posts[-1]
    return {"post":post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post": post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_id(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: PostModel):
    post_index = find_post_id(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post = post.dict()
    post["id"] = id
    posts[post_index] = post
    return {"post": post}

