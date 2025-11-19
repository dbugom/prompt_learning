/**
 * Lessons list page
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../../styles/Lessons.module.css'
import { getLessons, getLessonsWithProgress, getCurrentUser } from '../../utils/api'
import { getToken, removeToken } from '../../utils/auth'

export default function Lessons() {
  const router = useRouter()
  const [lessons, setLessons] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [stats, setStats] = useState(null)
  const [currentUser, setCurrentUser] = useState(null)

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
      // Load current user info
      const user = await getCurrentUser()
      setCurrentUser(user)

      // Load lessons with progress
      const progressData = await getLessonsWithProgress()

      // Load lessons with access control
      const accessData = await getLessons()

      // Merge progress and access data
      const mergedData = progressData.map(progressLesson => {
        const accessLesson = accessData.find(l => l.id === progressLesson.lesson_id)
        return {
          ...progressLesson,
          is_accessible: accessLesson?.is_accessible ?? true
        }
      })

      setLessons(mergedData)

      // Calculate stats
      const completed = mergedData.filter(l => l.is_completed).length
      const total = mergedData.length
      const avgScore = mergedData.reduce((sum, l) => sum + l.best_score, 0) / (total || 1)

      setStats({
        completed,
        total,
        inProgress: mergedData.filter(l => l.attempts > 0 && !l.is_completed).length,
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
          <div className={styles.headerActions}>
            {currentUser?.is_admin && (
              <Link href="/admin/students" className={styles.adminButton}>
                🔐 Admin Panel
              </Link>
            )}
            <button onClick={handleLogout} className={styles.logoutButton}>
              Logout
            </button>
          </div>
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
              {lessons.map((lesson) => {
                const isLocked = !lesson.is_accessible

                return (
                  <div
                    key={lesson.lesson_id}
                    className={`${styles.lessonCard} ${isLocked ? styles.locked : ''}`}
                    onClick={() => {
                      if (isLocked) {
                        toast.error('This lesson is locked. Please contact an administrator.')
                      } else {
                        router.push(`/lessons/${lesson.lesson_slug}`)
                      }
                    }}
                  >
                    <div className={styles.lessonHeader}>
                      <h3>{lesson.lesson_title}</h3>
                      <div className={styles.badges}>
                        {isLocked && (
                          <span className={styles.lockedBadge}>🔒 Locked</span>
                        )}
                        {lesson.is_completed && !isLocked && (
                          <span className={styles.completedBadge}>✓</span>
                        )}
                      </div>
                    </div>

                    <div className={styles.lessonMeta}>
                      <span
                        className={styles.difficulty}
                        style={{ backgroundColor: getDifficultyColor(lesson.difficulty) }}
                      >
                        {lesson.difficulty || 'beginner'}
                      </span>
                    </div>

                    {!isLocked && lesson.attempts > 0 && (
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

                    {!isLocked && lesson.attempts === 0 && (
                      <div className={styles.startPrompt}>
                        Click to start →
                      </div>
                    )}

                    {isLocked && (
                      <div className={styles.lockedMessage}>
                        Access restricted. Contact your administrator.
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
