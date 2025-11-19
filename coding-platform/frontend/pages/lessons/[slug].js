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

  const loadLesson = async () => {
    try {
      const data = await getLessonBySlug(slug)
      setLesson(data)
      setCode(data.starter_code || '# Write your code here\n')
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
      toast.error('Failed to execute code')
      setOutput({
        stdout: '',
        stderr: error.response?.data?.detail || 'Execution failed',
        executionTime: 0,
        status: 'error'
      })
    } finally {
      setIsExecuting(false)
    }
  }

  const handleReset = () => {
    if (confirm('Are you sure you want to reset your code?')) {
      setCode(lesson.starter_code || '# Write your code here\n')
      setOutput(null)
      setTestResults(null)
    }
  }

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner}></div>
      </div>
    )
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
        <header className={styles.header}>
          <Link href="/lessons" className={styles.backButton}>
            ← Back to Lessons
          </Link>
          <h1>{lesson.title}</h1>
          <div className={styles.headerActions}>
            <span className={styles.difficulty}>{lesson.difficulty}</span>
          </div>
        </header>

        <div className={styles.layout}>
          <div className={styles.leftPanel}>
            <LessonViewer lesson={lesson} />
          </div>

          <div className={styles.rightPanel}>
            <div className={styles.editorSection}>
              <div className={styles.editorHeader}>
                <h3>Code Editor</h3>
                <div className={styles.editorActions}>
                  <button
                    onClick={handleReset}
                    className={styles.resetButton}
                    disabled={isExecuting}
                  >
                    Reset
                  </button>
                  <button
                    onClick={handleRunCode}
                    className={styles.runButton}
                    disabled={isExecuting}
                  >
                    {isExecuting ? 'Running...' : 'Run Code'}
                  </button>
                </div>
              </div>
              <CodeEditor
                value={code}
                onChange={setCode}
                language={lesson.language || 'python'}
                readOnly={isExecuting}
              />
            </div>

            <div className={styles.outputSection}>
              <OutputConsole
                output={output}
                testResults={testResults}
                isExecuting={isExecuting}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
