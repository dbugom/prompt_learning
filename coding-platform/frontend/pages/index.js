/**
 * Home page - Landing page with login/register
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import styles from '../styles/Home.module.css'
import { getToken, removeToken } from '../utils/auth'

export default function Home() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    const token = getToken()
    if (token) {
      router.push('/lessons')
    } else {
      setIsLoading(false)
    }
  }, [router])

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Coding Education Platform</title>
        <meta name="description" content="Learn to code interactively" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <div className={styles.hero}>
          <h1 className={styles.title}>
            Learn to Code <span className={styles.highlight}>Interactively</span>
          </h1>
          <p className={styles.description}>
            Master programming through hands-on coding exercises with instant feedback
          </p>

          <div className={styles.features}>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>💻</div>
              <h3>Interactive Editor</h3>
              <p>Write and execute code directly in your browser</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>⚡</div>
              <h3>Instant Feedback</h3>
              <p>Get immediate results and learn from your mistakes</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>📚</div>
              <h3>Structured Lessons</h3>
              <p>Progress through carefully designed curriculum</p>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>🔒</div>
              <h3>Secure Execution</h3>
              <p>Sandboxed environment for safe code execution</p>
            </div>
          </div>

          <div className={styles.actions}>
            <button
              className={`${styles.button} ${styles.primary}`}
              onClick={() => router.push('/register')}
            >
              Get Started
            </button>
            <button
              className={`${styles.button} ${styles.secondary}`}
              onClick={() => router.push('/login')}
            >
              Login
            </button>
          </div>
        </div>

        <footer className={styles.footer}>
          <p>Built with Next.js, FastAPI, and Piston</p>
        </footer>
      </main>
    </>
  )
}
