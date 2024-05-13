from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from utils import get_mongo_client, change_db_id_to_str
from models.post import Post, Comment
from models.llm import PostAnalysis
from routers.user import auth_manager, user_client

annotator_router = APIRouter(prefix="/annotator")
annotator_client = get_mongo_client()["annotator"]


@annotator_router.post("/add-post")
def add_post(post: Post = Body(...)):
    post_data = jsonable_encoder(post)
    res_post = annotator_client["posts"].insert_one(post_data)
    return {
        "message": "Added text post",
        "post_id": str(res_post.inserted_id),
    }


@annotator_router.get("/get-post")
def get_one_post(post_id: str):
    if (post := get_post(post_id)) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "message": "Retrieved post",
        "post": jsonable_encoder(post),
    }


@annotator_router.get("/get-all-posts")
async def get_posts(limit: int = 5, query: str = "", page: int = 1):
    if not query:
        return {
            "message": "Retrieved posts",
            "list_posts": get_all_posts(limit, page - 1),
        }
    else:
        return {
            "message": "Retrieved posts by query",
            "list_posts": get_posts_by_query(query, limit, page - 1),
        }


def vote_post_or_comment(
    uid: str,
    is_upvote: bool,
    is_comment: bool,
    user=Depends(auth_manager),
):
    identifier = "Comment" if is_comment else "Post"
    if (is_comment and get_comment(uid) is None) or (
        not is_comment and get_post(uid) is None
    ):
        raise HTTPException(status_code=404, detail=f"{identifier} not found")

    collection_name = "comments" if is_comment else "posts"

    to_vote = "upvotes" if is_upvote else "downvotes"
    to_vote_against = "downvotes" if is_upvote else "upvotes"

    user_votes = user_client["votes"].find_one({"user_id": user["id"]})

    # Checks if user has already upvoted
    if uid in user_votes[f"list_of_{collection_name}_{to_vote}"]:
        raise HTTPException(status_code=400, detail=f"{identifier} already {to_vote}")

    # Checks if user has downvoted the post
    if uid in user_votes[f"list_of_{collection_name}_{to_vote_against}"]:
        change_attribute_count(collection_name, uid, to_vote_against, False)
        remove_from_attribute_list(
            user_votes, f"list_of_{collection_name}_{to_vote_against}", uid
        )

    change_attribute_count(collection_name, uid, to_vote, True)
    add_to_attribute_list(user["id"], f"list_of_{collection_name}_{to_vote}", uid)

    return {"message": f"{identifier} {to_vote}"}


def remove_vote_post_or_comment(
    uid: str,
    is_upvote: bool,
    is_comment: bool,
    user=Depends(auth_manager),
):
    identifier = "Comment" if is_comment else "Post"
    if (is_comment and get_comment(uid) is None) or (
        not is_comment and get_post(uid) is None
    ):
        raise HTTPException(status_code=404, detail=f"{identifier} not found")

    collection_name = "comments" if is_comment else "posts"
    to_vote = "upvotes" if is_upvote else "downvotes"

    user_votes = user_client["votes"].find_one({"user_id": user["id"]})

    # Checks if user has not voted the post
    if uid not in user_votes[f"list_of_{collection_name}_{to_vote}"]:
        raise HTTPException(status_code=400, detail=f"{collection_name} not {to_vote}")

    change_attribute_count(collection_name, uid, to_vote, False)
    remove_from_attribute_list(user_votes, f"list_of_{collection_name}_{to_vote}", uid)

    return {"message": f"{identifier} {to_vote} removed"}


@annotator_router.put("/upvote-post")
async def upvote_post(post_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=post_id, is_upvote=True, is_comment=False, user=user
    )


@annotator_router.put("/upvote-comment")
async def upvote_comment(comment_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=comment_id, is_upvote=True, is_comment=True, user=user
    )


@annotator_router.put("/downvote-post")
async def downvote_post(post_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=post_id, is_upvote=False, is_comment=False, user=user
    )


@annotator_router.put("/downvote-comment")
async def downvote_comment(comment_id: str, user=Depends(auth_manager)):
    return vote_post_or_comment(
        uid=comment_id, is_upvote=False, is_comment=True, user=user
    )


