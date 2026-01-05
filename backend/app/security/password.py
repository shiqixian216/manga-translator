from passlib.context import CryptContext

# 用 pbkdf2_sha256：稳定、纯 Python、不会踩 bcrypt 兼容坑
_pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    # 可选：防止超长输入导致性能问题（不是必须）
    if len(password) > 1024:
        raise ValueError("password too long")
    return _pwd.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _pwd.verify(password, password_hash)
