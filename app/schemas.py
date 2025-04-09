from pydantic import BaseModel, AnyHttpUrl

class URLRequest(BaseModel):
    original_url: AnyHttpUrl

class URLResponse(BaseModel):
    short_url: str
