import os
import model

from config import CONFIG
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from glob import glob

import starlette.status as status

app = FastAPI()
VIEWS = {}

app.mount("/public", StaticFiles(directory="public"), name="public")


def load_views():
    views = {}
    for file_path in glob('views/*.html'):
        print(f"[*] View found -> {file_path}")
        view_name = os.path.basename(file_path).split('.')[0]
        with open(file_path, 'r') as f:
            cont = f.read()
            views[view_name] = cont
    return views


@app.on_event("startup")
async def startup_event():
    global VIEWS
    model_name = os.getenv("MODEL", None)
    pipeline_name = os.getenv("PIPELINE", None)

    CONFIG.MODEL_NAME = model_name
    CONFIG.PIPELINE = pipeline_name

    if model_name is not None:
        print(f"[*] MODEL selected: {model_name}")
        model.load_model(model_name=model_name)
    elif pipeline_name is not None:
        model.load_model_from_pipeline(pipeline_name)

    VIEWS = load_views()


@app.get("/")
async def root():
    """Redirect to docs"""
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


class PredictionRequest(BaseModel):
    model: Optional[str] = None
    task: Optional[str] = None
    prompt: str


@app.post("/predict")
async def predict(request: PredictionRequest):
    """Function to predict response from a prompt

    Example body:
    {
        "prompt": "YOUR PROMPT"
    }
    """
    if request.task and not CONFIG.PIPELINE:
        global VIEWS

        CONFIG.PIPELINE = request.task
        model.load_model_from_pipeline(request.task)
        VIEWS = load_views()
    out = model.predict(
        request.prompt, pipelane_name=request.task, model_name=request.model)
    return out



@app.get("/config")
def get_config():
    return {"MODEL_NAME":CONFIG.MODEL_NAME,"PIPELINE":CONFIG.PIPELINE}

class ConfigRequest(BaseModel):
    model: Optional[str] = None
    pipeline: Optional[str] = None

@app.post("/config")
def post_config( request: ConfigRequest):
    if request.model is not None:
        CONFIG.MODEL_NAME = request.model
    
    if request.pipeline is not None:
        CONFIG.PIPELINE = request.pipeline

@app.get("/ui", response_class=HTMLResponse)
def get_ui():
    """Redirect to /ui/chat"""
    return RedirectResponse(url="/ui/chat", status_code=status.HTTP_302_FOUND)


@app.get("/ui/{view}", response_class=HTMLResponse)
def get_ui(view):
    """Load any view with /ui/:view:"""
    return HTMLResponse(content=VIEWS[view])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
