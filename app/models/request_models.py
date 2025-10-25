from pydantic import BaseModel, HttpUrl, Field

class TextVerificationRequest(BaseModel):
    text: str = Field(..., description="The text content to verify")

class URLVerificationRequest(BaseModel):
    url: HttpUrl = Field(..., description="The webpage URL to verify")
