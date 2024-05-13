import { HomeView, PostInfo, UserVotes } from "@/types";
import PostCard from "./PostCard";
import {
  Pagination,
  PaginationContent,
  // PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

function HomeContentView(ContentViewProps: {
  posts: Array<PostInfo>;
  authToken: string;
  userVotes: UserVotes;
  setView: (view: HomeView) => void;
  setCurrentPost: (post: PostInfo) => void;
  page: number;
  setPage: (page: number) => void;
}) {
  const posts = ContentViewProps.posts;
  const authToken = ContentViewProps.authToken;
  const userVotes = ContentViewProps.userVotes;
  const setView = ContentViewProps.setView;
  const setCurrentPost = ContentViewProps.setCurrentPost;
  const page = ContentViewProps.page;
  const setPage = ContentViewProps.setPage;

  return (
    <div className="">
      <div className="flex-row ">
        {posts.map((post) => (
          <PostCard
            post={post}
            authToken={authToken}
            userVotes={userVotes}
            setView={setView}
            setCurrentPost={setCurrentPost}
          />
        ))}
      </div>
      {posts.length !== 0 && (
        <Pagination className="m-3">
          <PaginationContent>
            <PaginationItem
              className="text-white hover:cursor-pointer"
              onClick={() => {
                if (page !== 1) {
                  setPage(page - 1);
                }
              }}
            >
              <PaginationPrevious />
            </PaginationItem>

            {[1, 2, 3].map((num) => (
              <PaginationItem className="text-white">
                {num === page ? (
                  <PaginationLink
                    isActive
                    className="text-black hover:cursor-pointer"
                  >
                    {num}
                  </PaginationLink>
                ) : (
                  <PaginationLink
                    className="hover:cursor-pointer"
                    onClick={() => setPage(num)}
                  >
                    {num}
                  </PaginationLink>
                )}
              </PaginationItem>
            ))}

            <PaginationItem>
              <PaginationNext
                className="text-white hover:cursor-pointer"
                onClick={() => {
                  if (page !== 3) {
                    setPage(page + 1);
                  }
                }}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
}

export default HomeContentView;
