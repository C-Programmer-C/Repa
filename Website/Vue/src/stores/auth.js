import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const csrfToken = ref('')

  // Initialize from session storage if available
  const storedUser = sessionStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
    isAuthenticated.value = true
  }

  // Set CSRF token for subsequent requests
  const setCsrfToken = (token) => {
    csrfToken.value = token
    api.defaults.headers.common['X-CSRFToken'] = token
  }

  // Login user
  const login = async (username, password, userType) => {
    try {
      const response = await api.post('/login/', {
        username,
        password,
        user_type: userType
      })
      
      const { user: userData, csrfToken: token } = response.data
      user.value = userData
      isAuthenticated.value = true
      setCsrfToken(token)
      
      // Store in session storage
      sessionStorage.setItem('user', JSON.stringify(userData))
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.error || 'Ошибка входа в систему'
      return { success: false, message }
    }
  }

  // Register new user
  const register = async (userData) => {
    try {
      const response = await api.post('/register/', userData)
      
      const { user: newUser, csrfToken: token } = response.data
      user.value = newUser
      isAuthenticated.value = true
      setCsrfToken(token)
      
      // Store in session storage
      sessionStorage.setItem('user', JSON.stringify(newUser))
      
      return { success: true }
    } catch (error) {
      const errors = error.response?.data?.errors || { 'error': 'Ошибка регистрации' }
      return { success: false, errors }
    }
  }

  // Logout user
  const logout = async () => {
    try {
      await api.post('/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
      isAuthenticated.value = false
      sessionStorage.removeItem('user')
    }
  }

  // Get current user info
  const getCurrentUser = async () => {
    try {
      const response = await api.get('/user/')
      user.value = response.data.user
      isAuthenticated.value = true
      sessionStorage.setItem('user', JSON.stringify(response.data.user))
      return true
    } catch (error) {
      console.error('Error fetching user:', error)
      return false
    }
  }

  return {
    user,
    isAuthenticated,
    login,
    register,
    logout,
    getCurrentUser,
    api
  }
})
