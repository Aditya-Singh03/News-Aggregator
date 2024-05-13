from typing import List
from recommender.spacy import get_spacy_preprocessor
from models.utils.constants import DB_HOST
from models.post import Post
from models.recommendation import PostRecommendation
import numpy as np
from models.utils.funcs import get_data_from_api, Response
from models.utils.constants import LIST_TOPICS
from tqdm import tqdm
from models.utils.constants import LAPLACE_CONSTANT

NUM_TOPICS_PER_POST = 3


def get_topic_recommendations(list_posts: List[Post]) -> List[PostRecommendation]:
    recommendations = get_topics_for_post(list_posts)
    list_recommendations = []

    for recom_post, post in zip(recommendations, list_posts):
        if post.summary and post.title:
            list_recommendations.append(recom_post)

    return list_recommendations


def get_user_info(user_id: str) -> dict | Response:
    return get_data_from_api(DB_HOST, "user/get-user", {"user_id": user_id})


def calculate_similarity(topic1, topic2):
    nlp = get_spacy_preprocessor().nlp

    topic1_vector = nlp(topic1).vector
    topic2_vector = nlp(topic2).vector

    similarity = (topic1_vector.dot(topic2_vector) + LAPLACE_CONSTANT) / (
        np.linalg.norm(topic1_vector) * np.linalg.norm(topic2_vector) + LAPLACE_CONSTANT * len(topic1_vector)
    )

    return similarity


# TODO - Ji
def get_topics_for_post(posts: List[Post]) -> List[PostRecommendation]:
    posts_recommendations: List[PostRecommendation] = []

    for post in tqdm(posts, desc="Calculating post recommendations"):
        post_similarity_scores = dict()

        for topic in LIST_TOPICS:
            post_similarity_scores[topic] = sum(calculate_similarity(topic, post_topic) for post_topic in post.topics)

        sorted_post_scores = sorted(post_similarity_scores.items(), key=lambda x: x[1])

        post_recommendation = PostRecommendation(
            post_id=post.id,
            topics=[topic for topic, _ in sorted_post_scores[:NUM_TOPICS_PER_POST]],
            date=post.date,
        )
        posts_recommendations.append(post_recommendation)

    return posts_recommendations
