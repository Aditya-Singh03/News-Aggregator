import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { UserAvatar } from "./UserAvatar";
import { useState } from "react";

function AvatarSelection(AvatarSelectionProps: {
  avatarIndex: number;
  setAvatarIndex: (idx: number) => void;
}) {
  const avatarIndex = AvatarSelectionProps.avatarIndex;
  const setAvatarIndex = AvatarSelectionProps.setAvatarIndex;

  const [showSelection, setShowSelection] = useState(false);

  const handleSelection = (event: React.SyntheticEvent, idx: number) => {
    event.preventDefault();
    setAvatarIndex(idx);
    setShowSelection(false);
  };

  return (
    <>
      <DropdownMenu open={showSelection} onOpenChange={setShowSelection}>
        <DropdownMenuTrigger data-state="open">
          <UserAvatar avatarIndex={avatarIndex} />
        </DropdownMenuTrigger>
        {showSelection && (
          <DropdownMenuContent>
            <DropdownMenuLabel>Select your user Avatar</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <div className="flex">
              {[0, 1, 2].map((idx) => (
                <DropdownMenuItem
                  onClick={(e) => {
                    setShowSelection(false);
                    handleSelection(e, idx);
                  }}
                >
                  <UserAvatar avatarIndex={idx} />
                </DropdownMenuItem>
              ))}
            </div>
            <div className="flex">
              {[3, 4, 5].map((idx) => (
                <DropdownMenuItem onClick={(e) => handleSelection(e, idx)}>
                  <UserAvatar avatarIndex={idx} />
                </DropdownMenuItem>
              ))}
            </div>
          </DropdownMenuContent>
        )}
      </DropdownMenu>
    </>
  );
}

export default AvatarSelection;
