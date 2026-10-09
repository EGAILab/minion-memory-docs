# Minion-Memory project environment (Owner rule OWN-001, 2026-10-09) — POSIX/Git-Bash variant.
# Every project-controlled temp file, cache, build output and review worktree lives on E: inside
# the Minion-Memory project folder. Never on C:.
#
#   . /e/AI/Projects/OpenMinds/Minions/Minion-Memory/minion-memory-docs/process/environment/project-environment.sh
#
# Linux/WSL/Docker: set MNEME_ROOT to the mounted project folder first; keep Linux outputs separate.

MNEME_ROOT="${MNEME_ROOT:-/e/AI/Projects/OpenMinds/Minions/Minion-Memory}"
MNEME_TMP="$MNEME_ROOT/.tmp"
MNEME_CACHE="$MNEME_TMP/cache"
mkdir -p "$MNEME_TMP/process-temp" "$MNEME_CACHE" "$MNEME_TMP/work" "$MNEME_ROOT/review-worktrees"

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) MNEME_PLATFORM=windows; MNEME_W="E:/AI/Projects/OpenMinds/Minions/Minion-Memory/.tmp" ;;
  *) MNEME_PLATFORM=linux; MNEME_W="$MNEME_TMP" ;;
esac

export TEMP="$MNEME_W/process-temp" TMP="$MNEME_W/process-temp" TMPDIR="$MNEME_W/process-temp"
export UV_CACHE_DIR="$MNEME_W/cache/uv"
export UV_PYTHON_INSTALL_DIR="$MNEME_W/cache/uv-python"
export PIP_CACHE_DIR="$MNEME_W/cache/pip"
export PYTHONPYCACHEPREFIX="$MNEME_W/cache/pycache"
export RUFF_CACHE_DIR="$MNEME_W/cache/ruff"
export MYPY_CACHE_DIR="$MNEME_W/cache/mypy"
export HYPOTHESIS_STORAGE_DIRECTORY="$MNEME_W/cache/hypothesis"
export CARGO_TARGET_DIR="$MNEME_W/cache/cargo-target/$MNEME_PLATFORM"
export MNEME_PYTEST_CACHE="$MNEME_W/cache/pytest"
export MNEME_VENV_ROOT="$MNEME_W/cache/venvs"
