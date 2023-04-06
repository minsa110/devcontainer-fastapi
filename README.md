# devcontainer-fastapi

1. Create the plugin code using Copilot chat:
```markdown
Write a simple TODO app using FastAPI, that lets the user add TODOs, list their TODOs, and delete TODOs, ensuring that the app stores item_id for each todo item.
 
Include a __main__ section which will run this app using uvicorn. The Python module where I save this code will be called main.py.
 
In addition to the normal endpoints, include a route .wellknown/ai-plugin.json which serves (as JSON) the contents of ./ai-plugin.json, located in the same directory as main.py. Exclude this route from the OpenAPI spec, and don't serve any other static content.
```

2. Create `main.py` and copy the generated code

2. Create `ai-plugin.json` (use snippet via `manifest-openai` -- or let Copilot generate it)

3. Run the app (in terminal run: `uvicorn main:app` or press `F5`) and test the CRUD operations at .../docs

4. Further customize **Run and Debug** by editing `launch.json` in the `.vscode` folder