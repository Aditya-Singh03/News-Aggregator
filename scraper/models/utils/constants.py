import os

DB_HOST = os.getenv("DB_HOST", "localhost") + ":8000"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost") + ":11434"
SCRAPER_HOST = os.getenv("SCRAPER_HOST", "localhost") + ":8050"
RECOMMENDER_HOST = os.getenv("RECOMMENDER_HOST", "localhost") + ":8030"
LLM_HOST = os.getenv("LLM_HOST", "localhost") + ":8040"

LIST_TOPICS = [
    "World News",
    "National News",
    "Business & Finance",
    "Science & Technology",
    "Health & Wellness",
    "Entertainment & Culture",
    "Sports",
    "Travel",
    "Politics",
    "Education",
    "Environment & Sustainability",
    "Arts & Literature",
    "Gaming & Esports",
    "Food & Cooking",
    "Fashion & Beauty",
    "Local News",
    "Personal Finance",
    "Science by Field",
    "Health Conditions",
    "Hobbies & Interests",
    "Social Issues",
]
