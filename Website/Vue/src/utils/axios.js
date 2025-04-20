import axios from 'axios'

// Get API URL from environment or default to localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Create axios instance with CSRF token handling
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor to include CSRF token from cookies
api.interceptors.request.use(config => {
  // Get CSRF token from cookie
  const csrfToken = getCookie('csrftoken')
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

// Helper function to get cookie value by name
function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) {
    return parts.pop().split(';').shift()
  }
  return null
}

export default api 