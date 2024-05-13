import { useState, useEffect } from "react";
import { HomeInfo, PostInfo, HomeView, UserInfo, UserVotes } from "./types";
import { BACKEND_URL } from "./utils/constants";
import PostView from "./PostView";
import HomeContentView from "./custom/HomeContentView";
import HomeTopHeader from "./custom/HomeTopHeader";

function Home(HomeProps: HomeInfo) {
  const authToken = HomeProps.authToken;
  const setLoginState = HomeProps.setLoginState;

  const [posts, setPosts] = useState<PostInfo[]>([]);
  const [view, setView] = useState<HomeView>(
    parseInt(window.sessionStorage.getItem("HomeView") || "0")
  );
  const [page, setPage] = useState<number>(
    parseInt(window.sessionStorage.getItem("page") || "1")
  );
  const [currentPost, setCurrentPost] = useState<PostInfo>(
    JSON.parse(window.sessionStorage.getItem("currentPost") || "{}")
  );
  const [userProfile, setUserProfile] = useState<UserInfo>({
    username: "Loading",
    email: "Loading",
    avatarIndex: 0,
  });

  const [userVotes, setUserVotes] = useState<UserVotes>({
    postUpvotes: [],
    postDownvotes: [],
    commentUpvotes: [],
    commentDownvotes: [],
  });

  const [searched, setSearched] = useState(false);

  const [searchTerm, setSearchTerm] = useState("");

  const [currTerm, setCurrTerm] = useState("");

  const setViewWrapper = (newView: HomeView) => {
    window.sessionStorage.setItem("HomeView", JSON.stringify(newView));
    setView(newView);
  };

  const setCurrentPostWrapper = (newPost: PostInfo) => {
    window.sessionStorage.setItem("currentPost", JSON.stringify(newPost));
    setCurrentPost(newPost);
  };

  const setPageWrapper = (newPage: number) => {
    window.sessionStorage.setItem("page", JSON.stringify(newPage));
    setPage(newPage);
  };

  useEffect(() => {
    setPosts([]);
    fetch(
      `${BACKEND_URL}/recommender/get-recommendations?page=${page}&query=${searchTerm}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    )
      .then((res) => res.json())
      .then((json) => {
        setPosts(json["list_recommendations"]);
      });
  }, [page, searched]);

  useEffect(() => {
    fetch(`${BACKEND_URL}/user/view`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })
      .then((res) => res.json())
      .then((json) => {
        const user = json.user;
        setUserProfile({
          email: user.email_address,
          username: user.username,
          avatarIndex: user.avatar,
        });

        const userVotes = json.votes;
        setUserVotes({
          postUpvotes: userVotes.list_of_posts_upvotes,
          postDownvotes: userVotes.list_of_posts_downvotes,
          commentUpvotes: userVotes.list_of_comments_upvotes,
          commentDownvotes: userVotes.list_of_comments_downvotes,
        });
      });
  }, [view]);

  const handleLogoClick = (event: React.SyntheticEvent) => {
    event.preventDefault();
    setPage(1);
    setSearchTerm("");
    setCurrTerm("");
    setSearched(false);
    setViewWrapper(HomeView.Content);
  };

  return (
    <>
      <div className="grid grid-rows-home h-screen max-h-screen overflow-y-scroll">
        <HomeTopHeader
          handleLogoClick={handleLogoClick}
          userProfile={userProfile}
          setUserProfile={setUserProfile}
          setLoginState={setLoginState}
          setSearched={setSearched}
          setSearchTerm={setSearchTerm}
          setPage={setPage}
          currTerm={currTerm}
          setCurrTerm={setCurrTerm}
          authToken={authToken}
        />
        <div className="bg-gradient-to-b from-[#161616] to-slate-900 grid grid-cols-home ">
          <div className=""></div>
          {view == HomeView.Content ? (
            <HomeContentView
              posts={posts}
              authToken={authToken}
              userVotes={userVotes}
              setView={setViewWrapper}
              setCurrentPost={setCurrentPostWrapper}
              page={page}
              setPage={setPageWrapper}
            />
          ) : posts.length === 0 ? (
            <></>
          ) : (
            <PostView
              post={currentPost}
              authToken={authToken}
              userVotes={userVotes}
              setView={setViewWrapper}
            />
          )}
        </div>
      </div>
    </>
  );
}

export default Home;
