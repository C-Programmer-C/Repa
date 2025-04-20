import api from '@/utils/axios'

// API service for handling help requests
export const requestsApi = {
  // Get all requests with optional filters
  async getRequests(filters = {}) {
    try {
      const queryParams = new URLSearchParams()
      if (filters.status) queryParams.append('status', filters.status)
      if (filters.help_type) queryParams.append('help_type', filters.help_type)
      
      const response = await api.get(`/requests/?${queryParams.toString()}`)
      return { success: true, data: response.data.requests }
    } catch (error) {
      console.error('Error fetching requests:', error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Ошибка получения данных'
      }
    }
  },
  
  // Get a specific request by ID
  async getRequest(id) {
    try {
      const response = await api.get(`/requests/${id}/`)
      return { success: true, data: response.data }
    } catch (error) {
      console.error(`Error fetching request ${id}:`, error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Ошибка получения данных заявки'
      }
    }
  },
  
  // Create a new help request
  async createRequest(requestData) {
    try {
      const response = await api.post('/requests/create/', requestData)
      return { success: true, data: response.data.request }
    } catch (error) {
      console.error('Error creating request:', error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Ошибка создания заявки'
      }
    }
  },
  
  // Respond to an existing request
  async respondToRequest(requestId, contactInfo) {
    try {
      const response = await api.post(`/requests/${requestId}/respond/`, {
        contact_info: contactInfo
      })
      return { success: true, data: response.data }
    } catch (error) {
      console.error(`Error responding to request ${requestId}:`, error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Ошибка отклика на заявку'
      }
    }
  },
  
  // Mark a request as completed
  async completeRequest(requestId) {
    try {
      const response = await api.post(`/requests/${requestId}/complete/`)
      return { success: true, data: response.data }
    } catch (error) {
      console.error(`Error completing request ${requestId}:`, error)
      return { 
        success: false, 
        error: error.response?.data?.error || 'Ошибка завершения заявки'
      }
    }
  }
} 