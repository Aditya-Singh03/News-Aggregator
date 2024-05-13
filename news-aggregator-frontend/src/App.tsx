// import { useState } from "react";
import { useEffect, useState } from "react";
import "./App.css";
import Login from "./Login";
import Preferences from "./Preferences";
import Home from "./Home";
import { BACKEND_URL } from "./utils/constants";
import { LoginState } from "./types";

function App() {
  const [loginState, setLoginState] = useState<LoginState>(
    LoginState.LoggedOut
  );
  const [authToken, setAuthToken] = useState("");
  const [firstTimeUser, setFirstTimeUser] = useState(false);

  useEffect(() => {
    setAuthTokenWrapper(window.localStorage.getItem("authToken") || "");
  }, []);

  const setAuthTokenWrapper = (newToken: string) => {
    setAuthToken(newToken);
    window.localStorage.setItem("authToken", newToken);
    if (newToken !== "") {
      setLoginState(LoginState.Loading);
      fetch(`${BACKEND_URL}/user/view`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${newToken}`,
        },
      })
        .then((res) => (res.status === 200 ? res.json() : Promise.reject()))
        .then((json) => {
          console.log(json);
          setLoginState(LoginState.LoggedIn);
          setFirstTimeUser(json["is_first_time"]);
        })
        .catch(() => {
          setLoginState(LoginState.LoggedOut);
        });
    }
  };
  if (loginState == LoginState.Loading) {
    return (
      <>
        <div className="bg-[#161616] w-screen h-screen"></div>
      </>
    );
  } else if (loginState == LoginState.LoggedOut) {
    return (
      <>
        <Login
          setLoginState={setLoginState}
          setAuthToken={setAuthTokenWrapper}
          setFirstTimeUser={setFirstTimeUser}
        />
      </>
    );
  } else {
    if (firstTimeUser) {
      return (
        <>
          <Preferences
            authToken={authToken}
            setFirstTimeUser={setFirstTimeUser}
          />
        </>
      );
    } else {
      return (
        <>
          <Home authToken={authToken} setLoginState={setLoginState} />
        </>
      );
    }
  }

  // TESTING Preferences
  // return (
  //   <>
  //     <Preferences authToken={authToken} setFirstTimeUser={setFirstTimeUser} />
  //   </>
  // );

  // TESTING Home
  // return (
  //   <>
  //   <Home authToken={authToken}/>
  //   </>
  // );
}

export default App;
