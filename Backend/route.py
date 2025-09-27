# backend/routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from .db import conn
from .utils import upload_to_web3_storage, recompute_score, call_asi_chat
from .embeddings import create_embeddings_and_store, retrieve_relevant_texts

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str | None
    message: str

@router.post("/create_inft")
async def create_inft(name: str = Form(...), owner: str = Form(...), tag: str = Form(...),
                      file: UploadFile = File(...), traits: str = Form("{}")):
    content = await file.read()
    cid = upload_to_web3_storage(content, file.filename)

    cur = conn.cursor()
    cur.execute("INSERT INTO infts (name, owner, tag, cid, traits_json, created_at) VALUES (?,?,?,?,?,?)",
                (name, owner, tag, cid, traits, datetime.utcnow().isoformat()))
    inft_id = cur.lastrowid
    conn.commit()

    text_chunks = []
    try:
        text = content.decode("utf-8")
        for part in text.split("\n\n"):
            if len(part.strip()) > 20:
                text_chunks.append(part.strip())
    except:
        try:
            trait_text = json.loads(traits)
            text_chunks = trait_text if isinstance(trait_text, list) else [str(trait_text)]
        except:
            text_chunks = []

    if text_chunks:
        create_embeddings_and_store(inft_id, text_chunks)

    return {"inft_id": inft_id, "cid": cid}

@router.get("/list_infts")
def list_infts():
    cur = conn.cursor()
    cur.execute("SELECT id, name, owner, tag, cid, traits_json, score, created_at FROM infts ORDER BY id DESC")
    rows = cur.fetchall()
    return [
        {"id": r[0], "name": r[1], "owner": r[2], "tag": r[3], "cid": r[4],
         "traits": json.loads(r[5]) if r[5] else [], "score": r[6], "created_at": r[7]}
        for r in rows
    ]

@router.post("/chat/{inft_id}")
async def chat_with_inft(inft_id: int, req: ChatRequest):
    cur = conn.cursor()
    cur.execute("SELECT name, owner, tag, traits_json FROM infts WHERE id=?", (inft_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="iNFT not found")
    name, owner, tag, traits_json = row
    traits = json.loads(traits_json) if traits_json else []

    retrieved = retrieve_relevant_texts(inft_id, req.message, k=3)
    persona = f"Persona: name={name}, tag={tag}, traits={traits}"
    if retrieved:
        persona += "\nRelevant memory:\n" + "\n---\n".join(retrieved)

    reply = call_asi_chat(system_prompt=persona, user_message=req.message)
    return {"reply": reply}

@router.post("/feedback/{inft_id}")
async def submit_feedback(inft_id: int, rating: float = Form(...), comment: str = Form("")):
    if rating < 0 or rating > 10:
        raise HTTPException(status_code=400, detail="rating must be 0..10")
    cur = conn.cursor()
    cur.execute("INSERT INTO feedbacks (inft_id, rating, comment, created_at) VALUES (?,?,?,?)",
                (inft_id, rating, comment, datetime.utcnow().isoformat()))
    conn.commit()
    new_score = recompute_score(inft_id)
    return {"new_score": new_score}
