from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.settings import settings
from api import auth
from api import elements, events

app = FastAPI(title="UserBehavior API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(o) for o in settings.cors_origins] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(elements.router, tags=["elements"])  
app.include_router(events.router, tags=["events"])      