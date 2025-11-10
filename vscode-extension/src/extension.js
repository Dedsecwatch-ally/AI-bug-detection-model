const vscode = require('vscode');
const fetch = require('node-fetch');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const output = vscode.window.createOutputChannel('AI Bug Fixer');

  let disposable = vscode.commands.registerCommand('aiBugFixer.reviewCode', async function () {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('Open a file to review first');
      return;
    }

    const code = editor.document.getText();
    const apiUrl = vscode.workspace.getConfiguration('aiBugFixer').get('apiUrl') || 'http://localhost:8000';
    output.appendLine('Sending code to AI Bug Finder...');
    output.show(true);

    // Show a progress notification while awaiting the review
    await vscode.window.withProgress({
      location: vscode.ProgressLocation.Notification,
      title: 'AI Bug Finder: analyzing code',
      cancellable: false
    }, async (progress) => {
      progress.report({ message: 'Sending code...' });
      try {
        const res = await fetch(`${apiUrl}/review`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code })
        });

        if (!res.ok) {
          const body = await res.text();
          vscode.window.showErrorMessage(`Review failed: ${res.status} ${body}`);
          output.appendLine(`Error: ${res.status} ${body}`);
          return;
        }

        progress.report({ message: 'Processing response...' });
        const json = await res.json();
        const reviewText = json.review || '';
        const staticReport = json.static_report || '';

        // open a new read-only document with the review
        const doc = await vscode.workspace.openTextDocument({ content: `Review:\n\n${reviewText}\n\nStatic analysis:\n\n${staticReport}`, language: 'markdown' });
        await vscode.window.showTextDocument(doc, { preview: false });

        output.appendLine('Review received.');

        // Attempt to parse and apply quick fixes
        await tryApplyQuickFixes(reviewText, editor, output);
      } catch (err) {
        vscode.window.showErrorMessage('Error sending code: ' + err.message);
        output.appendLine('Error sending code: ' + err.message);
      }
    });
  });

  context.subscriptions.push(disposable);
}

/**
 * Try to parse the review text for quick-fix instructions and apply them.
 * Supports two simple formats:
 * 1) Full file replacement: a block starting with 'PATCH_FULL:' followed by a fenced code block
 * 2) Line replacements: lines like 'Replace line N: <new content>' (1-based line numbers)
 */
async function tryApplyQuickFixes(reviewText, editor, output) {
  if (!reviewText || !editor) return;

  // Check for PATCH_FULL:```py\n...``` or ```\n
  const patchFullMatch = reviewText.match(/PATCH_FULL:\s*```(?:[a-zA-Z0-9]+)?\n([\s\S]*?)```/m);
  if (patchFullMatch) {
    const newContent = patchFullMatch[1];
    const confirmed = await vscode.window.showInformationMessage('Apply full-file patch suggested by AI?', 'Apply', 'Ignore');
    if (confirmed === 'Apply') {
      const fullRange = new vscode.Range(
        editor.document.positionAt(0),
        editor.document.positionAt(editor.document.getText().length)
      );
      await editor.edit((eb) => eb.replace(fullRange, newContent));
      output.appendLine('Applied full-file patch from review.');
    }
    return;
  }

  // Line replacements
  const lineReplaceRegex = /Replace line (\d+):\s*(.*)/g;
  let m;
  const edits = [];
  while ((m = lineReplaceRegex.exec(reviewText)) !== null) {
    const lineNum = parseInt(m[1], 10) - 1; // convert to 0-based
    const newLine = m[2];
    if (isNaN(lineNum) || lineNum < 0 || lineNum >= editor.document.lineCount) continue;
    edits.push({ line: lineNum, text: newLine });
  }

  if (edits.length === 0) return;

  const confirmed = await vscode.window.showInformationMessage(`Apply ${edits.length} quick fix(es) suggested by AI?`, 'Apply', 'Ignore');
  if (confirmed !== 'Apply') return;

  await editor.edit((eb) => {
    for (const e of edits) {
      const line = editor.document.lineAt(e.line);
      eb.replace(line.range, e.text);
    }
  });
  output.appendLine(`Applied ${edits.length} quick fix(es) from review.`);
}

function deactivate() {}

module.exports = { activate, deactivate };
