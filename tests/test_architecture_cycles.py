"""
Unit Test for Architecture Cycles
===============================

Перевіряє, чи немає циклічних залежностей між агентами.
"""

import subprocess
import sys
import os

def test_no_architecture_cycles():
    """Тест: немає циклів у архітектурі агентів."""
    result = subprocess.run(
        [sys.executable, "scripts/agent_dependency_audit.py"],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True
    )

    # Якщо є цикли — тест провалено
    assert result.returncode == 0, (
        f"Знайдено циклічні залежності!\\n"
        f"stdout: {result.stdout}\\n"
        f"stderr: {result.stderr}"
    )