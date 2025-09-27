import time, requests
from fastapi import HTTPException
from .config import ASI_API_KEY, ASI_MODEL, BASE_URL_ASI
from .db import conn

def upload_to_web3_storage(file_bytes: bytes, filename: str) -> str:
    ts = int(time.time())
    return f"mockCID-{filename}-{ts}"

def call_asi_chat(system_prompt: str, user_message: str, history: list = None) -> str:
    if not ASI_API_KEY:
        return f"[MOCK REPLY] {user_message}"
    headers = {"Authorization": f"Bearer {ASI_API_KEY}", "Content-Type": "application/json"}
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    payload = {"model": ASI_MODEL, "messages": messages, "max_tokens": 512}
    r = requests.post(BASE_URL_ASI, headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail=f"ASI API error {r.status_code}: {r.text}")
    return r.json()["choices"][0]["message"]["content"]