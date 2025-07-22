from config.database import bcrypt


def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(hashed_password, password):
    """Check if a password matches the hashed version"""
    return bcrypt.check_password_hash(hashed_password, password) 