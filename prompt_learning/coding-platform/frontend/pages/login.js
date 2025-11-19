/**
 * Login page
 */

import { useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../styles/Auth.module.css'
import { login } from '../utils/api'
import { setToken } from '../utils/auth'

export default function Login() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await login(formData.username, formData.password)
      setToken(response.access_token)
      toast.success('Welcome back! Redirecting to lessons...')
      router.push('/lessons')
    } catch (error) {
      // Use improved error message from interceptor
      const message = error.userMessage || error.response?.data?.detail || 'Login failed. Please try again.'

      // Special handling for authentication errors
      if (error.response?.status === 401) {
        toast.error('Invalid username or password. Please check your credentials and try again.')
      } else {
        toast.error(message)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <>
      <Head>
        <title>Login - Coding Platform</title>
        <meta name="description" content="Login to your account" />
      </Head>

      <div className={styles.container}>
        <div className={styles.card} role="main">
          <h1 className={styles.title} id="login-heading">Welcome Back</h1>
          <p className={styles.subtitle}>Login to continue learning</p>

          <form
            onSubmit={handleSubmit}
            className={styles.form}
            aria-labelledby="login-heading"
          >
            <div className={styles.formGroup}>
              <label htmlFor="username">Username or Email</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your username or email"
                required
                autoComplete="username"
                aria-required="true"
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
                autoComplete="current-password"
                aria-required="true"
              />
            </div>

            <button
              type="submit"
              className={styles.submitButton}
              disabled={isLoading}
              aria-busy={isLoading}
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <div className={styles.footer}>
            <p>
              Don't have an account?{' '}
              <Link href="/register">
                Register here
              </Link>
            </p>
          </div>

          <div className={styles.backLink}>
            <Link href="/">
              ← Back to home
            </Link>
          </div>
        </div>
      </div>
    </>
  )
}
