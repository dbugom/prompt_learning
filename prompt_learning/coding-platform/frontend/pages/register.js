/**
 * Registration page
 */

import { useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../styles/Auth.module.css'
import { register } from '../utils/api'
import { setToken } from '../utils/auth'

export default function Register() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    fullName: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [touchedFields, setTouchedFields] = useState({})
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  // Password strength calculator
  const getPasswordStrength = (password) => {
    let strength = 0
    if (password.length >= 8) strength++
    if (password.length >= 12) strength++
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
    if (/\d/.test(password)) strength++
    if (/[^A-Za-z0-9]/.test(password)) strength++
    return strength
  }

  const passwordStrength = getPasswordStrength(formData.password)
  const strengthLabels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
  const strengthColors = ['#f44336', '#ff5722', '#ff9800', '#ffc107', '#8bc34a', '#4caf50']

  // Field validation
  const validateField = (name, value) => {
    switch (name) {
      case 'email':
        if (!value) return 'Email is required'
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return 'Please enter a valid email address'
        }
        break
      case 'username':
        if (!value) return 'Username is required'
        if (value.length < 3) {
          return 'Username must be at least 3 characters'
        }
        if (!/^[a-zA-Z0-9_]+$/.test(value)) {
          return 'Username can only contain letters, numbers, and underscores'
        }
        break
      case 'password':
        if (!value) return 'Password is required'
        if (value.length < 8) {
          return 'Password must be at least 8 characters'
        }
        if (passwordStrength < 2) {
          return 'Password is too weak. Add numbers, symbols, or mix upper and lower case.'
        }
        break
      case 'confirmPassword':
        if (!value) return 'Please confirm your password'
        if (value !== formData.password) {
          return 'Passwords do not match'
        }
        break
    }
    return null
  }

  const handleBlur = (e) => {
    const { name, value } = e.target
    setTouchedFields({ ...touchedFields, [name]: true })
    const error = validateField(name, value)
    setFieldErrors({ ...fieldErrors, [name]: error })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    // Validate password length
    if (formData.password.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }

    setIsLoading(true)

    try {
      const response = await register({
        email: formData.email,
        username: formData.username,
        password: formData.password,
        full_name: formData.fullName || null
      })
      setToken(response.access_token)
      toast.success('Registration successful!')
      router.push('/lessons')
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed. Please try again.'
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })

    // Validate only if field has been touched
    if (touchedFields[name]) {
      const error = validateField(name, value)
      setFieldErrors({ ...fieldErrors, [name]: error })
    }

    // Also validate confirmPassword if password changes
    if (name === 'password' && touchedFields.confirmPassword) {
      const confirmError = validateField('confirmPassword', formData.confirmPassword)
      setFieldErrors({ ...fieldErrors, [name]: null, confirmPassword: confirmError })
    }
  }

  return (
    <>
      <Head>
        <title>Register - Coding Platform</title>
        <meta name="description" content="Create your account" />
      </Head>

      <div className={styles.container}>
        <div className={styles.card} role="main">
          <h1 className={styles.title} id="register-heading">Create Account</h1>
          <p className={styles.subtitle}>Start your coding journey today</p>

          <form
            onSubmit={handleSubmit}
            className={styles.form}
            aria-labelledby="register-heading"
          >
            <div className={styles.formGroup}>
              <label htmlFor="email">Email *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                onBlur={handleBlur}
                placeholder="your.email@example.com"
                required
                autoComplete="email"
                aria-invalid={!!fieldErrors.email}
                aria-describedby={fieldErrors.email ? "email-error" : undefined}
                className={fieldErrors.email && touchedFields.email ? styles.inputError : ''}
              />
              {fieldErrors.email && touchedFields.email && (
                <span id="email-error" className={styles.errorMessage} role="alert">
                  {fieldErrors.email}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="username">Username *</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                onBlur={handleBlur}
                placeholder="Choose a username"
                required
                minLength={3}
                maxLength={50}
                autoComplete="username"
                aria-invalid={!!fieldErrors.username}
                aria-describedby={fieldErrors.username ? "username-error" : undefined}
                className={fieldErrors.username && touchedFields.username ? styles.inputError : ''}
              />
              {fieldErrors.username && touchedFields.username && (
                <span id="username-error" className={styles.errorMessage} role="alert">
                  {fieldErrors.username}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="fullName">Full Name (optional)</label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="Your full name"
                autoComplete="name"
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password">Password *</label>
              <div className={styles.passwordField}>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  placeholder="At least 8 characters"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  aria-invalid={!!fieldErrors.password}
                  aria-describedby={fieldErrors.password ? "password-error password-strength" : "password-strength"}
                  className={fieldErrors.password && touchedFields.password ? styles.inputError : ''}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className={styles.togglePassword}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  tabIndex={-1}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {formData.password && (
                <div className={styles.passwordStrength} id="password-strength" aria-live="polite">
                  <div className={styles.strengthBar}>
                    <div
                      className={styles.strengthFill}
                      style={{
                        width: `${(passwordStrength / 5) * 100}%`,
                        background: strengthColors[passwordStrength]
                      }}
                    />
                  </div>
                  <span style={{ color: strengthColors[passwordStrength], fontSize: '0.85rem' }}>
                    {strengthLabels[passwordStrength]}
                  </span>
                </div>
              )}
              {fieldErrors.password && touchedFields.password && (
                <span id="password-error" className={styles.errorMessage} role="alert">
                  {fieldErrors.password}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">Confirm Password *</label>
              <div className={styles.passwordField}>
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  placeholder="Confirm your password"
                  required
                  minLength={8}
                  autoComplete="new-password"
                  aria-invalid={!!fieldErrors.confirmPassword}
                  aria-describedby={fieldErrors.confirmPassword ? "confirm-password-error" : undefined}
                  className={fieldErrors.confirmPassword && touchedFields.confirmPassword ? styles.inputError : ''}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className={styles.togglePassword}
                  aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                  tabIndex={-1}
                >
                  {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {fieldErrors.confirmPassword && touchedFields.confirmPassword && (
                <span id="confirm-password-error" className={styles.errorMessage} role="alert">
                  {fieldErrors.confirmPassword}
                </span>
              )}
            </div>

            <button
              type="submit"
              className={styles.submitButton}
              disabled={isLoading}
            >
              {isLoading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <div className={styles.footer}>
            <p>
              Already have an account?{' '}
              <Link href="/login">
                Login here
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
