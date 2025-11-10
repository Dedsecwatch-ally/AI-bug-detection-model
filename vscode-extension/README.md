AI Bug Fixer VS Code extension

This minimal extension adds a command to send the active editor's code to your local AI Bug Finder backend and open the review in a new editor.

Setup
1. In the `vscode-extension` folder run:
   - `npm install`
   - `npm run compile`
2. In VS Code press F5 to launch the Extension Development Host.

Configuration
- Add a workspace setting `aiBugFixer.apiUrl` to point to your backend (default: http://localhost:8000)

Usage
- Open a code file, run the command "AI Bug Fixer: Review Code" from the command palette (Cmd+Shift+P), and a new document with the review will open.

Packaging & install
1. Build a packaged extension (.vsix):
   - `cd vscode-extension`
   - `npm ci`
   - `npm run compile`
   - `npx vsce package --yarn false`
   This creates a `ai-bug-fixer-vscode-0.0.1.vsix` file.

2. Install the .vsix into VS Code (regular install):
   - In VS Code: Extensions view → click the ellipsis menu → "Install from VSIX..." → select the generated .vsix file.

CI
 - A GitHub Actions workflow `.github/workflows/package-vscode-extension.yml` will build the extension and upload the .vsix as an artifact on push to `main`/`master`.
