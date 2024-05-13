import { PostInfo, Comment, UserVotes, HomeView } from "./types";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";

import { PostTitleBar } from "./custom/PostTitleBar";
import { CustomCardFooter } from "./custom/CustomCardFooter";
import { useState, useEffect } from "react";
import { BACKEND_URL } from "./utils/constants";
import CommentCard from "./custom/CommentCard";
import UserCommentBox from "./custom/UserCommentBox";
import SourceCarousel from "./custom/SourceCarousel";
import { dateFormatter } from "./utils/formatter";

function PostView(PostViewProp: {
  post: PostInfo;
  userVotes: UserVotes;
  authToken: string;
  setView: (state: HomeView) => void;
}) {
  const post: PostInfo = PostViewProp.post;
  const authToken = PostViewProp.authToken;
  const userVotes = PostViewProp.userVotes;
  const setView = PostViewProp.setView;

  const [liked, setLiked] = useState(false);
  const [disliked, setDisliked] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    if (userVotes.postUpvotes.includes(post.id)) {
      setLiked(true);
    } else {
      setLiked(false);
    }

    if (userVotes.postDownvotes.includes(post.id)) {
      setDisliked(true);
    } else {
      setDisliked(false);
    }
  }, [userVotes]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/annotator/get-comments?post_id=${post.id}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((json) => setComments(() => [...json.comments]));
  }, [newComment]);

  return (
    <Card className="overflow-y-scroll mt-3 rounded-md bg-[#161616] border-slate-200">
      <CardHeader className="text-white">
      <div className="relative">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-6 h-6 absolute hover:cursor-pointer"
          onClick={() => setView(HomeView.Content)}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18"
          />
        </svg>
        <div className="ml-8">
        <PostTitleBar post={post} liked={liked} disliked={disliked} />
        </div>
        </div>
        {/* <CardDescription>{dateFormatter(post.date)}</CardDescription> */}
      </CardHeader>
      <CardContent className="text-white flex-row">
        <div className="flex justify-center m-2">
          <img src={post.media} alt="" width={"75%"} />
        </div>
        <p className="m-2 mt-3 mb-3">{post.summary}</p>
        <div className="flex justify-center mb-3">
        <h2 className="m-2 text-xl font-semibold">Sources</h2>
        </div>
        <div className="flex justify-center">
          <SourceCarousel sourceIds={post.source_ids} />
        </div>
      </CardContent>

      <CustomCardFooter
        id={post.id}
        authToken={authToken}
        liked={liked}
        disliked={disliked}
        setLiked={setLiked}
        setDisliked={setDisliked}
        isPost={true}
      />
      <UserCommentBox
        authToken={authToken}
        newComment={newComment}
        setNewComment={setNewComment}
        postId={post.id}
      />
      {comments.map((comment) => (
        <CommentCard
          comment={comment}
          authToken={authToken}
          userVotes={userVotes}
        />
      ))}
    </Card>
  );
}

export default PostView;
