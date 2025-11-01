import { useState } from "#imports"

export const useChatState = () => {
  const initialMessage = useState<string>('initialMessage', () => '')
  
  return {
    initialMessage
  }
}