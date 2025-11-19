/**
 * Individual lesson page with code editor
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import styles from '../../styles/Lesson.module.css'
import CodeEditor from '../../components/CodeEditor'
import OutputConsole from '../../components/OutputConsole'
import LessonViewer from '../../components/LessonViewer'
import ConfirmModal from '../../components/ConfirmModal'
import LessonSkeleton from '../../components/LessonSkeleton'
import { getLessonBySlug, executeCode, updateProgress } from '../../utils/api'
import { getToken, removeToken } from '../../utils/auth'

export default function LessonPage() {
  const router = useRouter()
  const { slug } = router.query

  const [lesson, setLesson] = useState(null)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState(null)
  const [isExecuting, setIsExecuting] = useState(false)
  const [testResults, setTestResults] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [showResetModal, setShowResetModal] = useState(false)
  const [saveStatus, setSaveStatus] = useState('saved') // 'saving' | 'saved' | 'error'
  const [retryCount, setRetryCount] = useState(0)
  const MAX_RETRIES = 3

  useEffect(() => {
    // Check if user is logged in
    const token = getToken()
    if (!token) {
      router.push('/login')
      return
    }

    if (slug) {
      loadLesson()
    }
  }, [slug, router])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl/Cmd + Enter to run code
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault()
        if (!isExecuting && code.trim()) {
          handleRunCode()
          toast('Running code...', { icon: '⌨️' })
        }
      }

      // Ctrl/Cmd + R to reset (prevent browser refresh)
      if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault()
        if (!isExecuting) {
          handleReset()
        }
      }

      // Escape to clear output
      if (e.key === 'Escape') {
        if (output || testResults) {
          setOutput(null)
          setTestResults(null)
          toast('Output cleared', { icon: '🧹' })
        }
      }

      // Shift + Alt + F to format code
      if (e.shiftKey && e.altKey && e.key === 'F') {
        e.preventDefault()
        if (!isExecuting) {
          handleFormatCode()
        }
      }

      // Ctrl/Cmd + / to show keyboard shortcuts help
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault()
        toast(
          <div style={{ textAlign: 'left' }}>
            <strong>Keyboard Shortcuts:</strong>
            <div style={{ marginTop: '8px', fontSize: '0.9em' }}>
              <div>⌘/Ctrl + Enter - Run Code</div>
              <div>⌘/Ctrl + R - Reset Code</div>
              <div>Shift + Alt + F - Format Code</div>
              <div>Esc - Clear Output</div>
              <div>⌘/Ctrl + / - Show Shortcuts</div>
            </div>
          </div>,
          { duration: 5000, icon: '⌨️' }
        )
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isExecuting, code, output, testResults])

  const loadLesson = async () => {
    try {
      const data = await getLessonBySlug(slug)
      setLesson(data)

      // Check for saved code in localStorage
      const savedCode = localStorage.getItem(`lesson_${data.id}_code`)
      if (savedCode && savedCode !== data.starter_code) {
        setCode(savedCode)
        toast('Restored your previous work', { icon: '💾', duration: 3000 })
      } else {
        setCode(data.starter_code || '# Write your code here\n')
      }
    } catch (error) {
      console.error('Failed to load lesson:', error)
      if (error.response?.status === 401) {
        removeToken()
        router.push('/login')
      } else if (error.response?.status === 404) {
        toast.error('Lesson not found')
        router.push('/lessons')
      } else {
        toast.error('Failed to load lesson')
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Auto-save code to localStorage
  useEffect(() => {
    if (!code || !lesson) return

    setSaveStatus('saving')
    const timeoutId = setTimeout(async () => {
      try {
        localStorage.setItem(`lesson_${lesson.id}_code`, code)
        setSaveStatus('saved')
      } catch (error) {
        setSaveStatus('error')
        console.error('Failed to save code:', error)
        toast.error('Failed to save your work locally')
      }
    }, 1000) // Debounce 1 second

    return () => clearTimeout(timeoutId)
  }, [code, lesson])

  const handleRunCode = async () => {
    if (!code.trim()) {
      toast.error('Please write some code first')
      return
    }

    setIsExecuting(true)
    setOutput(null)
    setTestResults(null)

    try {
      const result = await executeCode({
        code,
        language: lesson.language || 'python',
        lesson_id: lesson.id
      })

      setRetryCount(0) // Reset retry count on success

      setOutput({
        stdout: result.output,
        stderr: result.error,
        executionTime: result.execution_time,
        status: result.status
      })

      if (result.test_results) {
        setTestResults(result.test_results)

        // Calculate score
        const passed = result.test_results.filter(t => t.passed).length
        const total = result.test_results.length
        const score = Math.round((passed / total) * 100)

        // Update progress
        await updateProgress(lesson.id, {
          lesson_id: lesson.id,
          is_completed: passed === total,
          score: score
        })

        if (passed === total) {
          toast.success('🎉 All tests passed! Lesson completed!')
        } else {
          toast(`${passed}/${total} tests passed`, {
            icon: '📝'
          })
        }
      }
    } catch (error) {
      console.error('Execution error:', error)

      const errorMessage = error.userMessage ||
                          error.response?.data?.detail ||
                          'Failed to execute code'

      // Show retry option if error is retryable
      if (error.canRetry && retryCount < MAX_RETRIES) {
        toast.error(
          <div>
            <p>{errorMessage}</p>
            <button
              onClick={() => {
                setRetryCount(prev => prev + 1)
                setIsExecuting(false)
                setTimeout(() => handleRunCode(), 100)
              }}
              style={{
                marginTop: '8px',
                padding: '4px 12px',
                background: '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Retry ({MAX_RETRIES - retryCount} attempts left)
            </button>
          </div>,
          { duration: 5000 }
        )
      } else {
        toast.error(errorMessage)
      }

      setOutput({
        stdout: '',
        stderr: errorMessage,
        executionTime: 0,
        status: 'error'
      })
    } finally {
      setIsExecuting(false)
    }
  }

  const handleReset = () => {
    setShowResetModal(true)
  }

  const confirmReset = () => {
    setCode(lesson.starter_code || '# Write your code here\n')
    setOutput(null)
    setTestResults(null)
    toast.success('Code reset to starter template')
  }

  const handleFormatCode = () => {
    try {
      // Simple Python code formatting
      let formatted = code

      // Remove trailing whitespace from each line
      formatted = formatted.split('\n').map(line => line.trimEnd()).join('\n')

      // Remove multiple consecutive blank lines
      formatted = formatted.replace(/\n{3,}/g, '\n\n')

      // Trim leading/trailing blank lines
      formatted = formatted.trim()

      // Add newline at end of file if not present
      if (formatted && !formatted.endsWith('\n')) {
        formatted += '\n'
      }

      setCode(formatted)
      toast.success('Code formatted successfully')
    } catch (error) {
      console.error('Format error:', error)
      toast.error('Failed to format code')
    }
  }

  if (isLoading) {
    return <LessonSkeleton />
  }

  if (!lesson) {
    return null
  }

  return (
    <>
      <Head>
        <title>{lesson.title} - Coding Platform</title>
        <meta name="description" content={lesson.description} />
      </Head>

      <div className={styles.container}>
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
        <header className={styles.header} role="banner">
          <Link
            href="/lessons"
            className={styles.backButton}
            aria-label="Go back to lessons list"
          >
            ← Back to Lessons
          </Link>
          <h1 id="lesson-title">{lesson.title}</h1>
          <div className={styles.headerActions}>
            <span
              className={styles.difficulty}
              role="status"
              aria-label={`Difficulty level: ${lesson.difficulty}`}
            >
              {lesson.difficulty}
            </span>
          </div>
        </header>

        <div className={styles.layout} id="main-content" role="main">
          <div
            className={styles.leftPanel}
            role="complementary"
            aria-labelledby="lesson-title"
          >
            <LessonViewer lesson={lesson} />
          </div>

          <div className={styles.rightPanel}>
            <div className={styles.editorSection}>
              <div className={styles.editorHeader}>
                <div>
                  <h3 id="editor-heading">Code Editor</h3>
                  <div className={styles.editorMeta}>
                    <div className={styles.keyboardHints}>
                      <span><kbd>⌘</kbd> + <kbd>Enter</kbd> Run</span>
                      <span><kbd>⌘</kbd> + <kbd>R</kbd> Reset</span>
                      <span><kbd>Esc</kbd> Clear</span>
                    </div>
                    <div className={styles.saveStatus}>
                      {saveStatus === 'saving' && (
                        <span className={styles.saving}>
                          <span className={styles.savingDot}></span> Saving...
                        </span>
                      )}
                      {saveStatus === 'saved' && (
                        <span className={styles.saved} aria-live="polite">
                          ✓ Saved
                        </span>
                      )}
                      {saveStatus === 'error' && (
                        <span className={styles.saveError}>
                          ⚠ Save failed
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className={styles.editorActions}>
                  <button
                    onClick={handleFormatCode}
                    className={styles.formatButton}
                    disabled={isExecuting}
                    aria-label="Format code (clean up spacing and indentation)"
                    title="Format Code (Shift+Alt+F)"
                  >
                    ✨ Format
                  </button>
                  <button
                    onClick={handleReset}
                    className={styles.resetButton}
                    disabled={isExecuting}
                    aria-label="Reset code to starter template"
                    aria-describedby="reset-help"
                  >
                    Reset
                  </button>
                  <span id="reset-help" className="sr-only">
                    This will discard your changes and restore the original code
                  </span>
                  <button
                    onClick={handleRunCode}
                    className={styles.runButton}
                    disabled={isExecuting}
                    aria-label={isExecuting ? 'Code is executing' : 'Run code and see results'}
                    aria-live="polite"
                  >
                    {isExecuting ? 'Running...' : 'Run Code'}
                  </button>
                </div>
              </div>
              <div
                role="region"
                aria-labelledby="editor-heading"
                aria-label="Code editor area"
              >
                <CodeEditor
                  value={code}
                  onChange={setCode}
                  language={lesson.language || 'python'}
                  readOnly={isExecuting}
                />
              </div>
            </div>

            <div
              className={styles.outputSection}
              role="region"
              aria-live="polite"
              aria-atomic="true"
              aria-label="Code execution results"
            >
              <OutputConsole
                output={output}
                testResults={testResults}
                isExecuting={isExecuting}
              />
            </div>
          </div>
        </div>

        <ConfirmModal
          isOpen={showResetModal}
          onClose={() => setShowResetModal(false)}
          onConfirm={confirmReset}
          title="Reset Code?"
          message="This will discard all your changes and restore the original starter code. This action cannot be undone."
          confirmText="Reset Code"
          cancelText="Cancel"
          confirmButtonStyle="danger"
        />
      </div>
    </>
  )
}
