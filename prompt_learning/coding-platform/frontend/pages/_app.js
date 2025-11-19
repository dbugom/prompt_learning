/**
 * Next.js App component
 * Wraps all pages with global providers and styles
 */

import { Toaster } from 'react-hot-toast'
import SessionManager from '../components/SessionManager'
import '../styles/globals.css'

export default function App({ Component, pageProps }) {
  return (
    <>
      <SessionManager />
      <Component {...pageProps} />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#4CAF50',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#F44336',
              secondary: '#fff',
            },
          },
        }}
      />
    </>
  )
}
