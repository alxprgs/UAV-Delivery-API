import bcrypt

def create_hash(text: str) -> str:
    if len(text) > 1024:
        raise ValueError("Text too long (max 1024 characters)")
    hashed = bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt(rounds=10))
    return hashed.decode('utf-8')

def verify_hash(text: str, stored_hash: str) -> bool:
    if len(text) > 1024:
        raise ValueError("Text too long (max 1024 characters)")
    try:
        return bcrypt.checkpw(text.encode('utf-8'), stored_hash.encode('utf-8'))
    except (ValueError, UnicodeEncodeError, AttributeError):
        return False
