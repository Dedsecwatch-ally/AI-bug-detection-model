// App.jsx
import React, { useState } from "react";
import Editor from "@monaco-editor/react";
import { sendCodeForReview } from "./api";
import "./styles.css";
import CodeReviewPanel from "./components/CodeReviewPanel";

export default function App() {
  const [code, setCode] = useState(`# Write your Python code here
def add(a,b):
  return a-b`);
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [staticReport, setStaticReport] = useState("");
  const [patches, setPatches] = useState(null);
  const [fullFile, setFullFile] = useState(null);

  async function handleReview() {
      setLoading(true);
      setError("");
      setStaticReport("");
      setPatches(null);
      setFullFile(null);
      try {
        const res = await sendCodeForReview(code);
        if (!res.ok) {
          setError(res.error || "Server error");
          return;
        }
        setReview(res.data.review || "");
        setStaticReport(res.data.static_report || "");
        // optional structured fields: patches (array) and full_file (string)
        if (res.data.full_file) setFullFile(res.data.full_file);
        if (res.data.patches) setPatches(res.data.patches);
      } finally {
        setLoading(false);
      }
  }

  return (
    <div className="app">
      <header>
        <h1>🧠 AI Bug Finder & Code Reviewer</h1>
        <button onClick={handleReview} disabled={loading}>
          {loading ? "Analyzing..." : "Review Code"}
        </button>
      </header>

      <main>
        <section className="editor">
          <Editor
            height="60vh"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value)}
            theme="vs-dark"
          />
        </section>

        <section className="output">
          <h3>Review Result</h3>
            {error ? <div style={{ color: 'salmon' }}>{error}</div> : null}
            <pre style={{ whiteSpace: 'pre-wrap' }}>{review}</pre>
            {staticReport ? (
              <>
                <h4>Static analysis</h4>
                <pre style={{ whiteSpace: 'pre-wrap' }}>{staticReport}</pre>
              </>
            ) : null}

            {/* Code review panel shows patches / preview / apply actions */}
            <CodeReviewPanel
              code={code}
              setCode={setCode}
              patches={patches}
              fullFile={fullFile}
              reviewText={review}
            />
        </section>
      </main>
    </div>
  );
}