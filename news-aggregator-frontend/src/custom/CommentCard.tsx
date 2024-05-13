import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { Comment, UserVotes } from "@/types";
import { BACKEND_URL } from "@/utils/constants";
import { useEffect, useRef, useState } from "react";
import { UserAvatar } from "./UserAvatar";
import { numberFormatter } from "@/utils/funcs";
import { CustomCardFooter } from "./CustomCardFooter";
import UpDownVotes from "./UpDownVotes";

function CommentCard(CommentCardProp: {
  comment: Comment;
  authToken: string;
  userVotes: UserVotes;
}) {
  const comment = CommentCardProp.comment;
  const authToken = CommentCardProp.authToken;
  const userVotes = CommentCardProp.userVotes;

  const [author, setAuthor] = useState("");
  const [authorAvatar, setAuthorAvatar] = useState();

  const [commentLiked, setCommentLiked] = useState(false);
  const [commentDisliked, setCommentDisliked] = useState(false);

  const [upvotes, setUpvotes] = useState(comment.upvotes);
  const [downvotes, setDownvotes] = useState(comment.downvotes);

  const [gotData, setGotData] = useState(false);

  useEffect(() => {
    fetch(`${BACKEND_URL}/user/get-user?user_id=${comment.author_id}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((json) => json.user)
      .then((user) => {
        setAuthor(user.username);
        setAuthorAvatar(user.avatar);
        if (!gotData) {
          setGotData(true);
        }
      });
  }, [gotData]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/annotator/get-comment?comment_id=${comment.id}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((json) => json.comment)
      .then((updatedComment) => {
        setUpvotes(updatedComment.upvotes);
        setDownvotes(updatedComment.downvotes);
      });
  }, [commentLiked, commentDisliked]);

  useEffect(() => {
    if (userVotes.commentUpvotes.includes(comment.id)) {
      setCommentLiked(true);
    } else if (userVotes.commentDownvotes.includes(comment.id)) {
      setCommentDisliked(true);
    }
  }, [userVotes]);

  return (
    <>
      <Card className="bg-[#161616] m-3 text-white">
        <CardHeader>
          <CardTitle className="flex justify-between">
            <div className="flex gap-2">
              <UserAvatar avatarIndex={authorAvatar} />
              <p className="mt-2  text-xl">{author}</p>
            </div>
            <div className="flex gap-2">
              <p className="text-base">
                {" "}
                {numberFormatter(Math.abs(upvotes - downvotes))}{" "}
              </p>
              <UpDownVotes
                upvotes={upvotes}
                downvotes={downvotes}
                width={3}
                height={3}
              />
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p>{comment.content}</p>
        </CardContent>
        <CustomCardFooter
          id={comment.id}
          authToken={authToken}
          liked={commentLiked}
          disliked={commentDisliked}
          setLiked={setCommentLiked}
          setDisliked={setCommentDisliked}
          isPost={false}
        />
      </Card>
    </>
  );
}

export default CommentCard;
