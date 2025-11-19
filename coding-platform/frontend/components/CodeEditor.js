/**
 * CodeEditor component using CodeMirror 6
 */

import { useCallback } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { javascript } from '@codemirror/lang-javascript'
import { oneDark } from '@codemirror/theme-one-dark'
import styles from '../styles/CodeEditor.module.css'

const languageExtensions = {
  python: python(),
  javascript: javascript({ jsx: true }),
}

export default function CodeEditor({ value, onChange, language = 'python', readOnly = false }) {
  const handleChange = useCallback(
    (val) => {
      onChange(val)
    },
    [onChange]
  )

  const extensions = [languageExtensions[language] || python()]

  return (
    <div className={styles.editorContainer}>
      <CodeMirror
        value={value}
        height="100%"
        theme={oneDark}
        extensions={extensions}
        onChange={handleChange}
        readOnly={readOnly}
        basicSetup={{
          lineNumbers: true,
          highlightActiveLineGutter: true,
          highlightSpecialChars: true,
          foldGutter: true,
          drawSelection: true,
          dropCursor: true,
          allowMultipleSelections: true,
          indentOnInput: true,
          syntaxHighlighting: true,
          bracketMatching: true,
          closeBrackets: true,
          autocompletion: true,
          rectangularSelection: true,
          crosshairCursor: true,
          highlightActiveLine: true,
          highlightSelectionMatches: true,
          closeBracketsKeymap: true,
          defaultKeymap: true,
          searchKeymap: true,
          historyKeymap: true,
          foldKeymap: true,
          completionKeymap: true,
          lintKeymap: true,
        }}
        className={styles.editor}
      />
    </div>
  )
}
