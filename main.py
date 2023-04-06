from fastapi import FastAPI, HTTPException

app = FastAPI()

todos = []
item_id = 0

@app.get("/todos")
def read_todos():
    return {"todos": todos}

@app.post("/todos")
def add_todo(todo: str):
    global item_id
    todos.append({"id": item_id, "todo": todo})
    item_id += 1
    return {"id": item_id - 1, "todo": todo}

@app.delete("/todos/{item_id}")
def delete_todo_by_id(item_id: int):
    try:
        for todo in todos:
            if todo["id"] == item_id:
                todos.remove(todo)
                return {"id": item_id, "todo": todo["todo"]}
        raise HTTPException(status_code=404, detail="Todo not found")
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
def read_plugin():
    with open("ai-plugin.json", "r") as f:
        return json.load(f)
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
