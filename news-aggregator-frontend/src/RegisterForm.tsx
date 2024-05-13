import { useState } from "react";
import AvatarSelection from "./custom/AvatarSelection.tsx";
import { LoginState, RegisterFormInfo } from "./types";
import { BACKEND_URL } from "./utils/constants.ts";

function RegisterForm(registerProps: RegisterFormInfo) {
  const toggleRegister = registerProps.toggleRegister;
  const setToggleRegister = registerProps.setToggleRegister;
  const email = registerProps.email;
  const setEmail = registerProps.setEmail;
  const password = registerProps.password;
  const setPassword = registerProps.setPassword;
  const setAuthToken = registerProps.setAuthToken;
  const setLoginState = registerProps.setLoginState;
  const setFirstTimeUser = registerProps.setFirstTimeUser;
  const setRegisterFail = registerProps.setRegisterFail;

  const [avatarIndex, setAvatarIndex] = useState(0);
  const [username, setUsername] = useState("");
  const [confirmPass, setConfirmPass] = useState("");

  const handleRegister = (event: React.SyntheticEvent) => {
    event.preventDefault();
    // send fetch POST to backend to register user
    if (password !== confirmPass) {
      setRegisterFail(true);
    } else {
      fetch(`${BACKEND_URL}/user/register`, {
        method: "POST",
        body: JSON.stringify({
          email_address: email,
          password: password,
          username: username,
          avatar: avatarIndex,
        }),
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => (res.status === 200 ? res.json() : Promise.reject()))
        .then((json) => {
          setAuthToken(json.token);
          setLoginState(LoginState.LoggedIn);
          setFirstTimeUser(true);
        })
        .catch(() => setRegisterFail(true));
    }
  };

  if (toggleRegister) {
    return (
      <>
        <form action="" className="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
          <div className="pb-2 pt-4 flex gap-2 ">
            <input
              type="username"
              name="username"
              id="username"
              placeholder="Username"
              className="block w-11/12 p-4 text-lg rounded-sm bg-black"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <div className="mt-2">
              <AvatarSelection
                avatarIndex={avatarIndex}
                setAvatarIndex={setAvatarIndex}
              />
            </div>
          </div>
          <div className="pb-2 pt-4">
            <input
              type="email"
              name="email"
              id="email"
              placeholder="Email"
              className="block w-full p-4 text-lg rounded-sm bg-black"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="pb-2 pt-4">
            <input
              className="block w-full p-4 text-lg rounded-sm bg-black"
              type="password"
              name="password"
              id="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="pb-2 pt-4">
            <input
              className="block w-full p-4 text-lg rounded-sm bg-black"
              type="password"
              name="confirmPass"
              id="confirmPass"
              placeholder="Re-enter your password"
              value={confirmPass}
              onChange={(e) => setConfirmPass(e.target.value)}
            />
          </div>
          <a
            href="#"
            className="hover:underline hover:text-gray-100 text-gray-400"
            onClick={() => {
              setRegisterFail(false);
              setToggleRegister(false);
            }}
          >
            Already have an account? Sign in instead
          </a>
          <div className="px-4 pb-2 pt-4">
            <button
              className="uppercase block w-full p-4 text-lg rounded-full bg-indigo-500 hover:bg-indigo-600 focus:outline-none"
              onClick={handleRegister}
            >
              Register
            </button>
          </div>
        </form>
      </>
    );
  } else {
    return <></>;
  }
}

export default RegisterForm;
