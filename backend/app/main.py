from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.routers.auth import router as auth_router
from app.models import Role

app = FastAPI(title="Manga Translator")


@app.on_event("startup")
def on_startup():
    # 1) 自动建表（MVP 最省事）
    Base.metadata.create_all(bind=engine)

    # 2) 初始化 roles（user/admin）
    db = SessionLocal()
    try:
        def ensure_role(code: str, name: str):
            r = db.query(Role).filter(Role.code == code).first()
            if not r:
                db.add(Role(code=code, name=name))

        ensure_role("user", "普通用户")
        ensure_role("admin", "管理员")
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
