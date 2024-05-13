from pydantic import BaseModel, Field


class ScrapeQuery(BaseModel):
    link: str


class ScrapeData(BaseModel):
    content: str
