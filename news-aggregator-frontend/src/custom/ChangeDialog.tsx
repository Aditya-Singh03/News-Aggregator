import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { UserInfo } from "@/types";
import { BACKEND_URL } from "@/utils/constants";
import { useState } from "react";

function ChangeDialog(ChangeDialogProps: {
  changeName: string;
  subText: string;
  authToken: string;
  userProfile: UserInfo;
  setUserProfile: (profile: UserInfo) => void;
}) {
  const changeName = ChangeDialogProps.changeName;
  const subText = ChangeDialogProps.subText;
  const authToken = ChangeDialogProps.authToken;
  const userProfile = ChangeDialogProps.userProfile;
  const setUserProfile = ChangeDialogProps.setUserProfile;

  const [changeEmail, setChangeEmail] = useState("");
  const [changePassword, setChangePassword] = useState("");
  const [showSelection, setShowSelection] = useState(false);

  const currRequest = changeName === "email" ? "email_address" : "password";
  const currFeature = changeName === "email" ? changeEmail : changePassword;

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    fetch(`${BACKEND_URL}/user/update-user`, {
        method: "PUT",
        headers: {
            Authorization: `Bearer ${authToken}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ [currRequest]: currFeature }),
    }).then(res => {
        if (res.status === 200) { 
            setShowSelection(false)
            setUserProfile({
                username: userProfile.username,
                email: changeName == "email"? currFeature: userProfile.email,
                avatarIndex: userProfile.avatarIndex,
            })

        }
    }).catch()
  };

  return (
    <Dialog open={showSelection} onOpenChange={setShowSelection}>
      <DialogTrigger>
        <Button
          variant="outline"
          className="bg-[#161616] border-2 mt-3 border-white rounded-2xl font-semibold pl-3 pr-3 hover:bg-[#222222] hover:text-white"
        >
          Change
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] bg-[#161616] text-white">
        <DialogHeader>
          <DialogTitle>Edit {changeName}</DialogTitle>
          <DialogDescription className="text-slate-200">
            {subText}
          </DialogDescription>
        </DialogHeader>
        <div>
          <Input
            id="name"
            type={changeName}
            value={currFeature}
            className="col-span-3 text-black z-50"
            onChange={(e) =>
              changeName === "email"
                ? setChangeEmail(e.target.value)
                : setChangePassword(e.target.value)
            }
          />
        </div>
        <DialogFooter>
          <Button
            type="submit"
            onClick={handleSubmit}
            className="bg-white text-black hover:bg-slate-200 mt-2"
          >
            Save
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default ChangeDialog;
