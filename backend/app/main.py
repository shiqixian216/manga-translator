from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, projects

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manga Translator")

app.include_router(auth.router)
app.include_router(projects.router)

@app.get("/health")
def health():
    return {"status": "ok"}
