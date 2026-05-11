import os
import sys
import subprocess
import tempfile

_MAX_OUTPUT = 10_240  # bytes

# Prepended to every submission. Runs in the subprocess before user code.
_SANDBOX_PREAMBLE = '''\
import sys as __sys

class __Blocker:
    _banned = frozenset([
        "os", "nt", "posix", "subprocess", "socket", "socketserver",
        "shutil", "pathlib", "importlib", "ctypes", "multiprocessing",
        "threading", "signal", "pty", "winreg", "msvcrt", "mmap",
        "resource", "select", "selectors", "asyncio",
    ])
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in self._banned:
            raise ImportError(f"Module \'{name}\' is blocked in the sandbox.")
        return None

__sys.meta_path.insert(0, __Blocker())
for __m in list(__Blocker._banned):
    __sys.modules.pop(__m, None)

import builtins as __bi
_ro = __bi.open
def __safe_open(file, mode="r", *args, **kwargs):
    if any(c in str(mode) for c in "wax"):
        raise PermissionError("File writes are blocked in the sandbox.")
    return _ro(file, mode, *args, **kwargs)
__bi.open = __safe_open
del __sys, __m, __bi, _ro, __safe_open, __Blocker
'''


def run_code(source_code: str, test_cases: list[dict], timeout: int = 5) -> list[dict]:
    results = []

    for test in test_cases:
        sandboxed = _SANDBOX_PREAMBLE + "\n" + source_code

        with tempfile.NamedTemporaryFile(
            suffix=".py", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write(sandboxed)
            tmp = f.name

        try:
            proc = subprocess.run(
                [sys.executable, tmp],
                input=str(test.get("input", "")),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            actual = proc.stdout.strip()
            if len(actual) > _MAX_OUTPUT:
                actual = actual[:_MAX_OUTPUT] + "\n[output truncated]"
            expected = str(test.get("expected", "")).strip()
            results.append({
                "test_id":  test.get("id", len(results) + 1),
                "passed":   actual == expected,
                "expected": expected,
                "got":      actual,
                "error":    proc.stderr.strip() or None,
            })
        except subprocess.TimeoutExpired:
            results.append({
                "test_id":  test.get("id", len(results) + 1),
                "passed":   False,
                "expected": str(test.get("expected", "")),
                "got":      None,
                "error":    "Time limit exceeded (5s)",
            })
        finally:
            os.unlink(tmp)

    return results
