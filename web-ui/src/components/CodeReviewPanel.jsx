import React, { useState } from "react";

function applyLinePatches(code, patches) {
  // patches: [{line: 3, content: 'new line text'}] or [{start:1,end:2,content:'...'}]
  const lines = code.split("\n");
  patches.forEach((p) => {
    if (typeof p.line === "number") {
      const idx = p.line - 1;
      if (idx >= 0 && idx < lines.length) lines[idx] = p.content;
      else if (idx === lines.length) lines.push(p.content);
    } else if (typeof p.start === "number" && typeof p.end === "number") {
      const start = Math.max(0, p.start - 1);
      const end = Math.min(lines.length, p.end);
      const insert = (p.content || "").split("\n");
      lines.splice(start, end - start, ...insert);
    }
  });
  return lines.join("\n");
}

export default function CodeReviewPanel({ code, setCode, patches, fullFile, reviewText }) {
  const [preview, setPreview] = useState(code);
  const [mode, setMode] = useState(fullFile ? "full" : patches ? "patches" : "none");

  function previewChanges() {
    if (mode === "full" && fullFile) setPreview(fullFile);
    else if (mode === "patches" && patches) setPreview(applyLinePatches(code, patches));
    else setPreview(code);
  }

  function applyChanges() {
    if (mode === "full" && fullFile) setCode(fullFile);
    else if (mode === "patches" && patches) setCode(applyLinePatches(code, patches));
  }

  return (
    <div style={{ marginTop: 12 }}>
      <h4>Suggested Fixes</h4>
      <div style={{ fontSize: 13, color: '#cbd5e1' }}>{reviewText}</div>

      <div style={{ marginTop: 8 }}>
        <label>
          <input type="radio" checked={mode === 'none'} onChange={() => { setMode('none'); setPreview(code); }} />
          Keep original
        </label>
        {fullFile ? (
          <label style={{ marginLeft: 8 }}>
            <input type="radio" checked={mode === 'full'} onChange={() => { setMode('full'); }} />
            Replace full file
          </label>
        ) : null}
        {patches ? (
          <label style={{ marginLeft: 8 }}>
            <input type="radio" checked={mode === 'patches'} onChange={() => { setMode('patches'); }} />
            Apply patches ({patches.length})
          </label>
        ) : null}
      </div>

      <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
        <button onClick={previewChanges}>Preview</button>
        <button onClick={applyChanges} disabled={mode === 'none'}>Apply</button>
      </div>

      <div style={{ marginTop: 12 }}>
        <h5>Preview</h5>
        <pre style={{ maxHeight: 240, overflow: 'auto', whiteSpace: 'pre-wrap', background: '#071024', padding: 8, borderRadius: 6 }}>{preview}</pre>
      </div>
    </div>
  );
}
// CodeReviewPanel.jsx
