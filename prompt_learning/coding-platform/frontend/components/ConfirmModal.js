/**
 * ConfirmModal component - Accessible confirmation dialog
 */

import { useEffect, useRef } from 'react'
import styles from '../styles/ConfirmModal.module.css'

export default function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmButtonStyle = 'danger'
}) {
  const modalRef = useRef(null)
  const previousActiveElement = useRef(null)

  useEffect(() => {
    if (isOpen) {
      // Store the element that had focus before opening modal
      previousActiveElement.current = document.activeElement

      // Focus the modal
      modalRef.current?.focus()

      // Prevent body scroll
      document.body.style.overflow = 'hidden'

      // Trap focus within modal
      const handleTabKey = (e) => {
        const focusableElements = modalRef.current?.querySelectorAll(
          'button:not([disabled]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        if (!focusableElements || focusableElements.length === 0) return

        const firstElement = focusableElements[0]
        const lastElement = focusableElements[focusableElements.length - 1]

        if (e.key === 'Tab') {
          if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault()
            lastElement.focus()
          } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault()
            firstElement.focus()
          }
        }
      }

      // Close on Escape
      const handleEscape = (e) => {
        if (e.key === 'Escape') {
          onClose()
        }
      }

      document.addEventListener('keydown', handleTabKey)
      document.addEventListener('keydown', handleEscape)

      return () => {
        document.removeEventListener('keydown', handleTabKey)
        document.removeEventListener('keydown', handleEscape)
        document.body.style.overflow = 'unset'
        // Restore focus when closing
        previousActiveElement.current?.focus()
      }
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  const handleConfirm = () => {
    onConfirm()
    onClose()
  }

  return (
    <div
      className={styles.overlay}
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-describedby="modal-description"
    >
      <div
        ref={modalRef}
        className={styles.modal}
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <h3 id="modal-title" className={styles.title}>
          {title}
        </h3>
        <p id="modal-description" className={styles.message}>
          {message}
        </p>
        <div className={styles.actions}>
          <button
            onClick={onClose}
            className={styles.cancelButton}
            autoFocus
          >
            {cancelText}
          </button>
          <button
            onClick={handleConfirm}
            className={`${styles.confirmButton} ${styles[confirmButtonStyle]}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}
