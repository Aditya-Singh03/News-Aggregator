import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { HomeProfileInfo, LoginState } from "@/types";
import { UserAvatar } from "./UserAvatar";
import { useEffect, useState, useRef } from "react";
import AvatarSelection from "./AvatarSelection";
import { BACKEND_URL } from "@/utils/constants";
import ChangeDialog from "./ChangeDialog";

export function HomeProfile(HomeProfileProp: HomeProfileInfo) {
  const side = HomeProfileProp.side;
  const userProfile = HomeProfileProp.userProfile;
  const authToken = HomeProfileProp.authToken;
  const setUserProfile = HomeProfileProp.setUserProfile;
  const setLoginState = HomeProfileProp.setLoginState;

  const [avatarIndex, setAvatarIndex] = useState(userProfile.avatarIndex);
  const [username, setUsername] = useState(userProfile.username);

  const handleLogOut = (event: React.SyntheticEvent) => {
    event.preventDefault();
    window.localStorage.setItem("authToken", "");
    setLoginState(LoginState.LoggedOut);
  };

  useEffect(() => setUsername(userProfile.username), [userProfile]);

  useEffect(() => {
    setUserProfile({
      email: userProfile.email,
      username: userProfile.username,
      avatarIndex: userProfile.avatarIndex,
    });
    fetch(`${BACKEND_URL}/user/update-user`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${authToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ avatar: avatarIndex }),
    });
  }, [avatarIndex]);

  const handleUsernameChange = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && event.shiftKey === false) {
      event.preventDefault();
      fetch(`${BACKEND_URL}/user/update-user`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username }),
      }).then((res) =>
        res.status === 200
          ? setUserProfile({
              email: userProfile.email,
              username: username,
              avatarIndex: userProfile.avatarIndex,
            })
          : setUsername(userProfile.username)
      );
    }
  };

  return (
    <Sheet>
      <SheetTrigger className="text-white font-anton text-4xl mr-10 mt-7">
        <UserAvatar avatarIndex={avatarIndex} />
      </SheetTrigger>
      <SheetContent side={side} className="border-0 bg-[#161616] text-white">
        <SheetHeader>
          <SheetTitle className="text-white flex gap-4">
            <AvatarSelection
              avatarIndex={avatarIndex}
              setAvatarIndex={setAvatarIndex}
            />
            <input
              className="text-xl mt-1 border-0 bg-inherit"
              value={username}
              onKeyDown={handleUsernameChange}
              onChange={(e) => setUsername(e.target.value)}
            ></input>
          </SheetTitle>
        </SheetHeader>
        <SheetDescription className="text-white mt-10">
          <div className="flex justify-between m-2">
            <div className="flex-row">
              <h1 className="text-xl pt-2">Email Address</h1>
              <p className="text-md text-slate-400">{userProfile.email}</p>
            </div>
            <ChangeDialog
              changeName="email"
              subText={userProfile.email}
              authToken={authToken}
              userProfile={userProfile}
              setUserProfile={setUserProfile}
            />
          </div>
          <div className="flex justify-between m-2 mt-10">
            <div className="flex-row">
              <h1 className="text-xl pt-2">Password</h1>
              <p className="text-md text-slate-400">
                Must be 5 characters long
              </p>
            </div>
            <ChangeDialog
              changeName="password"
              subText={"Password must be 5 characters long"}
              authToken={authToken}
              userProfile={userProfile}
              setUserProfile={setUserProfile}
            />
          </div>
        </SheetDescription>
        <button
          title="Sign Out"
          onClick={handleLogOut}
          className="absolute bottom-0 mb-5 border-2 border-red-600 text-red-600 font-semibold rounded-xl right-0 mr-5 p-2 hover:bg-[#222222]"
        >
          Log Out
        </button>
      </SheetContent>
    </Sheet>
  );
}
