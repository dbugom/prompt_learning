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
