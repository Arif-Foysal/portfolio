interface ChatMessage {
  message: string
  user_id: string
  session_id: string
}

interface ChatResponse {
  type: string
  data: string | any
  session_id: string
}

export const useChatApi = () => {
  const { post } = useApi()
  const { authToken } = useAuthentication()

  const sendMessage = async (messageData: ChatMessage) => {
    const headers: Record<string, string> = {}
    if (authToken?.value) {
      headers['Authorization'] = `Bearer ${authToken.value}`
    }

    return await post<ChatResponse>('/chat/', messageData, headers)
  }

  return {
    sendMessage
  }
}
