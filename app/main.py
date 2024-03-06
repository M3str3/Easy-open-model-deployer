import os
import model

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import FastAPI

from dotenv import load_dotenv
from glob import glob

import starlette.status as status

load_dotenv()
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
            views[view_name] = cont.replace("%MODEL%", model.MODEL_NAME).replace(
                "%PIPELANE%", model.PIPELANE)
    return views


@app.on_event("startup")
async def startup_event():
    global VIEWS
    model_name = os.getenv("MODEL", None)
    pipelane_name = os.getenv("PIPELANE", None)

    if pipelane_name is None and model_name is None:
        print("No MODEL or PIPELANE especified")
        exit(1)

    model.MODEL_NAME = model_name
    model.PIPELANE = pipelane_name

    if model_name is not None:
        print(f"[*] MODEL selected: {model_name}")
        model.load_model(model_name=model_name)
    elif pipelane_name is not None:
        model.load_model_from_pipelane(pipelane_name)

    VIEWS = load_views()


@app.get("/")
async def root():
    """Redirect to docs"""
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


class PredictionRequest(BaseModel):
    prompt: str


@app.post("/predict/")
async def predict(request: PredictionRequest):
    """Function to predict response from a prompt

    Example body:
    {
        "prompt": "YOUR PROMPT"
    }
    """
    out = model.predict(request.prompt)
    if 'error' in out:
        return out
    return {"prediction": out}


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
    uvicorn.run(app=app, host="0.0.0.0", port=8888)
