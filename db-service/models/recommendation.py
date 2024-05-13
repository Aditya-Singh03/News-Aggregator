from typing import List
import uuid
from pydantic import BaseModel, Field


class RecommendationQuery(BaseModel):
    post_ids: List[str]


class PostRecommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    post_id: str
    topics: List[str]
    date: str
