/**
 * LessonSkeleton - Loading skeleton for lesson page
 */

import styles from '../styles/LessonSkeleton.module.css'

export default function LessonSkeleton() {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.skeletonBox} style={{ width: '120px', height: '36px' }}></div>
        <div className={styles.skeletonBox} style={{ width: '300px', height: '32px' }}></div>
        <div className={styles.skeletonBox} style={{ width: '80px', height: '36px' }}></div>
      </div>

      <div className={styles.layout}>
        <div className={styles.leftPanel}>
          <div className={styles.skeletonBox} style={{ width: '60%', height: '28px', marginBottom: '12px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '40%', height: '20px', marginBottom: '24px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '100%', height: '16px', marginBottom: '8px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '100%', height: '16px', marginBottom: '8px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '90%', height: '16px', marginBottom: '8px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '100%', height: '16px', marginBottom: '24px' }}></div>
          <div className={styles.skeletonBox} style={{ width: '100%', height: '120px', borderRadius: '8px' }}></div>
        </div>

        <div className={styles.rightPanel}>
          <div className={styles.editorSection}>
            <div className={styles.editorHeader}>
              <div className={styles.skeletonBox} style={{ width: '100px', height: '24px' }}></div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <div className={styles.skeletonBox} style={{ width: '80px', height: '36px' }}></div>
                <div className={styles.skeletonBox} style={{ width: '100px', height: '36px' }}></div>
              </div>
            </div>
            <div className={styles.skeletonBox} style={{ width: '100%', height: '400px' }}></div>
          </div>

          <div className={styles.outputSection}>
            <div className={styles.skeletonBox} style={{ width: '100px', height: '24px', marginBottom: '16px' }}></div>
            <div className={styles.skeletonBox} style={{ width: '100%', height: '200px' }}></div>
          </div>
        </div>
      </div>
    </div>
  )
}
