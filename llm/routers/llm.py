from fastapi import APIRouter, Body, HTTPException, Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from models.recommendation import RecommendationQuery
from models.utils.funcs import add_data_to_api
from models.llm import (
    PostAnalysis,
    Prompt,
    PostCompletion,
    PostsAnalysisQuery,
    Response,
)
from models.utils.constants import DB_HOST, RECOMMENDER_HOST
from llm.ollama.calls import generate_text_from_ollama, ollama_keep_alive
from tqdm import tqdm


llm_router = APIRouter(prefix="/llm")
PROMPT_PREFIX = "You are a news provider whose job is to write a title and summary for news events. Provide a title and summary for the following event."


@llm_router.post("/prompt")
async def compute_prompt_result(prompt: Prompt = Body(...)):
    prompt_text = prompt.prompt

    if prompt_text == "":
        raise HTTPException(status_code=400, detail="Prompt is empty")

    prompt_result = generate_text_from_ollama(prompt.prompt, prompt.query, Response)
    return {
        "message": "Prompt result generated",
        "result": jsonable_encoder(prompt_result),
    }


@llm_router.post("/add-analysis")
async def generate_analysis(
    _: Request,
    background_tasks: BackgroundTasks,
    post_analysis_query: PostsAnalysisQuery = Body(...),
):
    background_tasks.add_task(compute_analysis, post_analysis_query)
    return {"message": "Analysis in progress"}


def compute_analysis(post_analysis_query: PostsAnalysisQuery):
    ollama_keep_alive(-1)

    for post_query in tqdm(
        post_analysis_query.post_queries, desc="Generating summary and title for text"
    ):

        if post_completion := generate_text_from_ollama(
            prompt=PROMPT_PREFIX, query=post_query.text, response_dt=PostCompletion
        ):
            post_analysis = PostAnalysis(
                post_id=post_query.post_id, completion=post_completion
            )

            add_data_to_api(DB_HOST, "llm/add-analysis", post_analysis)

    ollama_keep_alive(-1)

    list_post_ids = [post_analysis.post_id for post_analysis in post_analysis_query.post_queries]
    recommender_query = RecommendationQuery(post_ids=list_post_ids)
    add_data_to_api(
        RECOMMENDER_HOST, "recommender/add-recommendations", recommender_query
    )