@annotator_router.put("/remove-upvote-comment")
async def remove_upvote_comment(comment_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=comment_id, is_upvote=True, is_comment=True, user=user
    )


@annotator_router.put("/remove-downvote-comment")
async def remove_downvote_comment(comment_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=comment_id, is_upvote=False, is_comment=True, user=user
    )


@annotator_router.put("/remove-upvote-post")
async def remove_upvote_post(post_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=post_id, is_upvote=True, is_comment=False, user=user
    )


@annotator_router.put("/remove-downvote-post")
async def remove_downvote_post(post_id: str, user=Depends(auth_manager)):
    return remove_vote_post_or_comment(
        uid=post_id, is_upvote=False, is_comment=False, user=user
    )


@annotator_router.post("/comment")
async def comment_post(comment: Comment = Body(...), user=Depends(auth_manager)):
    if get_post(comment.post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    comment_data = jsonable_encoder(comment)
    comment_data["author_id"] = user["id"]

    annotator_client["comments"].insert_one(comment_data)
    return {"message": "Comment added", "comment_id": str(comment_data["_id"])}


@annotator_router.get("/get-comments")
async def get_comments(post_id: str):
    return {
        "message": "Retrieved comments",
        "comments": get_comments_by_post_id(post_id),
    }


@annotator_router.get("/get-comment")
async def get_comment(comment_id: str):
    return {
        "message": "Retrieved comment",
        "comment": get_comment_by_id(comment_id),
    }


def remove_from_attribute_list(dt_vals: dict, attribute: str, post_id: str):
    dt_vals[attribute].remove(post_id)
    user_client["votes"].update_one(
        {"_id": dt_vals["_id"]}, {"$set": {attribute: dt_vals[attribute]}}, upsert=False
    )


def add_to_attribute_list(user_id: str, attribute: str, uid: str):
    user_client["votes"].update_one(
        {"user_id": user_id}, {"$push": {attribute: uid}}, upsert=False
    )


def change_attribute_count(
    collection_name: str, uid: str, attribute: str, increment: bool
):
    annotator_client[collection_name].update_one(
        {"_id": uid}, {"$inc": {attribute: 1 if increment else -1}}, upsert=False
    )


def get_comment(comment_id: str):
    comment = annotator_client["comments"].find_one({"_id": comment_id})
    comment = change_db_id_to_str(comment)
    return comment


def get_comments_by_post_id(post_id: str):
    comments = list(annotator_client["comments"].find({"post_id": post_id}))
    return list(map(change_db_id_to_str, comments))


def get_comment_by_id(comment_id: str):
    comment = annotator_client["comments"].find_one({"_id": comment_id})
    return change_db_id_to_str(comment)


def add_fields_to_post(post: dict):
    if post_analysis_json := get_llm_result_by_post_id("analyses", post["_id"]):
        post_analysis = PostAnalysis(**post_analysis_json)

        post["summary"] = post_analysis.completion.summary
        post["title"] = post_analysis.completion.title

    return post


def get_llm_result_by_post_id(result_collection: str, post_id: str):
    llm_client = get_mongo_client()["llm"]
    return llm_client[result_collection].find_one({"post_id": post_id})


def get_post(post_id: str):
    if post := annotator_client["posts"].find_one({"_id": post_id}):
        return change_db_id_to_str(add_fields_to_post(post))
    return None


def get_all_posts(limit: int, skip: int):
    list_posts = list(
        map(
            add_fields_to_post, annotator_client["posts"].find().skip(skip).limit(limit)
        )
    )
    return list(map(change_db_id_to_str, list_posts))


def get_posts_by_query(query: str, limit: int, skip: int):
    llm_analyses = get_mongo_client()["llm"]["analyses"]
    llm_agg = llm_analyses.aggregate(
        [
            {
                "$search": {
                    "index": "llm-post-query",
                    "text": {"query": query, "path": {"wildcard": "*"}},
                }
            },
            {"$skip": skip},
            {"$limit": limit},
            {"$project": {"_id": 0, "post_id": 1}},
        ]
    )
    return [get_post(post["post_id"]) for post in list(llm_agg)]
