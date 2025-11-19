/**
 * Lessons list page
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../../styles/Lessons.module.css'
import { getLessonsWithProgress } from '../../utils/api'
import { getToken, removeToken } from '../../utils/auth'

export default function Lessons() {
  const router = useRouter()
  const [lessons, setLessons] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    // Check if user is logged in
    const token = getToken()
    if (!token) {
      router.push('/login')
      return
    }

    loadLessons()
  }, [router])

  const loadLessons = async () => {
    try {
      const data = await getLessonsWithProgress()
      setLessons(data)

      // Calculate stats
      const completed = data.filter(l => l.is_completed).length
      const total = data.length
      const avgScore = data.reduce((sum, l) => sum + l.best_score, 0) / (total || 1)

      setStats({
        completed,
        total,
        inProgress: data.filter(l => l.attempts > 0 && !l.is_completed).length,
        avgScore: Math.round(avgScore)
      })
    } catch (error) {
      console.error('Failed to load lessons:', error)
      if (error.response?.status === 401) {
        removeToken()
        router.push('/login')
      } else {
        toast.error('Failed to load lessons')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    removeToken()
    router.push('/')
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return '#4CAF50'
      case 'intermediate': return '#FF9800'
      case 'advanced': return '#F44336'
      default: return '#2196F3'
    }
  }

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
        <title>Lessons - Coding Platform</title>
        <meta name="description" content="Browse coding lessons" />
      </Head>

      <div className={styles.container}>
        <header className={styles.header}>
          <h1>My Learning Dashboard</h1>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Logout
          </button>
        </header>

        {stats && (
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.completed}</div>
              <div className={styles.statLabel}>Completed</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.inProgress}</div>
              <div className={styles.statLabel}>In Progress</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.total}</div>
              <div className={styles.statLabel}>Total Lessons</div>
            </div>
            <div className={styles.statCard}>
              <div className={styles.statValue}>{stats.avgScore}%</div>
              <div className={styles.statLabel}>Avg Score</div>
            </div>
          </div>
        )}

        <div className={styles.lessonsSection}>
          <h2>Available Lessons</h2>

          {lessons.length === 0 ? (
            <div className={styles.emptyState}>
              <p>No lessons available yet. Check back soon!</p>
            </div>
          ) : (
            <div className={styles.lessonsGrid}>
              {lessons.map((lesson) => (
                <Link
                  key={lesson.lesson_id}
                  href={`/lessons/${lesson.lesson_slug}`}
                  className={styles.lessonCard}
                >
                  <div className={styles.lessonHeader}>
                    <h3>{lesson.lesson_title}</h3>
                    {lesson.is_completed && (
                      <span className={styles.completedBadge}>✓</span>
                    )}
                  </div>

                  <div className={styles.lessonMeta}>
                    <span
                      className={styles.difficulty}
                      style={{ backgroundColor: getDifficultyColor(lesson.difficulty) }}
                    >
                      {lesson.difficulty || 'beginner'}
                    </span>
                  </div>

                  {lesson.attempts > 0 && (
                    <div className={styles.progress}>
                      <div className={styles.progressInfo}>
                        <span>Best Score: {lesson.best_score}%</span>
                        <span>Attempts: {lesson.attempts}</span>
                      </div>
                      <div className={styles.progressBar}>
                        <div
                          className={styles.progressFill}
                          style={{ width: `${lesson.best_score}%` }}
                        ></div>
                      </div>
                    </div>
                  )}

                  {lesson.attempts === 0 && (
                    <div className={styles.startPrompt}>
                      Click to start →
                    </div>
                  )}
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
