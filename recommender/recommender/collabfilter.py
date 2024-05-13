import networkx as nx
from typing import List
import asyncio
import os
from models.utils.funcs import get_data_from_api, add_data_to_api
from models.utils.constants import DB_HOST
from models.user import UserVotes


class CollabFilteringDaemon:
    """A daemon that executes a task every x seconds"""

    def __init__(self, delay: int) -> None:
        self._delay = delay
        self.first_run = True



    async def _execute_task(self) -> None:
        await self._task()

    async def start_daemon(self) -> None:
        while True:
            if self.first_run:
                await asyncio.sleep(120)  # Wait for other services to start
                await self._execute_task()
                self.first_run = False

            await asyncio.sleep(self._delay)
            await self._execute_task()

    # TODO: Aditya
    async def _task(self) -> None:
        all_users = get_data_from_api(DB_HOST, 'user/get-all-users')
        user = get_data_from_api(DB_HOST, 'user/get-user', {"user_id":all_users[0]})
        # print(user)
        all_user_list = [get_data_from_api(DB_HOST, 'user/get-user', {"user_id":all_users[i]}) for i in range(len(all_users))]
        # print(f"all_user_list[0] -------------- {all_user_list[0]}")
        G, user_likes = create_user_graph(all_user_list[:-1])

        #Key: user_id, Value: list of recommended posts
        recommended_posts_for_users = {}
        for user_id in user_likes:
            neighbors = list(G.neighbors(user_id))
            # print("neighbors", neighbors)
            recommended_posts = set()

            total_edge_weight = sum(G[user_id][neighbor]['weight'] for neighbor in neighbors)

            # print("--------------neighbor---------------", len(neighbors))
            for neighbor in neighbors:
                neighbor_likes = user_likes.get(neighbor, set())
                # print("neighbor_likes", neighbor_likes)
                edge_weight = G[user_id][neighbor]['weight']
                score = edge_weight / total_edge_weight if total_edge_weight > 0 else 0
                for post in neighbor_likes:
                    recommended_posts.add((post, score))

            user_posts = set(post for post in user_likes[user_id])
            recommended_posts = {(post, score) for post, score in recommended_posts if post not in user_posts}

            recommended_posts_for_users[user_id] = recommended_posts
            for k, v in recommended_posts_for_users.items():
                
                print("***User***", k)
                print("***Recommendation***", v)

        print("***Done***")
                





def create_user_graph(all_users_list: List[UserVotes]):
    G = nx.Graph()

    likes_map = {}
    user_likes = {}  # This dictionary stores the posts liked by each user

    # print("length of all_users_list------------------------", len(all_users_list))
    for user_votes in all_users_list:
        # print("user_votes------------------------", type(user_votes))
        user = user_votes["votes"]
        user_id = user["user_id"]
        G.add_node(user_id)
        user_likes[user_id] = set(user['list_of_posts_upvotes']) #| set(user['list_of_comments_upvotes'])

        for post_id in user['list_of_posts_upvotes']:
            if post_id not in likes_map:
                likes_map[post_id] = []
            likes_map[post_id].append(user_id)

        # for comment_id in user['list_of_comments_upvotes']:
        #     if comment_id not in likes_map:
        #         likes_map[comment_id] = []
        #     likes_map[comment_id].append(user_id)

    users = list(user_likes.keys())
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            edge_weight = len(user_likes[users[i]] & user_likes[users[j]])
            # print(f"Edge weight between user {users[i]} and user {users[j]}: {edge_weight}")
            G.add_edge(users[i], users[j], weight=edge_weight)

    return G, user_likes
