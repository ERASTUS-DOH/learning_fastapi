from passlib.context import CryptContext


def hash_pwd(password: str)-> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
    return pwd_context.hash(password)