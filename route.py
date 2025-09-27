

from datetime import datetime
import json
from .db import conn


@router.post("/create_inft")
async def create_inft(name: str = Form(...), owner: str = Form(...), tag: str = Form(...),
                      file: UploadFile = File(...), traits: str = Form("{}")):
    content = await file.read()
    cid = "sfsf"
    #get_from_smart_contract

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