import time
from .config import ASI_API_KEY, ASI_MODEL, BASE_URL_ASI
from .db import conn

def upload_to_web3_storage(file_bytes: bytes, filename: str) -> str:
    ts = int(time.time())
    return f"mockCID-{filename}-{ts}"

