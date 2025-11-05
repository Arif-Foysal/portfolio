interface ApiOptions {
  params?: Record<string, any>
  timeout?: number
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  body?: any
  headers?: Record<string, string>
}

interface ApiResponse<T = any> {
  data: T
  success: boolean
  error?: string
}

export const useApi = () => {
  const { $config } = useNuxtApp()
  const apiBaseUrl = $config.public.apiBaseUrl

  // Generic API call with error handling
  const apiCall = async <T = any>(
    endpoint: string, 
    options: ApiOptions = {}
  ): Promise<ApiResponse<T>> => {
    try {
      const { params, timeout = 30000, method = 'GET', body, headers = {} } = options
      
      // Build URL with params
      let url = `${apiBaseUrl}${endpoint}`
      if (params) {
        const searchParams = new URLSearchParams(params)
        url += `?${searchParams.toString()}`
      }

      // Default headers
      const defaultHeaders = {
        'Content-Type': 'application/json',
        ...headers
      }

      const response = await $fetch<T>(url, {
        method,
        headers: defaultHeaders,
        body,
        timeout
      })

      return {
        data: response,
        success: true
      }
    } catch (error: any) {
      console.error('API Error:', error)
      return {
        data: null as T,
        success: false,
        error: error.message || 'An error occurred'
      }
    }
  }

  // Specific HTTP methods
  const get = <T = any>(endpoint: string, params?: Record<string, any>) =>
    apiCall<T>(endpoint, { method: 'GET', params })

  const post = <T = any>(endpoint: string, body?: any, headers?: Record<string, string>) =>
    apiCall<T>(endpoint, { method: 'POST', body, headers })

  const put = <T = any>(endpoint: string, body?: any) =>
    apiCall<T>(endpoint, { method: 'PUT', body })

  const del = <T = any>(endpoint: string) =>
    apiCall<T>(endpoint, { method: 'DELETE' })

  return {
    apiBaseUrl,
    apiCall,
    get,
    post,
    put,
    delete: del
  }
}
