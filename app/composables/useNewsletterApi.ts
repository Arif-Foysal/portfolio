interface NewsletterSubscription {
  email: string
  name?: string
}

interface NewsletterResponse {
  success: boolean
  message: string
}

export const useNewsletterApi = () => {
  const { post } = useApi()

  const subscribe = async (data: NewsletterSubscription) => {
    return await post<NewsletterResponse>('/newsletter/subscribe', data)
  }

  const unsubscribe = async (email: string) => {
    return await post<NewsletterResponse>('/newsletter/unsubscribe', { email })
  }

  return {
    subscribe,
    unsubscribe
  }
}
