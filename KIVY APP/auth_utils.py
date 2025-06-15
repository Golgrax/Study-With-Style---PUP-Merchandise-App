try:
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    import hashlib

    def generate_password_hash(password):
        """Generates a SHA256 hash for a given password."""
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password_hash(stored_hash, password):
        """Checks if a password matches a stored SHA256 hash."""
        return stored_hash == hashlib.sha256(password.encode()).hexdigest()