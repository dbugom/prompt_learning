/**
 * LessonViewer component to display lesson content
 */

import { useMemo } from 'react'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'isomorphic-dompurify'
import styles from '../styles/LessonViewer.module.css'

const md = new MarkdownIt({
  html: false, // Disable HTML tags in source
  linkify: true,
  typographer: true,
  breaks: true,
})

export default function LessonViewer({ lesson }) {
  const htmlContent = useMemo(() => {
    if (!lesson.content) return ''
    const rendered = md.render(lesson.content)
    return DOMPurify.sanitize(rendered)
  }, [lesson.content])

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>{lesson.title}</h2>
        {lesson.description && (
          <p className={styles.description}>{lesson.description}</p>
        )}

        <div className={styles.metadata}>
          {lesson.difficulty && (
            <span className={styles.badge}>{lesson.difficulty}</span>
          )}
          {lesson.language && (
            <span className={styles.badge}>{lesson.language}</span>
          )}
          {lesson.estimated_time && (
            <span className={styles.badge}>
              ~{lesson.estimated_time} min
            </span>
          )}
        </div>

        {lesson.tags && lesson.tags.length > 0 && (
          <div className={styles.tags}>
            {lesson.tags.map((tag, index) => (
              <span key={index} className={styles.tag}>
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className={styles.content}>
        <div
          className={styles.markdown}
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      </div>

      {lesson.test_cases && lesson.test_cases.length > 0 && (
        <div className={styles.requirements}>
          <h3>Requirements</h3>
          <p>Your code will be tested with {lesson.test_cases.length} test case(s).</p>
          <p>Make sure your solution handles all edge cases correctly.</p>
        </div>
      )}
    </div>
  )
}
