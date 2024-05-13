import { SetStateAction } from "react";

type UserForm = {
  email: string;
  password: string;
  setEmail: React.Dispatch<SetStateAction<string>>;
  setPassword: React.Dispatch<SetStateAction<string>>;
};

type BaseInfo = {
  setAuthToken: (token: string) => void;
  setLoginState: (loginState: LoginState) => void;
};

type PreferencesInfo = {
  authToken: string;
  setFirstTimeUser: (firstTimeUser: boolean) => void;
};

type LoginInfo = {
  setFirstTimeUser: (firstTimeUser: boolean) => void;
} & BaseInfo;

type FormInfo = {
  toggleRegister: boolean;
  setToggleRegister: React.Dispatch<SetStateAction<boolean>>;
} & UserForm;

type LoginError = {
  setSignInFail: (state: boolean) => void;
  setRegisterFail: (state: boolean) => void;
};

type SignInFormInfo = {
  setSignInFail: LoginError["setSignInFail"];
} & BaseInfo &
  FormInfo;
type RegisterFormInfo = {
  setRegisterFail: LoginError["setRegisterFail"];
} & LoginInfo &
  FormInfo;

type PostInfo = {
  id: string;
  title: string;
  date: string;
  media: string;
  upvotes: number;
  downvotes: number;
  summary: string;
  source_ids: Array<string>;
};
type SourceInfo = {
  id: string;
  title: string;
  link: string;
  author: string;
  date: string;
};
type UserInfo = {
  email: string;
  username: string;
  avatarIndex: number;
};

type UserVotes = {
  postUpvotes: string[];
  postDownvotes: string[];
  commentUpvotes: string[];
  commentDownvotes: string[];
};

type Comment = {
  id: string;
  content: string;
  upvotes: number;
  downvotes: number;
  author_id: string;
};

type HomeInfo = {
  authToken: string;
  setLoginState: (state: LoginState) => void;
};

enum HomeView {
  Content,
  Post,
}

enum LoginState {
  LoggedIn,
  Loading,
  LoggedOut,
}

type MessageProp = {
  error: string;
  message: string;
};

type HomeProfileInfo = {
  side: "top" | "bottom" | "left" | "right" | null | undefined;
  userProfile: UserInfo;
  authToken: string;
  setUserProfile: (user: UserInfo) => void;
  setLoginState: (state: LoginState) => void;
};

export type {
  LoginInfo,
  RegisterFormInfo,
  SignInFormInfo,
  PreferencesInfo,
  PostInfo,
  SourceInfo,
  HomeInfo,
  UserInfo,
  UserVotes,
  MessageProp,
  HomeProfileInfo,
  Comment,
};

export { HomeView, LoginState };
