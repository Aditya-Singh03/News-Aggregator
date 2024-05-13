import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { HomeView, PostInfo, UserVotes } from "@/types";
import { useEffect, useState } from "react";
import { PostTitleBar } from "./PostTitleBar";
import { CustomCardFooter } from "./CustomCardFooter";
import { minimizeSummary } from "@/utils/formatter";

function PostCard(PostProp: {
  post: PostInfo;
  userVotes: UserVotes;
  authToken: string;
  setView: (state: HomeView) => void;
  setCurrentPost: (post: PostInfo) => void;
}) {
  const post = PostProp.post;
  const authToken = PostProp.authToken;
  const setCurrentPost = PostProp.setCurrentPost;
  const setView = PostProp.setView;
  const userVotes = PostProp.userVotes;

  const [liked, setLiked] = useState(false);
  const [disliked, setDisliked] = useState(false);

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

  const handlePostClick = (event: React.SyntheticEvent) => {
    event.preventDefault();
    setCurrentPost(post);
    setView(HomeView.Post);
  };

  return (
    <Card className="m-2 text-white bg-[#161616] hover:cursor-pointer">
      <div onClick={handlePostClick}>
        <CardHeader>
          <PostTitleBar post={post} liked={liked} disliked={disliked} />
          <CardDescription className="gap-4">
            {/* <p>{post.summary}</p> <p>{post.date}</p> */}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex-row ">
          <div className="flex justify-center">
            <img src={post.media} alt="" width={"50%"} />
          </div>
          <p className="mt-2 mb-2 text-slate-400 height-[100px] overflow-clip mr-6">
            {minimizeSummary(post.summary)}
          </p>
        </CardContent>
      </div>
      <CustomCardFooter
        id={post.id}
        authToken={authToken}
        liked={liked}
        disliked={disliked}
        setLiked={setLiked}
        setDisliked={setDisliked}
        isPost={true}
      />
    </Card>
  );
}

export default PostCard;
