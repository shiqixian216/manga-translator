from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.auth import get_db, get_current_user, get_user_roles
from app.models import User, Role, UserRole
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(data.password))
    db.add(user)
    db.flush()  # 拿到 user.id

    # 默认分配 role=user
    role_user = db.query(Role).filter(Role.code == "user").first()
    if not role_user:
        raise HTTPException(status_code=500, detail="Role 'user' not initialized")

    db.add(UserRole(user_id=user.id, role_id=role_user.id))
    db.commit()
    return {"ok": True, "user_id": user.id}


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    email = data.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")

    roles = get_user_roles(db, user.id)
    token = create_access_token(sub=str(user.id))
    return TokenOut(
        access_token=token,
        user=UserOut(id=user.id, email=user.email, roles=roles),
    )


@router.get("/me", response_model=UserOut)
def me(user_and_roles=Depends(get_current_user)):
    user, roles = user_and_roles
    return UserOut(id=user.id, email=user.email, roles=roles)
