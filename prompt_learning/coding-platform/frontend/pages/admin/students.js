/**
 * Admin Panel - Student Lesson Access Management
 * Allows admins to enable/disable lessons for specific students
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../../styles/Admin.module.css'
import {
  getAllStudents,
  getStudentLessonAccess,
  updateLessonAccess,
  disableAllLessons,
  enableAllLessons,
  getCurrentUser
} from '../../utils/api'
import { getToken, removeToken } from '../../utils/auth'

export default function AdminStudentsPage() {
  const router = useRouter()
  const [currentUser, setCurrentUser] = useState(null)
  const [students, setStudents] = useState([])
  const [selectedStudent, setSelectedStudent] = useState(null)
  const [lessonAccess, setLessonAccess] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingLessons, setIsLoadingLessons] = useState(false)
  const [showDisableAllModal, setShowDisableAllModal] = useState(false)
  const [disableReason, setDisableReason] = useState('')

  useEffect(() => {
    // Check if user is logged in and is admin
    const token = getToken()
    if (!token) {
      router.push('/login')
      return
    }

    loadCurrentUser()
    loadStudents()
  }, [router])

  const loadCurrentUser = async () => {
    try {
      const user = await getCurrentUser()
      if (!user.is_admin) {
        toast.error('Access denied. Admin privileges required.')
        router.push('/lessons')
        return
      }
      setCurrentUser(user)
    } catch (error) {
      console.error('Failed to load user:', error)
      if (error.response?.status === 401) {
        removeToken()
        router.push('/login')
      } else {
        toast.error('Failed to verify admin status')
      }
    }
  }

  const loadStudents = async () => {
    try {
      const data = await getAllStudents()
      setStudents(data)
    } catch (error) {
      console.error('Failed to load students:', error)
      if (error.response?.status === 403) {
        toast.error('Access denied. Admin privileges required.')
        router.push('/lessons')
      } else {
        toast.error('Failed to load students list')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const loadStudentLessons = async (student) => {
    setSelectedStudent(student)
    setIsLoadingLessons(true)

    try {
      const data = await getStudentLessonAccess(student.id)
      setLessonAccess(data)
    } catch (error) {
      console.error('Failed to load lesson access:', error)
      toast.error('Failed to load lesson access data')
    } finally {
      setIsLoadingLessons(false)
    }
  }

  const toggleLessonAccess = async (lesson) => {
    const newStatus = !lesson.is_enabled
    const actionText = newStatus ? 'enable' : 'disable'

    try {
      await updateLessonAccess(selectedStudent.id, lesson.lesson_id, {
        is_enabled: newStatus,
        disabled_reason: newStatus ? null : 'Disabled by admin'
      })

      // Update local state
      setLessonAccess((prev) =>
        prev.map((l) =>
          l.lesson_id === lesson.lesson_id ? { ...l, is_enabled: newStatus } : l
        )
      )

      toast.success(`Lesson ${actionText}d successfully`)
    } catch (error) {
      console.error(`Failed to ${actionText} lesson:`, error)
      toast.error(`Failed to ${actionText} lesson`)
    }
  }

  const handleDisableAll = async () => {
    try {
      await disableAllLessons(selectedStudent.id, disableReason || 'All lessons disabled by admin')

      // Reload lesson access
      loadStudentLessons(selectedStudent)

      toast.success(`All lessons disabled for ${selectedStudent.username}`)
      setShowDisableAllModal(false)
      setDisableReason('')
    } catch (error) {
      console.error('Failed to disable all lessons:', error)
      toast.error('Failed to disable all lessons')
    }
  }

  const handleEnableAll = async () => {
    if (!window.confirm(`Enable all lessons for ${selectedStudent.username}?`)) {
      return
    }

    try {
      await enableAllLessons(selectedStudent.id)

      // Reload lesson access
      loadStudentLessons(selectedStudent)

      toast.success(`All lessons enabled for ${selectedStudent.username}`)
    } catch (error) {
      console.error('Failed to enable all lessons:', error)
      toast.error('Failed to enable all lessons')
    }
  }

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading admin panel...</div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>Admin - Student Access Management</title>
      </Head>

      <div className={styles.container}>
        <header className={styles.header}>
          <Link href="/lessons" className={styles.backButton}>
            ← Back to Lessons
          </Link>
          <h1>Student Access Management</h1>
          <div className={styles.adminBadge}>Admin Panel</div>
        </header>

        <div className={styles.layout}>
          {/* Students List */}
          <div className={styles.sidebar}>
            <h2>Students ({students.length})</h2>
            <div className={styles.studentList}>
              {students.map((student) => (
                <button
                  key={student.id}
                  onClick={() => loadStudentLessons(student)}
                  className={`${styles.studentCard} ${
                    selectedStudent?.id === student.id ? styles.active : ''
                  }`}
                >
                  <div className={styles.studentInfo}>
                    <div className={styles.studentName}>{student.username}</div>
                    <div className={styles.studentEmail}>{student.email}</div>
                    {student.full_name && (
                      <div className={styles.studentFullName}>{student.full_name}</div>
                    )}
                  </div>
                  <div className={styles.studentStatus}>
                    {student.is_active ? (
                      <span className={styles.active}>Active</span>
                    ) : (
                      <span className={styles.inactive}>Inactive</span>
                    )}
                  </div>
                </button>
              ))}

              {students.length === 0 && (
                <div className={styles.emptyState}>No students found</div>
              )}
            </div>
          </div>

          {/* Lesson Access Management */}
          <div className={styles.mainPanel}>
            {!selectedStudent ? (
              <div className={styles.emptyState}>
                <p>Select a student to manage their lesson access</p>
              </div>
            ) : isLoadingLessons ? (
              <div className={styles.loading}>Loading lessons...</div>
            ) : (
              <>
                <div className={styles.panelHeader}>
                  <div>
                    <h2>Lesson Access for {selectedStudent.username}</h2>
                    <p className={styles.subtitle}>
                      Enable or disable individual lessons for this student
                    </p>
                  </div>
                  <div className={styles.bulkActions}>
                    <button
                      onClick={() => setShowDisableAllModal(true)}
                      className={styles.dangerButton}
                    >
                      Disable All
                    </button>
                    <button onClick={handleEnableAll} className={styles.successButton}>
                      Enable All
                    </button>
                  </div>
                </div>

                <div className={styles.lessonGrid}>
                  {lessonAccess.map((lesson) => (
                    <div
                      key={lesson.lesson_id}
                      className={`${styles.lessonCard} ${
                        lesson.is_enabled ? styles.enabled : styles.disabled
                      }`}
                    >
                      <div className={styles.lessonHeader}>
                        <h3>{lesson.lesson_title}</h3>
                        <span className={styles.lessonSlug}>{lesson.lesson_slug}</span>
                      </div>

                      <div className={styles.lessonStatus}>
                        <span className={lesson.is_enabled ? styles.badgeEnabled : styles.badgeDisabled}>
                          {lesson.is_enabled ? '✓ Enabled' : '✗ Disabled'}
                        </span>
                      </div>

                      {lesson.disabled_reason && (
                        <div className={styles.disabledReason}>
                          <strong>Reason:</strong> {lesson.disabled_reason}
                        </div>
                      )}

                      <button
                        onClick={() => toggleLessonAccess(lesson)}
                        className={
                          lesson.is_enabled ? styles.disableButton : styles.enableButton
                        }
                      >
                        {lesson.is_enabled ? 'Disable' : 'Enable'}
                      </button>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Disable All Modal */}
        {showDisableAllModal && (
          <div className={styles.modalOverlay} onClick={() => setShowDisableAllModal(false)}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
              <h3>Disable All Lessons</h3>
              <p>
                This will disable all lessons for <strong>{selectedStudent.username}</strong>.
              </p>

              <div className={styles.formGroup}>
                <label>Reason (optional)</label>
                <textarea
                  value={disableReason}
                  onChange={(e) => setDisableReason(e.target.value)}
                  placeholder="e.g., Account suspended, Payment overdue, etc."
                  rows={3}
                  className={styles.textarea}
                />
              </div>

              <div className={styles.modalActions}>
                <button
                  onClick={() => {
                    setShowDisableAllModal(false)
                    setDisableReason('')
                  }}
                  className={styles.cancelButton}
                >
                  Cancel
                </button>
                <button onClick={handleDisableAll} className={styles.dangerButton}>
                  Disable All Lessons
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
