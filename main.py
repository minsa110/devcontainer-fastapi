from fastapi import FastAPI, HTTPException
from redis import Redis
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
redis = Redis(host="redis", port=6379)

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

class Todo(BaseModel):
    todo_id: int
    title: str
    description: str

@app.post("/todos/")
async def create_todo(todo: Todo):
    redis.set(todo.todo_id, todo.json())
    return {"message": "Todo created successfully"}

@app.get("/todos/")
async def get_todos():
    todos = []
    for key in redis.keys():
        todos.append(redis.get(key))
    return todos

@app.get("/todos/{todo_id}")
async def get_todo_by_id(todo_id: int):
    todo = redis.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo_by_id(todo_id: int):
    if not redis.get(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis.delete(todo_id)
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)