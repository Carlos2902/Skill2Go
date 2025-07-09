import hashlib

def hash_document(document):
    """SHA-256 hash for the uploaded document."""
    hasher = hashlib.sha256()
    for chunk in document.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()
