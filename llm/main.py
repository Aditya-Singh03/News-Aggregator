from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from llm.ollama.calls import add_model_to_ollama
from routers.llm import llm_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    add_model_to_ollama()
    yield


origins = ["*"]
app = FastAPI(title="News Annotator LLM", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router)


@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8040, reload=True, workers=1)
