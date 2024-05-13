import { LoginState, SignInFormInfo } from "./types";
import { BACKEND_URL } from "./utils/constants.ts";

function SignInForm(signInProps: SignInFormInfo) {
  const toggleRegister = signInProps.toggleRegister;
  const setToggleRegister = signInProps.setToggleRegister;
  const email = signInProps.email;
  const setEmail = signInProps.setEmail;
  const password = signInProps.password;
  const setPassword = signInProps.setPassword;
  const setAuthToken = signInProps.setAuthToken;
  const setLoginState = signInProps.setLoginState;
  const setSignInFail = signInProps.setSignInFail;

  function handleSignIn(event: React.SyntheticEvent) {
    event.preventDefault();

    // send fetch POST to backend to verify user and get back authentication token
    fetch(`${BACKEND_URL}/user/login`, {
      method: "POST",
      body: JSON.stringify({ email_address: email, password: password }),
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => (res.status === 200 ? res.json() : Promise.reject()))
      .then((json) => {
        setAuthToken(json.token);
        setLoginState(LoginState.LoggedIn);
      })
      .catch(() => setSignInFail(true));
  }

  if (!toggleRegister) {
    return (
      <>
        <form action="" className="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
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
          <a
            href="#"
            className="hover:underline text-gray-400 hover:text-gray-100"
            onClick={() => {
              setSignInFail(false);
              setToggleRegister(true);
            }}
          >
            Don't have an account? Register instead
          </a>
          <div className="px-4 pb-2 pt-4">
            <button
              className="uppercase block w-full p-4 text-lg rounded-full bg-indigo-500 hover:bg-indigo-600 focus:outline-none"
              onClick={handleSignIn}
            >
              sign in
            </button>
          </div>
        </form>
      </>
    );
  } else {
    return <></>;
  }
}

export default SignInForm;
