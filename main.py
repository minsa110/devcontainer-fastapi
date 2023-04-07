import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import os
import redis

redis_client = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)

# Get the value of PLUGIN_HOSTNAME from the environment variable, or use the default value
plugin_hostname = os.environ.get('PLUGIN_HOSTNAME', 'https://your-app-url.com')

app = FastAPI()

# Create a sub-application, in order to access just the query endpoints in the OpenAPI schema, found at http://0.0.0.0:8000/sub/openapi.json when the app is running locally
sub_app = FastAPI(
    title="Todo app",
    description="A todo app for managing your tasks",
    version="1.0.0",
    servers=[{"url": plugin_hostname}],
)
app.mount("/sub", sub_app)

def load_manifest():
    with open("./ai-plugin.json", "r") as f:
        return json.load(f)

# Route to serve ai-plugin.json
@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def ai_plugin():
    manifest = load_manifest()
    return JSONResponse(content=manifest)

# Route to list all TODOs
@app.get("/todos")
async def list_todos():
    todo_datastore = {}
    for key in redis_client.keys():
        todo_datastore[key] = redis_client.get(key).decode('utf-8')
    return todo_datastore

# Route to list a specific TODO
@app.get("/todos/{todo_id}")
async def list_todo(todo_id: int):
    todo = redis_client.get(todo_id)
    if todo:
        return {"todo_id": todo_id, "todo": todo.decode('utf-8')}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

# Route to add a TODO
@app.post("/todos")
async def add_todo(todo: str):
    # Generate a unique todo_id
    todo_id = redis_client.incr('todo_id')
    redis_client.set(todo_id, todo)
    return {"todo_id": todo_id, "todo": todo}

# Route to delete a TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if not redis_client.exists(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    redis_client.delete(todo_id)
    return {"result": "Todo deleted"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="TODO App",
        version="1.0.0",
        description="A simple TODO app with FastAPI",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
