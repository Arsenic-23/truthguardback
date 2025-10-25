from pydantic import BaseModel

class TextPayload(BaseModel):
    text: str

class URLPayload(BaseModel):
    url: str
