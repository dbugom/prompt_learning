/**
 * ExercisePanel Component
 * Displays practical exercises after lesson with hints and validation
 */

import { useState } from 'react'
import { toast } from 'react-hot-toast'
import styles from '../styles/ExercisePanel.module.css'
import CodeEditor from './CodeEditor'

export default function ExercisePanel({ exercises, onComplete }) {
  const [currentExercise, setCurrentExercise] = useState(0)
  const [code, setCode] = useState(exercises[0]?.starter_code || '')
  const [showHint, setShowHint] = useState(false)
  const [completedExercises, setCompletedExercises] = useState(new Set())
  const [isValidating, setIsValidating] = useState(false)

  const exercise = exercises[currentExercise]
  const allCompleted = completedExercises.size === exercises.length

  const validateExercise = () => {
    setIsValidating(true)

    // Perform validation checks
    const validation = exercise.validation
    let allChecksPassed = true
    const failedChecks = []

    if (validation.type === 'code_check') {
      for (const check of validation.checks) {
        if (check.contains) {
          if (!code.includes(check.contains)) {
            allChecksPassed = false
            failedChecks.push(check.message)
          }
        }
      }
    }

    setIsValidating(false)

    if (allChecksPassed) {
      // Mark as completed
      const newCompleted = new Set(completedExercises)
      newCompleted.add(exercise.id)
      setCompletedExercises(newCompleted)

      toast.success('✓ Exercise completed!', { duration: 3000 })

      // Check if all exercises are done
      if (newCompleted.size === exercises.length) {
        setTimeout(() => {
          toast.success('🎉 All exercises completed! You can proceed to the next lesson!', {
            duration: 5000
          })
          onComplete?.()
        }, 1000)
      } else {
        // Move to next exercise after a delay
        setTimeout(() => {
          const nextIndex = currentExercise + 1
          if (nextIndex < exercises.length) {
            setCurrentExercise(nextIndex)
            setCode(exercises[nextIndex].starter_code)
            setShowHint(false)
            toast('Moving to next exercise...', { icon: '➡️' })
          }
        }, 2000)
      }
    } else {
      toast.error(
        <div>
          <strong>Not quite right!</strong>
          <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
            {failedChecks.map((msg, idx) => (
              <li key={idx}>{msg}</li>
            ))}
          </ul>
        </div>,
        { duration: 5000 }
      )
    }
  }

  const handleExerciseChange = (index) => {
    setCurrentExercise(index)
    setCode(exercises[index].starter_code)
    setShowHint(false)
  }

  const handleShowSolution = () => {
    if (window.confirm('Are you sure you want to see the solution? Try the hint first!')) {
      setCode(exercise.solution_code)
      toast('Solution loaded. Study it and try to understand!', { icon: '💡' })
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Practical Exercises</h2>
        <p>Complete these exercises to unlock the next lesson</p>
      </div>

      {/* Exercise Navigation */}
      <div className={styles.exerciseTabs}>
        {exercises.map((ex, idx) => (
          <button
            key={ex.id}
            onClick={() => handleExerciseChange(idx)}
            className={`${styles.tab} ${
              currentExercise === idx ? styles.active : ''
            } ${completedExercises.has(ex.id) ? styles.completed : ''}`}
          >
            {completedExercises.has(ex.id) && '✓ '}
            Exercise {idx + 1}
          </button>
        ))}
      </div>

      {/* Exercise Content */}
      <div className={styles.exerciseContent}>
        <div className={styles.questionSection}>
          <h3>{exercise.title}</h3>
          <div className={styles.question}>
            {exercise.question.split('\n').map((line, idx) => (
              <p key={idx}>{line}</p>
            ))}
          </div>

          {/* Hint Section */}
          <div className={styles.hintSection}>
            {!showHint ? (
              <button
                onClick={() => setShowHint(true)}
                className={styles.hintButton}
              >
                💡 Show Hint
              </button>
            ) : (
              <div className={styles.hint}>
                <strong>💡 Hint:</strong> {exercise.hint}
              </div>
            )}
          </div>
        </div>

        {/* Code Editor */}
        <div className={styles.editorSection}>
          <div className={styles.editorHeader}>
            <span>Your Solution</span>
            <button
              onClick={handleShowSolution}
              className={styles.solutionButton}
            >
              View Solution
            </button>
          </div>
          <CodeEditor
            value={code}
            onChange={setCode}
            language="python"
            height="300px"
          />
        </div>

        {/* Actions */}
        <div className={styles.actions}>
          <button
            onClick={validateExercise}
            disabled={isValidating || completedExercises.has(exercise.id)}
            className={styles.validateButton}
          >
            {completedExercises.has(exercise.id)
              ? '✓ Completed'
              : isValidating
              ? 'Validating...'
              : 'Check Solution'}
          </button>

          {completedExercises.has(exercise.id) && currentExercise < exercises.length - 1 && (
            <button
              onClick={() => handleExerciseChange(currentExercise + 1)}
              className={styles.nextButton}
            >
              Next Exercise →
            </button>
          )}
        </div>
      </div>

      {/* Progress */}
      <div className={styles.progress}>
        <div className={styles.progressBar}>
          <div
            className={styles.progressFill}
            style={{ width: `${(completedExercises.size / exercises.length) * 100}%` }}
          />
        </div>
        <p>
          {completedExercises.size} of {exercises.length} exercises completed
          {allCompleted && ' 🎉'}
        </p>
      </div>
    </div>
  )
}
