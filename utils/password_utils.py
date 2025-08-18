from extensions import bcrypt


def hash_password(password):
    """
    Hash a password using bcrypt for secure storage.

    Uses Flask-Bcrypt to generate a salted hash of the provided password.
    The hash is decoded to UTF-8 string format for database storage.

    Args:
        password (str): Plain text password to hash.

    Returns:
        str: Bcrypt hashed password as UTF-8 string, safe for database storage.
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(hashed_password, password):
    """
    Verify a password against its hashed version.

    Uses bcrypt's secure comparison to check if a plain text password
    matches the stored hash. Resistant to timing attacks.

    Args:
        hashed_password (str): Stored bcrypt hash from database.
        password (str): Plain text password to verify.

    Returns:
        bool: True if password matches hash, False otherwise.
    """
    return bcrypt.check_password_hash(hashed_password, password)