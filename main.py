from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import redis

redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0, decode_responses=True)

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# Route to list all TODOs
@app.get("/todos")
async def list_todos():
    todos = {}
    for key in redis_client.keys():
        todos[key] = str(redis_client.get(key))+" (id: "+key+"))"
    return todos

# Route to list a specific TODO
@app.get("/todos/{todo_id}")
async def list_todo(todo_id: int):
    todo = redis_client.get(str(todo_id))
    if todo:
        return {"todo_id": todo_id, "todo": todo}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

# Route to add a TODO
@app.post("/todos")
async def add_todo(todo: str):
    # Generate a unique todo_id
    todo_id = redis_client.incr('todo_id')
    redis_client.set(str(todo_id), todo)
    return {"todo_id": todo_id, "todo": todo}

# Route to delete a TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if not redis_client.exists(str(todo_id)):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis_client.delete(str(todo_id))
    return {"result": "Todo deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
