from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash_psw(psw):
    return pwd_context.hash(psw)

def verify_psw(pain_psw, hashed_psw):
    return pwd_context.verify(pain_psw, hashed_psw)