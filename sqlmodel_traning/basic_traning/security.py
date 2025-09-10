from passlib.context import CryptContext


# What should you configure for production?
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
    

def verify_password(hashed_pass: str, password: str) -> bool:
    return pwd_context.verify(password, hashed_pass)
