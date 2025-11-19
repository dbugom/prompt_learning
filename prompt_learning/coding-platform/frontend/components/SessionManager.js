/**
 * SessionManager - Handles session timeout warnings
 */

import { useEffect } from 'react'
import { useRouter } from 'next/router'
import { toast } from 'react-hot-toast'
import { getToken, removeToken } from '../utils/auth'
import { verifyToken } from '../utils/api'

const SESSION_TIMEOUT = 60 * 60 * 1000 // 60 minutes
const WARNING_TIME = 5 * 60 * 1000 // 5 minutes before timeout

export default function SessionManager() {
  const router = useRouter()

  useEffect(() => {
    let warningTimeout
    let logoutTimeout
    let warningToastId

    const refreshSession = async () => {
      try {
        await verifyToken()
        resetTimers()
        if (warningToastId) {
          toast.dismiss(warningToastId)
        }
        toast.success('Session extended')
      } catch (error) {
        console.error('Failed to refresh session:', error)
      }
    }

    const resetTimers = () => {
      clearTimeout(warningTimeout)
      clearTimeout(logoutTimeout)

      const token = getToken()
      if (!token) return

      // Warn 5 minutes before timeout
      warningTimeout = setTimeout(() => {
        warningToastId = toast(
          (t) => (
            <div>
              <strong style={{ display: 'block', marginBottom: '8px' }}>
                Session Expiring Soon
              </strong>
              <p style={{ marginBottom: '12px', fontSize: '0.9em' }}>
                Your session will expire in 5 minutes due to inactivity.
              </p>
              <button
                onClick={() => {
                  toast.dismiss(t.id)
                  refreshSession()
                }}
                style={{
                  padding: '6px 16px',
                  background: '#667eea',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '0.9em',
                  fontWeight: 600
                }}
              >
                Stay Logged In
              </button>
            </div>
          ),
          {
            duration: Infinity,
            icon: '⏰',
          }
        )
      }, SESSION_TIMEOUT - WARNING_TIME)

      // Logout after timeout
      logoutTimeout = setTimeout(() => {
        removeToken()
        router.push('/login?reason=session_expired')
        toast.error('Your session has expired. Please log in again.')
      }, SESSION_TIMEOUT)
    }

    // Start timers if user is logged in
    const token = getToken()
    if (token) {
      resetTimers()

      // Reset timers on user activity
      const events = ['mousedown', 'keydown', 'scroll', 'touchstart']
      const handleActivity = () => {
        const currentToken = getToken()
        if (currentToken) {
          resetTimers()
          if (warningToastId) {
            toast.dismiss(warningToastId)
            warningToastId = null
          }
        }
      }

      events.forEach((event) => {
        document.addEventListener(event, handleActivity, { passive: true })
      })

      return () => {
        clearTimeout(warningTimeout)
        clearTimeout(logoutTimeout)
        events.forEach((event) => {
          document.removeEventListener(event, handleActivity)
        })
      }
    }
  }, [router])

  return null // This component doesn't render anything
}
