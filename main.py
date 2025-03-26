from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from middleware.cors import add_cors_middleware
from routes import auth, fases, perguntas, progress, temas, users
from settings.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Quiz Game API")


add_cors_middleware(app)

templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="templates/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(users.router, prefix="", tags=["users"])
app.include_router(temas.router, prefix="", tags=["temas"])
app.include_router(fases.router, prefix="", tags=["fases"])
app.include_router(perguntas.router, prefix="", tags=["perguntas"])
app.include_router(progress.router, prefix="", tags=["progress"])
