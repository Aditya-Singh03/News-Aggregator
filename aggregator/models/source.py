import uuid
from pydantic import BaseModel, Field


class Source(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    title: str = ""
    link: str = ""
    media: str = ""
    author: str = ""
    date: str = ""

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "sample",
                "link": "sample",
                "media": "sample",
                "author": "sample",
                "date": "sample",
            }
        }
