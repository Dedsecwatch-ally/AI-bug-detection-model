# analysis.py
import subprocess
import tempfile
import os
from typing import Optional


MAX_ANALYSIS_CODE = 20000


def run_static_analysis(code: str) -> str:
    """Run Pylint analysis and return results.

    Notes:
    - Limit input size
    - Ensure temporary file is always removed
    - Capture stderr for better error messages
    """
    if not isinstance(code, str):
        return "Invalid code format"
    if len(code) > MAX_ANALYSIS_CODE:
        return "Code too large for analysis"

    tmp_path: Optional[str] = None
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode("utf-8"))
        tmp_path = tmp.name

    try:
        proc = subprocess.run(
            ["pylint", tmp_path, "--score=n", "--disable=C0114,C0115,C0116"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = proc.stdout or proc.stderr or ""
    except Exception as e:
        output = str(e)
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

    return output