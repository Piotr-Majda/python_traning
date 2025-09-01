from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .lru import LruDocument


class UserSettings(BaseModel):
    capacity: int = Field(ge=1)


class CacheDocument(BaseModel):
    doc_id: str
    content: str


app = FastAPI()

lru_document = LruDocument()


@app.get('/users/{user_id}/cache/{doc_id}')
async def get_document(user_id: str, doc_id: str):
    doc = lru_document.get_doc(user_id, doc_id)
    if not doc:
        raise HTTPException(404, 'document not found')
    return doc


@app.get('/users/{user_id}/cache')
async def get_documents(user_id: str):
    documents = lru_document.get_docs(user_id)
    return {'size': lru_document.get_size(user_id), 'items': documents}


@app.post('/users/{user_id}/cache', status_code=201)
async def cache_document(user_id: str, document: CacheDocument):
    lru_document.cache(user=user_id, doc_id=document.doc_id, content=document.content)


@app.put('/users/{user_id}/settings')
async def set_capacity(user_id: str, settings: UserSettings):
    lru_document.set_capacity(user=user_id, capacity=settings.capacity)
    return {'size': lru_document.get_size(user_id)}
