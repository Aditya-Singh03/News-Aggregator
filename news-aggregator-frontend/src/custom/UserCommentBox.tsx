import { Button } from "@/components/ui/button";
import { BACKEND_URL } from "@/utils/constants";

function UserCommentBox(UserCommentBoxProps: {
  authToken: string;
  newComment: string;
  setNewComment: (newVal: string) => void;
  postId: string;
}) {
  const authToken = UserCommentBoxProps.authToken;
  const newComment = UserCommentBoxProps.newComment;
  const setNewComment = UserCommentBoxProps.setNewComment;
  const postId = UserCommentBoxProps.postId;

  const handlePostComment = (event: React.SyntheticEvent) => {
    event.preventDefault();
    // fetch req ur comment here
    fetch(`${BACKEND_URL}/annotator/comment`, {
      method: "POST",
      body: JSON.stringify({ content: newComment, post_id: postId }),
      headers: {
        Authorization: `Bearer ${authToken}`,
        "Content-Type": "application/json",
      },
    }).then((res) => {
      if (res.status === 200) {
        setNewComment("");
      }
    });
  };

  const handlePressEnter = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();
      handlePostComment(event);
    }
  };

  return (
    <>
      <div className="w-1/1 h-[160px]bg-[#161616] focus-within:bg-[#1d1c1c] rounded-md m-3 border border-slate-300">
        <textarea
          className="w-full p-3 h-[110px] bg-inherit text-white rounded-md focus:!outline-none"
          placeholder="Enter new comment"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          onKeyDown={handlePressEnter}
        ></textarea>
        <div className="flex justify-between">
          <div></div>
          <Button
            className="p-3 m-[0.4rem] h-[20px] rounded-md"
            variant="outline"
            onClick={handlePostComment}
          >
            Post
          </Button>
        </div>
      </div>
    </>
  );
}

export default UserCommentBox;
