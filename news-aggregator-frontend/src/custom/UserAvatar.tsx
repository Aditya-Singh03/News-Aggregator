import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function UserAvatar(UserAvatarProp: {
  avatarIndex: 0 | 1 | 2 | 3 | 4 | 5 | number;
}) {
  const avatarIndex = UserAvatarProp.avatarIndex;
  const avatarPath = `./public/avatars/avatar${avatarIndex}.png`;
  return (
    <Avatar>
      <AvatarImage src={avatarPath} alt="@shadcn" />
      <AvatarFallback>User</AvatarFallback>
    </Avatar>
  );
}
