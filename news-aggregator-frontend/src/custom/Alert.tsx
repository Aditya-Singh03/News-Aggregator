import { AlertCircle } from "lucide-react"

import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert"
import { MessageProp } from "../types";

export function AlertDestructive(messageProp: MessageProp) {
    const message = messageProp.message;
    const error = messageProp.error;
    return (
    <Alert variant="destructive" className="mt-2">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>{error}</AlertTitle>
      <AlertDescription>
        {message}
      </AlertDescription>
    </Alert>
  )
}
