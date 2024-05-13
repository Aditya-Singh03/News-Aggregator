import { CardTitle } from "@/components/ui/card";
import { PostInfo } from "@/types";
import { numberFormatter } from "@/utils/funcs";
import UpDownVotes from "./UpDownVotes";
import { useEffect, useState } from "react";
import { BACKEND_URL } from "@/utils/constants";

export function PostTitleBar(PostCardTitleProp: {
  post: PostInfo;
  liked: boolean;
  disliked: boolean;
}) {
  const post = PostCardTitleProp.post;
  const liked = PostCardTitleProp.liked;
  const disliked = PostCardTitleProp.disliked;
  const [upvotes, setUpvotes] = useState(post.upvotes);
  const [downvotes, setDownvotes] = useState(post.downvotes);

  useEffect(() => {
    fetch(`${BACKEND_URL}/annotator/get-post?post_id=${post.id}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((json) => json.post)
      .then((updatedPost) => {
        setUpvotes(updatedPost.upvotes);
        setDownvotes(updatedPost.downvotes);
      });
  }, [liked, disliked]);

  return (
    <CardTitle className="flex justify-between">
      <h1>{post.title}</h1>
      <div className="flex gap-2">
        {" "}
        {/* <h3 className="text-lg"> */}
        <h3 className="ml-2">
          {numberFormatter(Math.abs(upvotes - downvotes))}
        </h3>
        <UpDownVotes
          upvotes={upvotes}
          downvotes={downvotes}
          width={4}
          height={4}
        />
      </div>
    </CardTitle>
  );
}
