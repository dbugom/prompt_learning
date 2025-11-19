/**
 * OutputConsole component to display code execution results
 */

import styles from '../styles/OutputConsole.module.css'

export default function OutputConsole({ output, testResults, isExecuting }) {
  if (isExecuting) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <h3>Output</h3>
          <span className={styles.status}>Running...</span>
        </div>
        <div className={styles.content}>
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>Executing code...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!output && !testResults) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <h3>Output</h3>
        </div>
        <div className={styles.content}>
          <div className={styles.empty}>
            Click "Run Code" to see the output
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>Output</h3>
        {output && (
          <span
            className={`${styles.status} ${
              output.status === 'success' ? styles.success : styles.error
            }`}
          >
            {output.status}
          </span>
        )}
      </div>

      <div className={styles.content}>
        {/* Test Results */}
        {testResults && testResults.length > 0 && (
          <div className={styles.testResults} role="list" aria-label="Test case results">
            <h4 id="test-results-heading">Test Results</h4>
            {testResults.map((test, index) => (
              <div
                key={index}
                className={`${styles.testCase} ${
                  test.passed ? styles.passed : styles.failed
                }`}
                role="listitem"
                aria-labelledby={`test-${index}-description`}
              >
                <div className={styles.testHeader}>
                  <span
                    className={styles.testIcon}
                    role="img"
                    aria-label={test.passed ? 'Test passed' : 'Test failed'}
                  >
                    {test.passed ? '✓' : '✗'}
                  </span>
                  <span id={`test-${index}-description`} className={styles.testDescription}>
                    {test.description || `Test ${test.test_number}`}
                  </span>
                </div>

                {!test.passed && (
                  <div className={styles.testDetails}>
                    <div className={styles.testDetail}>
                      <span className={styles.label}>Input:</span>
                      <code>{test.input || '(empty)'}</code>
                    </div>
                    <div className={styles.testDetail}>
                      <span className={styles.label}>Expected:</span>
                      <code>{test.expected_output}</code>
                    </div>
                    <div className={styles.testDetail}>
                      <span className={styles.label}>Got:</span>
                      <code>{test.actual_output || '(empty)'}</code>
                    </div>
                    {test.error && (
                      <div className={styles.testDetail}>
                        <span className={styles.label}>Error:</span>
                        <code className={styles.error}>{test.error}</code>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}

            <div className={styles.summary}>
              {testResults.filter(t => t.passed).length} / {testResults.length} tests
              passed
            </div>
          </div>
        )}

        {/* Standard Output */}
        {output && output.stdout && (
          <div className={styles.section}>
            <h4>Standard Output</h4>
            <pre className={styles.output}>{output.stdout}</pre>
          </div>
        )}

        {/* Error Output */}
        {output && output.stderr && (
          <div className={styles.section}>
            <h4>Error Output</h4>
            <pre className={`${styles.output} ${styles.error}`}>
              {output.stderr}
            </pre>
          </div>
        )}

        {/* Execution Time */}
        {output && output.executionTime !== undefined && (
          <div className={styles.metadata}>
            <span>Execution time: {output.executionTime.toFixed(3)}s</span>
          </div>
        )}
      </div>
    </div>
  )
}
