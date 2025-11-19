/**
 * API utility functions
 */

import axios from 'axios'
import { getToken } from './auth'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Network errors (no response from server)
    if (!error.response) {
      error.userMessage = 'Network error. Please check your internet connection and try again.'
      error.canRetry = true
      error.retryable = true
      return Promise.reject(error)
    }

    // HTTP errors with contextual messages
    const status = error.response.status
    const statusMessages = {
      400: 'Invalid request. Please check your input and try again.',
      401: 'Your session has expired. Please log in again.',
      403: 'You don\'t have permission to perform this action.',
      404: 'The requested resource was not found.',
      409: 'This action conflicts with existing data. Please refresh and try again.',
      422: 'Invalid data provided. Please check your input.',
      429: 'Too many requests. Please wait a moment and try again.',
      500: 'Server error. Our team has been notified. Please try again later.',
      502: 'Service temporarily unavailable. Please try again in a moment.',
      503: 'Service temporarily unavailable. Please try again in a few moments.',
      504: 'Request timeout. Please try again.'
    }

    // Use backend error message if available, otherwise use status message
    error.userMessage = error.response?.data?.detail ||
                       error.response?.data?.message ||
                       statusMessages[status] ||
                       'An unexpected error occurred. Please try again.'

    // Mark which errors are retryable
    error.canRetry = [408, 429, 500, 502, 503, 504].includes(status)
    error.retryable = error.canRetry

    return Promise.reject(error)
  }
)

// Authentication
export const login = async (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)

  const response = await axios.post(`${API_URL}/api/auth/login`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const register = async (userData) => {
  const response = await axios.post(`${API_URL}/api/auth/register`, userData)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/api/auth/me')
  return response.data
}

export const verifyToken = async () => {
  const response = await api.get('/api/auth/verify')
  return response.data
}

// Lessons
export const getLessons = async () => {
  const response = await api.get('/api/lessons')
  return response.data
}

export const getLessonBySlug = async (slug) => {
  const response = await api.get(`/api/lessons/slug/${slug}`)
  return response.data
}

export const getLessonById = async (id) => {
  const response = await api.get(`/api/lessons/${id}`)
  return response.data
}

// Code Execution
export const executeCode = async (codeData) => {
  const response = await api.post('/api/code/execute', codeData)
  return response.data
}

export const getSubmissions = async (limit = 10, offset = 0) => {
  const response = await api.get('/api/code/submissions', {
    params: { limit, offset },
  })
  return response.data
}

export const getSubmission = async (submissionId) => {
  const response = await api.get(`/api/code/submissions/${submissionId}`)
  return response.data
}

export const getRuntimes = async () => {
  const response = await api.get('/api/code/runtimes')
  return response.data
}

// Progress
export const getProgressOverview = async () => {
  const response = await api.get('/api/progress/overview')
  return response.data
}

export const getLessonsWithProgress = async () => {
  const response = await api.get('/api/progress/lessons')
  return response.data
}

export const getLessonProgress = async (lessonId) => {
  const response = await api.get(`/api/progress/lesson/${lessonId}`)
  return response.data
}

export const updateProgress = async (lessonId, progressData) => {
  const response = await api.post(`/api/progress/lesson/${lessonId}`, progressData)
  return response.data
}

export const resetProgress = async (lessonId) => {
  const response = await api.delete(`/api/progress/lesson/${lessonId}`)
  return response.data
}

export default api
