import { LoginState, UserInfo } from "@/types";
import { HomeProfile } from "./HomeProfile";

function HomeTopHeader(HomeTopHeaderProps: {
  handleLogoClick: (event: React.SyntheticEvent) => void;
  userProfile: UserInfo;
  setUserProfile: (user: UserInfo) => void;
  setLoginState: (state: LoginState) => void;
  setSearched: (state: boolean) => void;
  setSearchTerm: (term: string) => void;
  setPage: (page: number) => void;
  currTerm: string;
  setCurrTerm: (term: string) => void;
  authToken: string;
}) {
  const handleLogoClick = HomeTopHeaderProps.handleLogoClick;
  const userProfile = HomeTopHeaderProps.userProfile;
  const setUserProfile = HomeTopHeaderProps.setUserProfile;
  const setLoginState = HomeTopHeaderProps.setLoginState;
  const setSearched = HomeTopHeaderProps.setSearched;
  const setSearchTerm = HomeTopHeaderProps.setSearchTerm;
  const setPage = HomeTopHeaderProps.setPage;
  const currTerm = HomeTopHeaderProps.currTerm;
  const setCurrTerm = HomeTopHeaderProps.setCurrTerm;
  const authToken = HomeTopHeaderProps.authToken;

  const handleSearch = (event: React.SyntheticEvent) => {
    event.preventDefault();
    setSearchTerm(currTerm);
    setSearched(true);
    setPage(1);
  };

  const handlePressEnter = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();
      handleSearch(event);
    }
  };

  return (
    <>
      <div className="flex justify-between bg-[rgb(22,22,22)] pb-3 sticky top-0 z-50">
        <h1
          className="font-anton text-4xl mt-7 ml-10 text-white hover:cursor-pointer"
          onClick={handleLogoClick}
        >
          AGORA
        </h1>
        <div className="w-2/3 h-1/2 rounded-sm border-gray-500 mt-7 flex justify-center">
          <input
            className=" w-10/12 text-lg rounded-sm focus:outline-none bg-slate-600 text-white p-2"
            value={currTerm}
            placeholder="Search Agora"
            onChange={(e) => setCurrTerm(e.target.value)}
            onKeyDown={handlePressEnter}
          ></input>
          <img
            src="./search-btn.png"
            className="h-5/6 ml-1 hover:cursor-pointer"
            alt="search"
            onClick={handleSearch}
          ></img>
        </div>
        <HomeProfile
          side="right"
          userProfile={userProfile}
          setUserProfile={setUserProfile}
          setLoginState={setLoginState}
          authToken={authToken}
        />
      </div>
    </>
  );
}

export default HomeTopHeader;
