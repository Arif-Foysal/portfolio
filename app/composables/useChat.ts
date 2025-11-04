import { useState, useAsyncData, useNuxtData } from "#imports"

interface AnonymousAuthResponse {
  success: boolean
  user_id: string
  session_id: string
  token: string
  is_anonymous: boolean
}

interface SessionRefreshResponse {
  success: boolean
  message: string
  new_session?: boolean
  user_id?: string
  session_id?: string
  token?: string
}

interface SessionValidationResponse {
  valid: boolean
  user_id?: string
  message?: string
}

export const useChatState = () => {
  const initialMessage = useState<string>('initialMessage', () => '')
  const userId = useState<string | null>('userId', () => null)
  const sessionId = useState<string | null>('sessionId', () => null)
  const authToken = useState<string | null>('authToken', () => null)
  const isAuthenticated = useState<boolean>('isAuthenticated', () => false)
  
  return {
    initialMessage,
    userId,
    sessionId,
    authToken,
    isAuthenticated
  }
}

export const useAuthentication = () => {
  const { userId, sessionId, authToken, isAuthenticated } = useChatState()
  const API_BASE_URL = process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000'
  
  const signInAnonymously = async (): Promise<AnonymousAuthResponse> => {
    try {
      const response = await $fetch<AnonymousAuthResponse>(`${API_BASE_URL}/auth/anonymous`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (response.success) {
        console.log('DEBUG: Anonymous sign-in successful:', response)
        
        userId.value = response.user_id
        sessionId.value = response.session_id
        authToken.value = response.token
        isAuthenticated.value = true
        
        console.log('DEBUG: Set userId to:', userId.value)
        
        // Save to sessionStorage for persistence
        if (process.client) {
          sessionStorage.setItem('user_id', response.user_id)
          sessionStorage.setItem('session_id', response.session_id)
          sessionStorage.setItem('auth_token', response.token)
        }
        
        return response
      }
      
      throw new Error('Anonymous sign-in failed')
    } catch (error) {
      console.error('Anonymous sign-in failed:', error)
      throw error
    }
  }
  
  const validateSession = async (sess_id: string): Promise<boolean> => {
    try {
      const response = await $fetch<SessionValidationResponse>(`${API_BASE_URL}/auth/validate/${sess_id}`, {
        method: 'GET'
      })
      
      return response.valid
    } catch (error) {
      console.error('Session validation failed:', error)
      return false
    }
  }
  
  const refreshSession = async (sess_id: string): Promise<boolean> => {
    try {
      const response = await $fetch<SessionRefreshResponse>(`${API_BASE_URL}/auth/refresh/${sess_id}`, {
        method: 'POST'
      })
      
      // Check if a new session was created
      if (response.new_session) {
        console.log('Refresh created new session:', response)
        
        // Update session data with new values
        userId.value = response.user_id!
        sessionId.value = response.session_id!
        authToken.value = response.token!
        isAuthenticated.value = true
        
        // Save to sessionStorage
        if (process.client) {
          sessionStorage.setItem('user_id', response.user_id!)
          sessionStorage.setItem('session_id', response.session_id!)
          sessionStorage.setItem('auth_token', response.token!)
        }
      }
      
      return true
    } catch (error) {
      console.error('Session refresh failed:', error)
      
      // If refresh fails completely, try to sign in anonymously
      try {
        console.log('Attempting to create new anonymous session after refresh failure')
        await signInAnonymously()
        return true
      } catch (signInError) {
        console.error('Failed to create new session after refresh failure:', signInError)
        return false
      }
    }
  }
  
  const logout = async (): Promise<void> => {
    try {
      if (sessionId.value) {
        await $fetch(`${API_BASE_URL}/auth/logout/${sessionId.value}`, {
          method: 'POST'
        })
      }
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      userId.value = null
      sessionId.value = null
      authToken.value = null
      isAuthenticated.value = false
      
      // Clear from sessionStorage
      if (process.client) {
        sessionStorage.removeItem('user_id')
        sessionStorage.removeItem('session_id')
        sessionStorage.removeItem('auth_token')
      }
    }
  }
  
  const restoreSession = (): void => {
    if (!process.client) return
    
    const storedUserId = sessionStorage.getItem('user_id')
    const storedSessionId = sessionStorage.getItem('session_id')
    const storedToken = sessionStorage.getItem('auth_token')
    
    if (storedUserId && storedSessionId && storedToken) {
      userId.value = storedUserId
      sessionId.value = storedSessionId
      authToken.value = storedToken
      isAuthenticated.value = true
    }
  }
  
  return {
    signInAnonymously,
    validateSession,
    refreshSession,
    logout,
    restoreSession,
    userId,
    sessionId,
    authToken,
    isAuthenticated
  }
}