from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password):
    '''
       This function Encrypts a Company's password
    '''
    return pwd_context.encrypt(password)


def verify_encrypted_password(password, hashed):
    '''
       This function compares a Company's password
    '''
    return pwd_context.verify(password, hashed)
